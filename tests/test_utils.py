"""Tests for utility functions."""
import pytest
from netagentbench.utils.validators import validate_tool_call

def test_validate_tool_call():
    valid_call = {"tool_name": "test", "parameters": {}}
    assert validate_tool_call(valid_call) is True
    
    invalid_call = {"parameters": {}}
    assert validate_tool_call(invalid_call) is False
