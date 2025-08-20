# SpinalHDL-Eval：基于Verilog-Eval的大模型SpinalHDL代码生成能力评估基准

>[**🇺🇸 English README**](README.md) | [**🇨🇳 中文版**](README_CN.md)

本项目是在**Verilog-Eval基准框架(https://github.com/NVlabs/verilog-eval)**基础上**修改和增强**而来，专门用于评估大语言模型（LLM）的SpinalHDL代码生成能力。Verilog-Eval专注于Verilog RTL生成，而本项目将其扩展到SpinalHDL——一种基于Scala的强大硬件描述语言，通过先进的软件工程技术实现复杂的数字电路设计。

项目继承了Verilog-Eval基准的156个综合设计问题，但对它们进行了适配，使其适用于SpinalHDL代码生成，为使用SpinalHDL的Scala-based HDL方法进行硬件设计的大模型性能评估提供系统化的基准框架。

## 🚀 项目概览

本项目包含两大核心组件：
1. **SpinalHDL-Eval评估基准**：包含156个多样化硬件设计问题的严格评估框架
2. **Context7 MCP增强框架**：基于n8n的大模型SpinalHDL代码自动化生成系统

## 📂 项目结构

```
.
├── build.sbt                 # Scala/SpinalHDL的SBT构建配置
├── Makefile.in               # 构建配置模板
├── dataset_spec-to-spinalhdl # 包含156个设计问题的综合数据集
├── hw/                       # 硬件源文件目录
├── n8n/                      # Context7 MCP自动化框架
│   └── SpinalHDL-Eval-MCP.json  # n8n自动化工作流配置
├── openrouter/               # OpenRouter大模型集成脚本
├── project/                  # SBT项目配置
├── scripts/                  # 高级LLM集成和代码生成脚本
└── README.md                 # 英文版文档
└── README_CN.md              # 中文版文档（本文件）
```

## 🔧 核心组件

### 1. 综合评估数据集 (`dataset_spec-to-spinalhdl/`)

基准测试包含**156个多样化的硬件设计问题**，跨越多个复杂度和应用领域。每个问题包含：

- **`_prompt.txt`**：详细自然语言规范，描述期望的硬件功能
- **`_ref.sv`**：正确性验证用的参考Verilog实现
- **`_test.sv`**：包含验证场景的综合测试平台
#### 🎯 针对SpinalHDL特性所做的适配
  为实现 SpinalHDL 代码的生成与评估，我们对提示词（prompt）进行了系统性的适配，主要包括提示词适配和增加SpinalHDL转Verilog流程两个方面。
##### 提示词适配

###### 系统提示词优化
- **角色定位调整**：修改了大语言模型（LLM）的角色定位和输出方式，使其更适合生成 SpinalHDL 代码
- **代码模板引入**：新增如下所示的代码模板结构，显著提高了后续 SpinalHDL 代码转换为 Verilog 的成功率
``` java
You are a SpinalHDL RTL designer that only writes code using correct SpinalHDL syntax(base spinalHDL 1.12.0 version).Response use follow pattern:

import spinal.core._
import spinal.lib._

// Hardware definition
case class TopModule() extends Component {
  
}

object TopMain {
  def main(args: Array[String]) {
    SpinalVerilog(new TopModule)
  }
}

```

###### 测试用例适配
- **关键词冲突解决**：将原 Verilog-Eval 测试用例中的输入信号 `in` 改为 `din`，输出信号 `out` 改为 `dout`，避免与 SpinalHDL 关键字冲突
- **Testbench同步更新**：相应更新了测试平台中的信号名称，确保测试的一致性

##### SpinalHDL转Verilog
见下一节描述

### 2. 代码生成脚本 (`scripts/`)

#### spinalhdl-to-sv脚本
基于 SpinalHDL 官方 1.12.0 版的 [SpinalTemplateSbt](https://github.com/SpinalHDL/SpinalTemplateSbt) 项目修改实现。
##### 转换流程
1. **代码预处理**
   - 从 LLM 输出目录拷贝 SpinalHDL 代码到hw临时目录
   - 添加 package 名称
   - 检查 TopMain 目标是否存在

2. **代码生成**
   - 使用 Sbt 指令生成 Verilog 代码
   - 实时记录执行状态

3. **结果处理**
   - 转换成功：将生成的 Verilog 代码重命名并拷贝到目标目录
   - 转换失败：直接进入下一个转换循环

4. **循环处理**
   - 循环处理所有待转换文件
   - 最终整理并输出所有转换任务的执行信息

##### 环境要求
- SpinalHDL 开发环境
- Sbt 和 Scala 相关依赖
- Java 运行环境

##### 注意事项
- 确保代码中的 TopMain 目标正确定义
- 检查生成代码的包名配置是否正确
- 转换过程中会生成临时文件，请注意磁盘空间管理

### 3. Context7 MCP框架 (`n8n/`)

**Context7 MCP框架**代表了自动化硬件设计的突破，提供了基于n8n的工作流，用于使用前沿LLM进行系统化SpinalHDL代码生成。

#### 🏗️ 架构概览
```
工作流流程：
[手动触发] → [文件处理] → [上下文增强] → [LLM生成] → [代码提取] → [输出管理]
```

#### 🔑 核心组件 (`SpinalHDL-Eval-MCP.json`)

**📁 输入处理**
- **文件读取器**：顺序处理所有156个提示文件
- **目录结构**：创建有组织的输出目录(`output/ProbXXX_problem_name/`)
- **路径解析**：文件路径和命名规范的自动处理

**🧠 LLM增强**
- **Context7集成**：通过MCP协议注入SpinalHDL文档
- **提示优化**：自动附加context7工具提示提高准确性
- **模型灵活性**：可配置任何OpenRouter支持的模型

**⚙️ 生成管道**
- **并行处理**：高效批量跨问题生成
- **错误处理**：强大的错误恢复和重试机制
- **格式验证**：从LLM响应自动提取SpinalHDL代码
- **日志记录**：用于调试和分析的综合生成日志

**💾 输出管理**
- **有序存储**：每个问题都有带结果的专用目录
- **双格式输出**：
  - `sample01.scala`：生成的SpinalHDL实现
  - `log01.log`：详细生成日志和元数据
- **批量汇总**：所有问题的聚合结果

## 🚀 快速开始

### 环境准备
```bash
# 设置OpenRouter API密钥
export OPENROUTER_API_KEY="你的-api-密钥"
```

### 手动评估示例

#### 生成单个问题代码
```bash
# 使用指定模型测试具体问题
./scripts/sv-generate --model gpt-4o \
  --language spinalhdl \
  --task spec-to-rtl \
  --output generated.scala \
  dataset_spec-to-spinalhdl/Prob144_conwaylife_prompt.txt

# 使用默认模型测试所有问题
cd build
make sv-generate LANGUAGE=spinalhdl
```

#### 编译生成的代码
```bash
# 使用自动转换脚本
python3 ./scripts/spinalhdl-to-sv.py -s ./build -t hw -sbt .
```
### 测试生成的Verilog代码
```bash
cd build
make sv-iv-test
```

### 分析生成的Verilog代码
```bash
cd build
make sv-iv-analyze
```
### Context7 MCP自动化评估

#### 工作流设置
```bash
# 1. 安装并启动n8n（假设已安装Docker）
docker run -it --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# 2. 加载工作流
n8n import:workflow --input=n8n/SpinalHDL-Eval-MCP.json

# 3. 配置凭据
# 在浏览器访问 http://localhost:5678
# 配置：OpenRouter API密钥和Context7 MCP服务器

# 4. 执行评估
# 手动触发或API调用
```

#### 批量处理示例
```bash
# 为所有问题生成SpinalHDL代码
bash build/Makefile.in sv-generate LANGUAGE=spinalhdl

# 分析结果
python3 count_failures.py results/
python3 pass_rate_to_csv.py --directory results/ --format detailed
```

## 📊 评估指标

### ✅ 成功标准
项目实现了全面的评估指标：

**语法正确率**：SpinalHDL到Verilog的转换成功，根据生成的spinalhdl2sv-summary.txt文件中执行成功次数除以总次数得到。

**功能通过率**：与测试平台的通过率，根据执行“make sv-iv-analyze”指令得到。


## 🔧 依赖项

### 核心依赖
- **Scala**: 2.13.14（生产级构建）
- **SpinalHDL**: 1.12.0（最新稳定版）
- **SBT**: 1.9.x+（Scala构建工具）
- **Python**: 3.8+与标准科学库
- **Java**: OpenJDK 11+（运行时兼容性）

### LLM集成依赖
- **langchain**: 高级LLM编排框架
- **langchain-openai**: OpenAI API集成
- **requests**: API交互HTTP客户端
- **pandas**: 数据分析和评估指标
- **tqdm**: 批量处理进度条

## 🌐 相关链接

- [英文版README](README.md) - 完整的英文文档
- [Verilog-Eval项目](https://github.com/NVlabs/verilog-eval) - 原始Verilog基准
- [SpinalHDL官方文档](https://spinalhdl.github.io/SpinalDoc-RTD/) - SpinalHDL文档
- [Context7 MCP](https://github.com/context7/mcp) - Context7 MCP协议