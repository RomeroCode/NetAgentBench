"""Tests for network tools and tool registry."""
import pytest
from netagentbench.tools.network_tools import NETWORK_TOOLS, get_tool_by_name, get_all_tool_names
from netagentbench.tools.tool_registry import ToolRegistry

def test_network_tools_count():
    assert len(NETWORK_TOOLS) == 15

def test_get_tool_by_name():
    tool = get_tool_by_name("configure_interface")
    assert tool["function"]["name"] == "configure_interface"

def test_tool_registry():
    registry = ToolRegistry(NETWORK_TOOLS)
    assert len(registry) == 15
    assert registry.has_tool("configure_interface")
