# SpinalHDL-Eval: Large Language Model SpinalHDL Code Generation Evaluation Benchmark

>This is a **modified and enhanced version** of the **Verilog-Eval benchmark framework(https://github.com/NVlabs/verilog-eval)**, specifically adapted to evaluate SpinalHDL code generation capabilities of large language models (LLMs). While Verilog-Eval focuses on Verilog RTL generation, this project extends the evaluation to SpinalHDL - a powerful hardware description language embedded in Scala that enables sophisticated digital circuit design through advanced software engineering techniques.

[**🇨🇳 中文文档**](README_CN.md) | [**🇺🇸 English README**](README.md)

Originally based on Verilog-Eval benchmark, this project maintains the same 156 comprehensive design problems but adapts them for SpinalHDL code generation, providing a systematic evaluation framework for assessing LLM performance in generating hardware designs using SpinalHDL's Scala-based HDL approach.

## Project Structure

```
.
├── build.sbt                 # SBT build configuration for Scala/SpinalHDL
├── Makefile.in               # Build configuration template
├── dataset_spec-to-spinalhdl # Comprehensive dataset with 156 design problems
├── hw/                       # Hardware source files directory
├── n8n/                      # Context7 MCP automation framework
│   └── SpinalHDL-Eval-MCP.json  # n8n workflow for automated SpinalHDL generation
├── openrouter/               # OpenRouter LLM integration scripts
├── project/                  # SBT project configuration
├── scripts/                  # Advanced LLM integration and code generation scripts
└── README.md                 # This file
```

## Key Components

### 1. Comprehensive Evaluation Dataset (`dataset_spec-to-spinalhdl/`)
The benchmark features a rich dataset of **156 diverse hardware design problems** spanning across multiple complexity levels and application domains. Each problem includes:

- **`_prompt.txt`**: Detailed natural language specification describing the desired hardware functionality
- **`_ref.sv`**: Reference Verilog implementation for correctness verification  
- **`_test.sv`**: Comprehensive testbench with validation scenarios

#### Design Categories
The problems cover a wide spectrum of digital design concepts:

**🔢 Basic Logic (Problems 001-030)**
- Simple gates (AND, OR, NOT, XOR implementations)
- Multiplexers and demultiplexers  
- Basic arithmetic circuits
- Signal routing and buffering

**⚙️ Sequential Circuits (Problems 031-060)**  
- Flip-flops and registers (DFF, TFF, JKFF)
- Counters (up/down, BCD, Johnson)
- Shift registers and barrel shifters
- Edge detection circuits

**🧮 Advanced Arithmetic (Problems 061-090)**
- ALU designs and arithmetic units
- Multipliers and dividers
- Adders and subtractors with various architectures
- Digital filters and signal processing

**🔄 State Machines (Problems 091-120)**
- Finite state machines (FSM) - Moore and Mealy types
- Protocol implementers (PS2, HDLC, serial communication)
- Traffic light controllers and sequence detectors
- One-hot encoded FSMs

**🔬 Complex Systems (Problems 121-156)**
- Conway's Game of Life cellular automaton
- Rule 90/110 cellular automata
- Linear feedback shift registers (LFSR)
- G-share branch predictors
- Historical sequence tracking systems

#### Problem Naming Convention
Problems are systematically numbered (Prob001 through Prob156) with descriptive names:
- `Prob001_zero`: Simple signal assignment
- `Prob018_mux256to1`: 256-to-1 multiplexer  
- `Prob144_conwaylife`: Conway's Game of Life implementation
- `Prob079_fsm3onehot`: FSM with one-hot encoding

### 2. Code Generation Scripts (`scripts/`)
Advanced LLM integration tools with comprehensive model support:

#### Core Generation Tool (`sv-generate`)
A sophisticated Python-based LLM integration tool supporting:

**🤖 Model Support**
- **OpenAI**: GPT-3.5-turbo, GPT-4, GPT-4-turbo, GPT-4o
- **NVIDIA NIM**: Llama-3.1 series (8B, 70B, 405B), CodeLlama, Mistral models
- **OpenRouter**: DeepSeek, Qwen, Gemini, Claude, and free-tier models

**⚙️ Task Types**
- `spec-to-spinalhdl`: **Direct SpinalHDL generation** from natural language

**🛠️ Advanced Features**
- Temperature control (0.1-1.0) for deterministic vs creative generation
- Few-shot learning with 1-4 contextual examples
- Repeat generation with error analysis
- Verbose debugging mode for detailed inspection

- `spinalhdl-to-sv.py`: Automated SpinalHDL to Verilog compilation   
- `count_failures.py`: Comprehensive evaluation metrics
- `pass_rate_to_csv.py`: CSV report generation

### 3. Context7 MCP Framework (`n8n/`)
The **Context7 MCP Framework** represents a breakthrough in automated hardware design generation, providing an n8n-based workflow for systematic SpinalHDL code generation using cutting-edge LLMs.

#### Architecture Overview
```
Workflow Process:
[Manual Trigger] → [File Processing] → [Context Enhancement] → [LLM Generation] → [Code Extraction] → [Output Management]
```

#### Key Components (`SpinalHDL-Eval-MCP.json`)

**🔍 Input Processing**
- **File Reader**: Processes all 156 prompt files sequentially
- **Directory Structure**: Creates organized output directories (`output/ProbXXX_problem_name/`)
- **Path Resolution**: Automatic handling of file paths and naming conventions

**🧠 LLM Enhancement**
- **Context7 Integration**: Injects SpinalHDL documentation via MCP protocol
- **Prompt Optimization**: Automatically appends context7 tool hints for improved accuracy
- **Model Flexibility**: Configurable for any OpenRouter-supported model

**⚡ Generation Pipeline**
- **Parallel Processing**: Efficient batch generation across problems
- **Error Handling**: Robust error recovery and retry mechanisms
- **Format Validation**: Automatic extraction of SpinalHDL code from LLM responses
- **Logging**: Comprehensive generation logs for debugging and analysis

**📂 Output Management**
- **Organized Storage**: Each problem gets dedicated directory with results
- **Dual Format Output**: 
  - `sample01.scala`: Generated SpinalHDL implementation
  - `log01.log`: Detailed generation log and metadata
- **Batch Summary**: Aggregate results across all problems

#### Usage Workflow
```bash
# Load workflow into n8n
n8n import:workflow --input=n8n/SpinalHDL-Eval-MCP.json

# Configure credentials
# 1. OpenRouter API key integration
# 2. Context7 MCP server setup
# 3. Docker volume mapping for file access

# Execute comprehensive evaluation
# Workflow runs automatically processing all 156 problems
```

### 3. Build System
The project uses SBT (Scala Build Tool) for managing the SpinalHDL compilation process:
- `build.sbt`: Defines project dependencies and settings
- Uses SpinalHDL version 1.12.0

## Workflow

1. **Specification**: Natural language problem descriptions are stored in the dataset directory.

2. **Code Generation**: The `sv-generate` script prompts an LLM to generate SpinalHDL code from the natural language specification.

3. **Compilation**: Generated SpinalHDL code is compiled to Verilog using the SpinalHDL compiler via the `spinalhdl-to-sv.py` script.

4. **Testing**: Generated Verilog is tested against reference implementations using the provided testbenches.

## Usage

### Prepare the environment
```bash
# set OpenRouter API key
export OPENROUTER_API_KEY="your-api-key"
```

### Generating SpinalHDL Code
```bash
# Generate SpinalHDL code for a specific problem using an LLM
./scripts/sv-generate --model gpt-4 --language spinalhdl \
  --task spec-to-rtl \
  --output generated.scala \
  dataset_spec-to-spinalhdl/Prob001_zero_prompt.txt

# Generate SpinalHDL code for all problem using an LLM
cd build
make sv-generate LANGUAGE=spinalhdl

```

### Converting SpinalHDL to Verilog
```bash
# Convert generated SpinalHDL to Verilog
python3 ./scripts/spinalhdl-to-sv.py -s ./build -t hw -sbt .
```

### Test the Verilog code
```bash
cd build
make sv-iv-test
```

### Analyze the Verilog code
```bash
cd build
make sv-iv-analyze
```

### Building with SBT
```bash
# Compile SpinalHDL code to Verilog
sbt "runMain <package>.<module>.TopMain"
```

## Dependencies

- Scala 2.13.14
- SpinalHDL 1.12.0
- Python 3.x with required packages (requests, tqdm)
- SBT (Scala Build Tool)

## Model Support

The project supports various LLMs through different APIs:

- OpenAI models (gpt-3.5-turbo, gpt-4, etc.)
- NVIDIA NIM models (Llama, CodeLlama, Mistral, etc.)
- OpenRouter models (including DeepSeek, Qwen, Gemini, Claude, etc.)

## Evaluation Metrics

The project includes scripts for analyzing the success rate of code generation:
- `count_failures.py`: Counts failed generations
- `pass_rate_to_csv.py`: Calculates and exports pass rates to CSV

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.