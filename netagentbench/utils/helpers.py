"""
Helper utilities for NetAgentBench.
"""

import json
from pathlib import Path
from typing import Any, Dict


def load_json(filepath: Path) -> Dict[str, Any]:
    """
    Load data from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Loaded data as dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filepath: Path to save to
        indent: Indentation level for formatting
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def format_tool_call(tool_name: str, parameters: Dict[str, Any]) -> str:
    """
    Format a tool call as a human-readable string.
    
    Args:
        tool_name: Name of the tool
        parameters: Tool parameters
        
    Returns:
        Formatted string
    """
    params_str = ", ".join(f"{k}={v}" for k, v in parameters.items())
    return f"{tool_name}({params_str})"


def compare_parameters(
    params1: Dict[str, Any],
    params2: Dict[str, Any],
    strict: bool = False
) -> bool:
    """
    Compare two parameter dictionaries.
    
    Args:
        params1: First parameters dict
        params2: Second parameters dict
        strict: If True, require exact match. If False, check subset.
        
    Returns:
        True if parameters match according to strictness level
    """
    if strict:
        return params1 == params2
    
    # Check if all keys in params2 exist in params1 with same values
    for key, value in params2.items():
        if key not in params1:
            return False
        if params1[key] != value:
            return False
    
    return True
