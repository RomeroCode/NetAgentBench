# Contributing to NetAgentBench

Thank you for your interest in contributing to NetAgentBench! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/NetAgentBench.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
5. Install development dependencies: `pip install -e ".[dev]"`

## Development Workflow

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest tests/`
4. Run linters (if configured): `black netagentbench/` and `flake8 netagentbench/`
5. Commit your changes: `git commit -m "Description of changes"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Types of Contributions

### Adding New Scenarios

We welcome contributions of new network automation scenarios! To add scenarios:

1. Create scenarios following the existing format in `netagentbench/scenarios/examples.py`
2. Ensure scenarios cover realistic network automation use cases
3. Include proper categorization (Configuration, Troubleshooting, Monitoring, Security, Optimization)
4. Set appropriate difficulty levels (1-5)
5. Add comprehensive context information

Example:
```python
Scenario(
    id="custom_001",
    category=ScenarioCategory.CONFIGURATION,
    intent="Your network management intent here",
    context={"device_id": "R1", "additional": "context"},
    expected_tools=[
        ToolCall(
            tool_name="tool_name",
            parameters={"param": "value"}
        )
    ],
    difficulty=2,
    requires_reasoning=False
)
```

### Adding New Tools

To add new network automation tools:

1. Add tool definitions to `netagentbench/tools/network_tools.py`
2. Follow the OpenAI function calling format
3. Include comprehensive parameter descriptions
4. Document required vs optional parameters

Example:
```python
{
    "type": "function",
    "function": {
        "name": "your_tool_name",
        "description": "Clear description of what the tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param1"]
        }
    }
}
```

### Improving Evaluation Metrics

Suggestions for new evaluation metrics are welcome! Consider:

- Tool selection accuracy
- Parameter correctness
- Multi-step reasoning evaluation
- Error categorization
- Performance metrics

### Documentation

Documentation improvements are always appreciated:

- Fix typos or unclear explanations
- Add examples and use cases
- Improve API documentation
- Add tutorials or guides

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and modular

## Testing

- Write tests for all new features
- Ensure all existing tests pass
- Aim for high code coverage
- Test edge cases and error conditions

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include tests for new functionality
- Update documentation as needed
- Keep pull requests focused on a single feature or fix

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

## Questions?

If you have questions or need help, feel free to:

- Open an issue for discussion
- Ask in pull request comments
- Reach out to maintainers

Thank you for contributing to NetAgentBench!
