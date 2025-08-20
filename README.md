# SpinalHDL-Eval: LLM SpinalHDL Code Generation Capability Benchmark (based on Verilog-Eval)

>[**🇨🇳 Chinese README**](README_CN.md) | [**🇺🇸 English README**](README.md)

This project is a modified and enhanced version of the [Verilog-Eval](https://github.com/NVlabs/verilog-eval) benchmark framework , specifically designed to evaluate large language models' (LLMs) ability to generate SpinalHDL code. While Verilog-Eval focuses on Verilog RTL generation, this project extends it to SpinalHDL — a powerful Scala-based hardware description language that enables complex digital circuit design through advanced software engineering techniques.

The project inherits the 156 comprehensive design problems from Verilog-Eval and adapts them for SpinalHDL code generation, providing a systematic benchmark framework for evaluating model performance when using SpinalHDL's Scala-based HDL approach.

## 🚀 Project Overview

This project includes two core components:
1. SpinalHDL-Eval benchmark: a rigorous evaluation framework with 156 diverse hardware design problems
2. Context7 MCP enhancement framework: an n8n-based automated system for SpinalHDL code generation with LLMs

## 📂 Project Structure

```
.
├── build.sbt                 # SBT build configuration for Scala/SpinalHDL
├── Makefile.in               # Build configuration template
├── dataset_spec-to-spinalhdl # Dataset containing 156 design problems
├── hw/                       # Hardware source files directory
├── n8n/                      # Context7 MCP automation framework
│   └── SpinalHDL-Eval-MCP.json  # n8n workflow configuration
├── openrouter/               # OpenRouter LLM integration scripts
├── project/                  # SBT project configuration
├── scripts/                  # Advanced LLM integration and code generation scripts
└── README.md                 # English documentation (this file)
└── README_CN.md              # Chinese documentation
```

## 🔧 Core Components

### 1. Comprehensive Evaluation Dataset (`dataset_spec-to-spinalhdl/`)

The benchmark includes 156 diverse hardware design problems across multiple complexity levels and domains. Each problem contains:

- `_prompt.txt`: Detailed natural language specification describing the desired hardware functionality
- `_ref.sv`: Reference Verilog implementation for correctness verification
- `_test.sv`: Comprehensive testbench with validation scenarios

#### 🎯 Adaptations for SpinalHDL
To enable SpinalHDL code generation and evaluation, we systematically adapted the prompts, focusing on prompt design and adding the SpinalHDL-to-Verilog flow.

##### Prompt Adaptation

###### System Prompt Optimization
- Role alignment: Adjusted the LLM's role and output style to better fit SpinalHDL code generation
- Code template introduction: Added the following template structure, significantly improving the success rate of converting SpinalHDL code to Verilog later
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

###### Test Case Adaptation
- Keyword conflict resolution: Renamed the original Verilog-Eval testbench signals — input `in` to `din`, output `out` to `dout` — to avoid conflicts with SpinalHDL keywords
- Testbench synchronization: Updated the testbench signal names accordingly to ensure consistency

##### SpinalHDL to Verilog
See the next section for details

### 2. Code Generation Scripts (`scripts/`)

#### spinalhdl-to-sv script
Based on the official SpinalHDL 1.12.0 project [SpinalTemplateSbt](`https://github.com/SpinalHDL/SpinalTemplateSbt`).

##### Conversion Flow
1. Code preprocessing
   - Copy SpinalHDL code from the LLM output directory to a temporary `hw` directory
   - Add package name
   - Check whether the `TopMain` target exists

2. Code generation
   - Use SBT commands to generate Verilog code
   - Record execution status in real time

3. Result handling
   - Success: Rename and copy the generated Verilog code to the target directory
   - Failure: Proceed directly to the next conversion task

4. Batch processing
   - Iterate through all files to be converted
   - Collect and output a final summary of all conversion tasks

##### Environment Requirements
- SpinalHDL development environment
- SBT and Scala dependencies
- Java runtime environment

##### Notes
- Ensure the `TopMain` target is correctly defined in the code
- Verify the generated code's package configuration
- Temporary files are created during conversion; monitor disk space

### 3. Context7 MCP Framework (`n8n/`)

The Context7 MCP framework represents a breakthrough in automated hardware design, providing an n8n-based workflow for systematic SpinalHDL code generation using cutting-edge LLMs.

#### 🏗️ Architecture Overview
```
Workflow:
[Manual Trigger] → [File Processing] → [Context Enhancement] → [LLM Generation] → [Code Extraction] → [Output Management]
```

#### 🔑 Key Components (`SpinalHDL-Eval-MCP.json`)

**Input Processing**
- File reader: Sequentially processes all 156 prompt files
- Directory structure: Creates organized output directories (`output/ProbXXX_problem_name/`)
- Path resolution: Automatic handling of file paths and naming conventions

**LLM Enhancement**
- Context7 integration: Injects SpinalHDL documentation via the MCP protocol
- Prompt optimization: Automatically appends context7 tool hints to improve accuracy
- Model flexibility: Configurable for any OpenRouter-supported model

**Generation Pipeline**
- Parallel processing: Efficient batch generation across problems
- Error handling: Robust error recovery and retry mechanisms
- Format validation: Automatically extracts SpinalHDL code from LLM responses
- Logging: Comprehensive generation logs for debugging and analysis

**Output Management**
- Organized storage: Each problem has a dedicated directory with results
- Dual-format output:
  - `sample01.scala`: Generated SpinalHDL implementation
  - `log01.log`: Detailed generation log and metadata
- Batch summary: Aggregate results across all problems

## 🚀 Quick Start

### Environment Setup
```bash
# Set OpenRouter API key
export OPENROUTER_API_KEY="your-api-key"
```

### Manual Evaluation Examples

#### Generate code for a single problem
```bash
# Use a specified model to test a concrete problem
./scripts/sv-generate --model gpt-4o \
  --language spinalhdl \
  --task spec-to-rtl \
  --output generated.scala \
  dataset_spec-to-spinalhdl/Prob144_conwaylife_prompt.txt

# Use the default model to test all problems
cd build
make sv-generate LANGUAGE=spinalhdl
```

#### Compile the generated code
```bash
# Use the automatic conversion script
python3 ./scripts/spinalhdl-to-sv.py -s ./build -t hw -sbt .
```

### Test the generated Verilog code
```bash
cd build
make sv-iv-test
```

### Analyze the generated Verilog code
```bash
cd build
make sv-iv-analyze
```

### Context7 MCP Automated Evaluation

#### Workflow Setup
```bash
# 1. Install and start n8n (assumes Docker is installed)
docker run -it --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# 2. Load the workflow
n8n import:workflow --input=n8n/SpinalHDL-Eval-MCP.json

# 3. Configure credentials
# Visit http://localhost:5678 in your browser
# Configure: OpenRouter API key and Context7 MCP server

# 4. Run the evaluation
# Trigger manually or via API
```

#### Batch Processing Example
```bash
# Generate SpinalHDL code for all problems
bash build/Makefile.in sv-generate LANGUAGE=spinalhdl

# Analyze results
python3 count_failures.py results/
python3 pass_rate_to_csv.py --directory results/ --format detailed
```

## 📊 Evaluation Metrics

### ✅ Success Criteria
The project provides comprehensive evaluation metrics:

**Syntax correctness rate**: Success rate of SpinalHDL-to-Verilog conversion, calculated as the number of successful conversions divided by total attempts based on `spinalhdl2sv-summary.txt`.

**Functional pass rate**: Testbench pass rate obtained by running `make sv-iv-analyze`.

## 🔧 Dependencies

### Core Dependencies
- Scala: 2.13.14 (production-grade build)
- SpinalHDL: 1.12.0 (latest stable)
- SBT: 1.9.x+ (Scala build tool)
- Python: 3.8+ with standard scientific stack
- Java: OpenJDK 11+ (runtime compatibility)

### LLM Integration Dependencies
- langchain: Advanced LLM orchestration
- langchain-openai: OpenAI API integration
- requests: HTTP client for API interaction
- pandas: Data analysis and evaluation metrics
- tqdm: Progress bars for batch processing

## 🌐 Related Links

- [Chinese README](README_CN.md) — Full Chinese documentation
- [Verilog-Eval Project](https://github.com/NVlabs/verilog-eval) — Original Verilog benchmark
- [SpinalHDL Documentation](https://spinalhdl.github.io/SpinalDoc-RTD/) — Official SpinalHDL docs
- [Context7 MCP](https://github.com/context7/mcp) — Context7 MCP protocol