# Changelog

All notable changes to NetAgentBench will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-09

### Added
- Initial release of NetAgentBench
- Core evaluation framework for AI agents in network automation
- 10 example network automation scenarios across 5 categories:
  - Configuration (5 scenarios)
  - Troubleshooting (2 scenarios)
  - Monitoring (1 scenario)
  - Security (1 scenario)
  - Optimization (1 scenario)
- 15 network automation tools compatible with OpenAI function calling format:
  - Interface configuration
  - VLAN management
  - Routing configuration
  - ACL/firewall rules
  - QoS policies
  - SNMP monitoring
  - Backup/restore
  - Diagnostic tools (ping, traceroute)
  - Network information queries
- Comprehensive evaluation metrics:
  - Accuracy
  - Precision and Recall
  - F1 Score
  - Error analysis
- Scenario dataset management with filtering and statistics
- Agent interface for implementing custom agents
- Example evaluation script with rule-based agent
- Full test suite with 21+ tests
- Comprehensive documentation and README
- MIT License

### Features
- Pure Python implementation with no external dependencies for core functionality
- Support for both strict and lenient evaluation modes
- Flexible scenario filtering by category, difficulty, and reasoning requirements
- JSON-based dataset storage and loading
- Detailed evaluation results and metrics export
- Extensible tool registry system
- Agent interface for easy integration with LLMs

[0.1.0]: https://github.com/RomeroCode/NetAgentBench/releases/tag/v0.1.0
