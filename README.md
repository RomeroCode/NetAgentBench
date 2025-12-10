# NetAgentBench

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**NetAgentBench** is a specialized benchmark for evaluating AI Agents and Large Language Models (LLMs) in Intent-Based Networking (IBN) and Tool Calling scenarios for network automation.

## 🎯 Overview

NetAgentBench provides a comprehensive framework to assess the capability of AI systems to:

1. **Interpret Network Management Intentions**: Understanding natural language network management requests (Intent-Based Networking)
2. **Orchestrate Tool Calls**: Selecting and executing the correct network automation tools (Function Calling)
3. **Perform Multi-Step Reasoning**: Breaking down complex network tasks into sequential operations

## 🚀 Features

- **Comprehensive Scenario Dataset**: 10+ realistic network automation scenarios across 5 categories
- **Network Tool Library**: 15+ pre-defined network automation tools compatible with OpenAI function calling format
- **Flexible Evaluation Framework**: Support for both strict and lenient evaluation modes
- **Rich Metrics**: Accuracy, Precision, Recall, F1-Score, and detailed error analysis
- **Easy Integration**: Simple interface for evaluating custom agents and LLMs
- **Pure Python**: No external dependencies required for core functionality

## 📦 Installation

### From Source

```bash
git clone https://github.com/RomeroCode/NetAgentBench.git
cd NetAgentBench
pip install -e .
```

### For Development

```bash
pip install -e ".[dev]"
```

## 🏃 Quick Start

### Basic Usage

```python
from netagentbench import Benchmark
from netagentbench.scenarios import Scenario
from pathlib import Path

# Initialize benchmark
benchmark = Benchmark()

# Load pre-built dataset
benchmark.load_dataset(Path("data/scenarios.json"))

# Define your agent runner function
def my_agent_runner(scenario: Scenario, tools: list) -> list:
    """
    Your agent implementation here.
    Returns list of tool calls: [{"tool_name": str, "parameters": dict}, ...]
    """
    # Agent logic to process scenario and select tools
    return tool_calls

# Run evaluation
results = benchmark.run_evaluation(
    agent_runner=my_agent_runner,
    difficulty_range=(1, 3)
)

# View metrics
print(f"Accuracy: {results['metrics']['accuracy']:.2%}")
print(f"F1 Score: {results['metrics']['f1_score']:.2%}")
```

### Running the Example

```bash
python examples/evaluate_agent.py
```

## 📊 Scenario Categories

NetAgentBench includes scenarios across five key categories:

| Category | Description | Example Scenarios |
|----------|-------------|-------------------|
| **Configuration** | Network device setup and configuration | Interface configuration, VLAN setup, routing |
| **Troubleshooting** | Diagnosing and resolving network issues | Connectivity tests, path analysis |
| **Monitoring** | Network performance and status monitoring | Bandwidth monitoring, interface status |
| **Security** | Security policies and access control | ACL configuration, firewall rules |
| **Optimization** | Network performance optimization | QoS policies, traffic prioritization |

## 🛠️ Available Network Tools

NetAgentBench provides 15+ network automation tools:

- **Configuration**: `configure_interface`, `configure_vlan`, `configure_routing`, `configure_acl`, `configure_qos`, `configure_snmp`
- **Diagnostics**: `ping_test`, `traceroute`, `get_device_info`, `get_interface_status`
- **Monitoring**: `monitor_bandwidth`, `get_routing_table`, `get_arp_table`
- **Management**: `backup_configuration`, `restore_configuration`

All tools follow the OpenAI function calling format and include detailed parameter specifications.

## 📈 Evaluation Metrics

NetAgentBench provides comprehensive metrics:

- **Accuracy**: Percentage of scenarios completed successfully
- **Tool Call Accuracy**: Percentage of scenarios with correct tool selections
- **Precision**: Ratio of correct tool calls to total tool calls made
- **Recall**: Ratio of correct tool calls to expected tool calls
- **F1 Score**: Harmonic mean of precision and recall
- **Error Analysis**: Detailed breakdown of error types

## 🔧 Creating Custom Scenarios

```python
from netagentbench.scenarios import Scenario, ScenarioCategory, ToolCall

scenario = Scenario(
    id="custom_001",
    category=ScenarioCategory.CONFIGURATION,
    intent="Configure interface GigabitEthernet0/1 with IP 10.0.0.1/24",
    context={
        "device_id": "R1",
        "device_type": "router"
    },
    expected_tools=[
        ToolCall(
            tool_name="configure_interface",
            parameters={
                "device_id": "R1",
                "interface_name": "GigabitEthernet0/1",
                "ip_address": "10.0.0.1",
                "subnet_mask": "255.255.255.0",
                "enabled": True
            }
        )
    ],
    difficulty=2,
    requires_reasoning=False
)
```

## 🤖 Implementing Custom Agents

```python
from netagentbench.agents import AgentInterface
from netagentbench.scenarios import Scenario

class MyAgent(AgentInterface):
    def process_scenario(self, scenario: Scenario, available_tools: list) -> list:
        # Your LLM/agent logic here
        # Parse scenario.intent and scenario.context
        # Select appropriate tools from available_tools
        # Return tool calls
        return [
            {
                "tool_name": "configure_interface",
                "parameters": {...}
            }
        ]
    
    def get_reasoning_steps(self) -> list:
        return ["Step 1: ...", "Step 2: ..."]
```

## 📁 Project Structure

```
NetAgentBench/
├── netagentbench/          # Main package
│   ├── scenarios/          # Scenario definitions and dataset
│   ├── evaluation/         # Evaluation framework and metrics
│   ├── tools/              # Network tool definitions
│   ├── agents/             # Agent interfaces and base classes
│   └── utils/              # Utility functions
├── data/                   # Pre-built datasets
│   └── scenarios.json      # Example scenario dataset
├── examples/               # Example scripts
│   └── evaluate_agent.py   # Example evaluation script
├── setup.py               # Package setup
└── requirements.txt       # Dependencies
```

## 📝 Dataset Statistics

The default dataset includes:
- **Total Scenarios**: 10
- **Difficulty Distribution**: 
  - Level 1: 2 scenarios
  - Level 2: 5 scenarios  
  - Level 3: 3 scenarios
- **Reasoning Required**: 5 scenarios
- **Categories**: Configuration (5), Troubleshooting (2), Monitoring (1), Security (1), Optimization (1)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas for contribution:

- Additional network automation scenarios
- New tool definitions
- Enhanced evaluation metrics
- Integration with popular LLM frameworks
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use NetAgentBench in your research, please cite:

```bibtex
@software{netagentbench2025,
  title={NetAgentBench: A Benchmark for Evaluating AI Agents in Intent-Based Network Automation},
  author={RomeroCode},
  year={2025},
  url={https://github.com/RomeroCode/NetAgentBench}
}
```

## 🔗 Related Projects

- [ToolBench](https://github.com/OpenBMB/ToolBench) - General tool learning benchmark
- [AgentBench](https://github.com/THUDM/AgentBench) - Multi-dimensional agent evaluation
- [Intent-Based Networking](https://en.wikipedia.org/wiki/Intent-based_networking) - IBN concepts

## ⭐ Star History

If you find NetAgentBench useful, please consider giving it a star! ⭐
