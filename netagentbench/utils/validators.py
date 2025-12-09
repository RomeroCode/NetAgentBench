"""
Validators for NetAgentBench components.
"""

from __future__ import annotations
from typing import Dict, Any, List
from netagentbench.scenarios.scenario import Scenario


def validate_tool_call(tool_call: Dict[str, Any]) -> bool:
    """
    Validate that a tool call has the required structure.
    
    Args:
        tool_call: Tool call dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(tool_call, dict):
        return False
    
    if "tool_name" not in tool_call:
        return False
    
    if "parameters" not in tool_call:
        return False
    
    if not isinstance(tool_call["parameters"], dict):
        return False
    
    return True


def validate_tool_calls(tool_calls: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
    """
    Validate a list of tool calls.
    
    Args:
        tool_calls: List of tool calls to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    if not isinstance(tool_calls, list):
        return False, ["Tool calls must be a list"]
    
    errors = []
    for i, tool_call in enumerate(tool_calls):
        if not validate_tool_call(tool_call):
            errors.append(f"Tool call at index {i} is invalid")
    
    return len(errors) == 0, errors


def validate_scenario(scenario: Scenario) -> tuple[bool, List[str]]:
    """
    Validate a scenario.
    
    Args:
        scenario: Scenario to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    try:
        # This will raise ValueError if validation fails
        scenario.__post_init__()
    except ValueError as e:
        errors.append(str(e))
    
    # Check expected tools
    for i, tool in enumerate(scenario.expected_tools):
        if not tool.tool_name:
            errors.append(f"Expected tool at index {i} has empty tool_name")
        if not isinstance(tool.parameters, dict):
            errors.append(f"Expected tool at index {i} has invalid parameters")
    
    return len(errors) == 0, errors


def validate_agent_response(
    response: List[Dict[str, Any]],
    available_tools: List[Dict[str, Any]]
) -> tuple[bool, List[str]]:
    """
    Validate that an agent's response uses only available tools.
    
    Args:
        response: Agent's tool calls
        available_tools: List of available tool definitions
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    # First validate structure
    is_valid, errors = validate_tool_calls(response)
    if not is_valid:
        return False, errors
    
    # Get available tool names
    available_names = {tool["function"]["name"] for tool in available_tools}
    
    # Check if all tools in response are available
    for tool_call in response:
        if tool_call["tool_name"] not in available_names:
            errors.append(
                f"Tool '{tool_call['tool_name']}' is not in available tools"
            )
    
    return len(errors) == 0, errors
