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

#### 🎯 设计问题分类

**🔢 基础逻辑电路（001-030题）**
- 简单门电路（与、或、非、异或实现）
- 多路选择器和解码器
- 基础算术电路
- 信号路由和缓冲

**⚙️ 时序电路（031-060题）**  
- 触发器和寄存器（D触发器、T触发器、JK触发器）
- 计数器（递增、递减、BCD、Johnson计数器）
- 移位寄存器和桶形移位器
- 边沿检测电路

**🧮 高级算术电路（061-090题）**
- ALU设计和算术单元
- 乘法和除法电路
- 不同架构的加法和减法器
- 数字滤波器和信号处理

**🔄 状态机（091-120题）**
- 有限状态机（FSM）- Moore和Mealy类型
- 协议实现器（PS2、HDLC、串行通信）
- 交通灯控制器和序列检测器
- 单热编码FSM

**🔬 复杂系统（121-156题）**
- Conway生命游戏元胞自动机
- 规则90/110元胞自动机
- 线性反馈移位寄存器（LFSR）
- G-share分支预测器
- 历史序列跟踪系统

#### 📋 问题命名规范

问题按Prob001至Prob156有序编号，具有描述性名称：
- `Prob001_zero`：简单信号赋值
- `Prob018_mux256to1`：256选1多路选择器
- `Prob144_conwaylife`：Conway生命游戏实现
- `Prob079_fsm3onehot`：单热编码FSM

### 2. 代码生成脚本 (`scripts/`)

#### 核心生成工具 (`sv-generate`)
复杂Python语言的LLM集成工具，支持：

**🤖 模型支持**
- **OpenAI**：GPT-3.5-turbo、GPT-4、GPT-4-turbo、GPT-4o
- **NVIDIA NIM**：Llama-3.1系列（8B、70B、405B）、CodeLlama、Mistral模型
- **OpenRouter**：DeepSeek、Qwen、Gemini、Claude及免费套餐模型

**⚙️ 任务类型**
- `spec-to-spinalhdl`：**直接SpinalHDL生成**从自然语言

**🛠️ 高级特性**
- 温度控制（0.1-1.0）用于确定性与创造性生成
- 1-4个情境样本的少量学习
- 重复生成和错误分析
- 详细检查的调试模式

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
# 使用高性能模型
./scripts/sv-generate --model gpt-4o \
  --language spinalhdl \
  --task spec-to-rtl \
  --output generated.scala \
  dataset_spec-to-spinalhdl/Prob144_conwaylife_prompt.txt

# 使用免费模型
./scripts/sv-generate --model deepseek/deepseek-chat-v3-0324:free \
  --language spinalhdl \
  --task spec-to-rtl \
  dataset_spec-to-spinalhdl/Prob001_zero_prompt.txt

# 使用带调试的详细模式
./scripts/sv-generate --verbose --temperature 0.7 --examples 2 \
  dataset_spec-to-spinalhdl/Prob079_fsm3onehot_prompt.txt
```

#### 编译生成的代码
```bash
# 使用SBT编译SpinalHDL到Verilog
sbt "runMain TopMain"

# 或使用自动转换脚本
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

**语法正确率**：SpinalHDL到Verilog的转换成功
**功能通过率**：与测试平台的通过率


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

## 🤝 参与贡献

### 开发设置
```bash
# 克隆仓库
git clone https://github.com/your-repo/SpinalHDL-Eval.git
cd SpinalHDL-Eval

# 安装依赖
pip3 install -r requirements.txt
sbt compile

# 运行初始测试
./scripts/sv-generate --list-models
```

### 故障排除
```bash
# 启用调试模式
./scripts/sv-generate --verbose --temperature 0.1 \
  dataset_spec-to-spinalhdl/Prob001_zero_prompt.txt

# 检查文件权限
chmod +x scripts/sv-generate
chmod +x scripts/spinalhdl-to-sv.py
```

## 📜 许可证和致谢

本项目基于以下项目构建而来：
- **Verilog-Eval**: NVIDIA的RTL评估基准
- **SpinalHDL**: 先进的硬件描述语言
- **Context7**: LLM知识增强MCP协议
- **OpenRouter**: 统一LLM API访问

**许可证**: MIT许可证 - 详见LICENSE文件

## 🌐 相关链接

- [英文版README](README.md) - 完整的英文文档
- [Verilog-Eval项目](https://github.com/NVlabs/verilog-eval) - 原始Verilog基准
- [SpinalHDL官方文档](https://spinalhdl.github.io/SpinalDoc-RTD/) - SpinalHDL文档
- [Context7 MCP](https://github.com/context7/mcp) - Context7 MCP协议