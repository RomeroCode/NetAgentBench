"""Tests for slice tools and tool registry."""
from netagentbench.agents.langgraph_agent import LangGraphAgent
from netagentbench.evaluation.benchmark import Benchmark
from netagentbench.scenarios.scenario import Scenario, ScenarioCategory, ToolCall
from netagentbench.tools.slice_tools import (
    SLICE_TOOLS,
    get_slice_tool_by_name,
    get_all_slice_tool_names,
)
from netagentbench.tools.tool_registry import ToolRegistry

def test_tool_registry():
    registry = ToolRegistry(SLICE_TOOLS)
    assert len(registry) == 12
    assert registry.has_tool("create_slice_state")


def test_slice_tools_count():
    assert len(SLICE_TOOLS) == 12


def test_get_slice_tool_by_name():
    tool = get_slice_tool_by_name("create_slice_state")
    assert tool["function"]["name"] == "create_slice_state"


def test_slice_tool_names_include_history():
    tool_names = get_all_slice_tool_names()
    assert "record_tool_call_history" in tool_names


def test_benchmark_uses_slice_tools_by_default():
    benchmark = Benchmark()
    assert len(benchmark.get_tools()) == len(SLICE_TOOLS)
    assert benchmark.tool_registry.has_tool("create_slice_state")


def test_langgraph_agent_generates_slice_tool_call():
    scenario = Scenario(
        id="slice_create_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Create a new slice for tenant alpha",
        context={"slice_id": "slice-alpha", "tenant_id": "tenant-alpha"},
        expected_tools=[ToolCall(tool_name="create_slice_state", parameters={})],
    )
    agent = LangGraphAgent()
    tool_calls = agent.process_scenario(scenario, SLICE_TOOLS)

    assert len(tool_calls) == 1
    assert tool_calls[0]["tool_name"] == "create_slice_state"
