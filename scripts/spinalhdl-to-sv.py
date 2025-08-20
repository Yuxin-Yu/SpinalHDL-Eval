import os
import shutil
import re
from pathlib import Path
import argparse
from tqdm import tqdm
import re

sbt_cnt_fail = 0
sbt_cnt_success = 0

def process_prob_folders(source_dir, target_dir,sbt_dir):
    """
    处理所有以Prob开头的文件夹
    :param source_dir: 源目录
    :param target_dir: 目标目录
    """
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)
    
    # 查找所有以Prob开头的文件夹
    prob_folders = [f for f in os.listdir(source_dir) 
                   if f.startswith('Prob') and os.path.isdir(os.path.join(source_dir, f))]
    
    if not prob_folders:
        print(f"警告: 在源目录 {source_dir} 中未找到以'Prob'开头的文件夹")
        return
    
    for folder in tqdm(prob_folders, desc="处理进度"):
        source_folder = os.path.join(source_dir, folder)
        target_folder = os.path.join(target_dir, folder)
        # 删除target_dir目录下以Prob开头的文件夹
        for subfolder in os.listdir(target_dir):
            subfolder_path = os.path.join(target_dir, subfolder)
            if subfolder.startswith('Prob') and os.path.isdir(subfolder_path):
                shutil.rmtree(subfolder_path)
        # 删除sbt_dir目录下任何.v文件
        for root, dirs, files in os.walk(sbt_dir):
            for file in files:
                if file.endswith('.v'):
                    v_file_path = os.path.join(root, file)
                    try:
                        os.remove(v_file_path)
                        print(f"已删除Verilog文件: {v_file_path}")
                    except Exception as e:
                        print(f"删除文件时出错: {v_file_path}, 错误: {e}")
        # 1. 复制文件夹到目标目录
        print(f"处理文件夹: {folder}")
        copy_folder(source_folder, target_folder)
        
        # 2. 处理所有scala文件
        process_scala_files(target_folder)
        
        # 3. 运行sbt命令
        run_sbt_commands(sbt_dir,source_folder,target_folder)
        

        print(f"完成处理: {folder}\n")
    
    # 在source_dir目录下生成scala2sv-summary.txt，写入sbt执行情况
    summary_path = os.path.join(source_dir, "spinalhdl2sv-summary.txt")
    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(f"sbt执行成功次数: {sbt_cnt_success}\n")
            f.write(f"sbt执行失败次数: {sbt_cnt_fail}\n")
        print(f"已生成sbt执行情况汇总: {summary_path}")
    except Exception as e:
        print(f"写入scala2sv-summary.txt时出错: {e}")

def copy_folder(src, dst):
    """复制文件夹"""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def process_scala_files(folder):
    """处理所有scala文件，添加package头"""
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.scala'):
                file_path = os.path.join(root, file)
                # 检查scala文件是否包含object TopMain，如果没有则在文件末尾添加
                add_topmain_object_if_missing(file_path)
                # 检查scala文件是否包含val io = new Bundle{，如果包含，则匹配出所有输入输出端口，并在其后添加io.端口信号.setName("端口信号")
                add_setname_to_ports(file_path)
                add_package_header(file_path, folder)

