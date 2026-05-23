"""Tests for network tools and tool registry."""
import pytest
from netagentbench.tools.network_tools import NETWORK_TOOLS, get_tool_by_name, get_all_tool_names
from netagentbench.tools.slice_tools import (
    SLICE_TOOLS,
    get_slice_tool_by_name,
    get_all_slice_tool_names,
)
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


def test_slice_tools_count():
    assert len(SLICE_TOOLS) == 12


def test_get_slice_tool_by_name():
    tool = get_slice_tool_by_name("create_slice_state")
    assert tool["function"]["name"] == "create_slice_state"


def test_slice_tool_names_include_history():
    tool_names = get_all_slice_tool_names()
    assert "record_tool_call_history" in tool_names