def add_setname_to_ports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 查找val io = new Bundle { 的起止行
    bundle_start = None
    bundle_end = None
    for idx, line in enumerate(lines):
        if re.search(r'val\s+io\s*=\s*new\s+Bundle\s*\{', line):
            bundle_start = idx
            break
    if bundle_start is None:
        return  # 没有io Bundle，直接返回

    # 找到Bundle的结束行（大括号配对）
    brace_count = 0
    for idx in range(bundle_start, len(lines)):
        brace_count += lines[idx].count('{')
        brace_count -= lines[idx].count('}')
        if brace_count == 0:
            bundle_end = idx
            break
    if bundle_end is None:
        return  # 没有正确配对，返回

    # 匹配端口定义行
    port_pattern = re.compile(r'^\s*val\s+(\w+)\s*=\s*(in|out)\s+\w+\(.*\)')
    # 记录要插入setName的行号和端口名
    insertions = []
    for idx in range(bundle_start+1, bundle_end):
        match = port_pattern.match(lines[idx])
        if match:
            port_name = match.group(1)
            # 检查下一行是否已经有setName
            next_line = lines[idx+1] if idx+1 < len(lines) else ""
            if f'io.{port_name}.setName' not in next_line:
                insertions.append((idx, port_name))

    # 倒序插入，避免行号错位
    for idx, port_name in reversed(insertions):
        indent = re.match(r'^(\s*)', lines[idx]).group(1)
        setname_line = f'{indent}io.{port_name}.setName("{port_name}")\n'
        lines.insert(bundle_end+1, setname_line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)               

def add_package_header(file_path, folder_path):
    """给scala文件添加package头"""
    folder_name = os.path.basename(folder_path)
    scala_file_name = os.path.splitext(os.path.basename(file_path))[0]
    package_line = f"package {folder_name}.{scala_file_name}\n"
    
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        # 检查是否已经有package声明
        if not content.startswith('package'):
            # 如果没有，添加package行
            f.seek(0, 0)
            f.write(package_line + content)
            print(f"已添加package头到: {file_path}")

def run_sbt_commands(sbtdir,source_folder,target_dir):
    """运行sbt命令"""
    global sbt_cnt_fail, sbt_cnt_success  # 添加这行声明
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.scala'):
                scala_file_name = os.path.splitext(file)[0]
                folder_name = os.path.basename(target_dir)
                cmd = f'sbt "runMain {folder_name}.{scala_file_name}.TopMain"'
                
                print(f"正在运行: {cmd}")
                os.chdir(sbtdir)  # 切换到目标文件夹
                exit_code = os.system(cmd)

                 # 构造新文件名
                new_verilog_name = f"{scala_file_name}.sv"
                # 找到源scala文件的目录
                dest_verilog_path = os.path.join(source_folder, new_verilog_name)
                # 移动并重命名
                # 如果目标文件已存在，先删除再移动，实现覆盖
                if os.path.exists(dest_verilog_path):
                    os.remove(dest_verilog_path)
                
                if exit_code != 0:
                    # 即使命令执行失败，也要创建目标Verilog文件（空文件或占位）
                    with open(dest_verilog_path, 'w', encoding='utf-8') as f:
                        f.write('// Verilog file generation failed or sbt command failed.\n')
                    print(f"命令执行失败: {cmd}")
                    sbt_cnt_fail=sbt_cnt_fail + 1
                else:
                    # 根据指令，当sbt命令执行成功时，将sbt目录下的TopModule.v重命名为scala文件名，并移动到源scala目录中
                    topmodule_v_path = os.path.join(sbtdir, "TopModule.v")
                    if os.path.exists(topmodule_v_path):
                        shutil.move(topmodule_v_path, dest_verilog_path)
                        print(f"已将TopModule.v重命名为{new_verilog_name}并移动到: {dest_verilog_path}")
                    else:
                        print(f"未找到TopModule.v于: {topmodule_v_path}")
                    print(f"命令执行成功: {cmd}")
                    sbt_cnt_success = sbt_cnt_success + 1
                    
                    
def process_verilog_files(target_folder, source_folder):
    """处理生成的Verilog文件"""
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file == 'TopModule.v':
                # 找到对应的scala文件名
                scala_file = find_corresponding_scala(root)
                if scala_file:
                    scala_name = os.path.splitext(scala_file)[0]
                    new_name = f"{scala_name}.v"
                    
                    # 重命名文件
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, new_name)
                    os.rename(old_path, new_path)
                    
                    # 复制到源文件夹
                    dest_path = os.path.join(source_folder, new_name)
                    shutil.copy2(new_path, dest_path)
                    print(f"已复制Verilog文件到: {dest_path}")

def find_corresponding_scala(folder):
    """在文件夹中查找对应的scala文件"""
    for file in os.listdir(folder):
        if file.endswith('.scala'):
            return file
    return None

def add_topmain_object_if_missing(file_path):
    """如果scala文件中没有object TopMain，则在文件末尾追加TopMain对象定义"""
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        if 'object TopMain' not in content:
            topmain_code = """

object TopMain {
  def main(args: Array[String]) {
    SpinalVerilog(new TopModule)
  }
}
"""
            f.seek(0, 2)
            f.write(topmain_code)
            print(f"已在文件末尾添加TopMain对象: {file_path}")

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(
        description='处理以Prob开头的文件夹中的Scala文件，生成Verilog并复制回源文件夹',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-s', '--source', 
                        default='/home/yyx/riscv/verilog-eval/build',
                        help='源目录路径，包含以Prob开头的文件夹')
    parser.add_argument('-t', '--target', 
                        default='/home/yyx/riscv/verilog-eval/hw',
                        help='目标目录路径，用于临时处理文件')
    parser.add_argument('-sbt', '--sbtdir', 
                        default='/home/yyx/riscv/verilog-eval',
                        help='执行sbt命令的文件夹路径')
    parser.add_argument('-v', '--verbose', 
                        action='store_true',
                        help='显示详细输出信息')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("详细模式启用")
        print(f"源目录: {args.source}")
        print(f"目标目录: {args.target}")
    
    print("开始处理Prob文件夹...")
    process_prob_folders(args.source, args.target,args.sbtdir)
    print("所有文件夹处理完成!")

if __name__ == "__main__":
    main()
