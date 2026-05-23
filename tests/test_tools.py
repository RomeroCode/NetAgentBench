"""Tests for slice tools and tool registry."""
from unittest.mock import Mock, patch

import langsmith.run_helpers as run_helpers

from netagentbench.agents.langgraph_agent import LangGraphAgent
from netagentbench.evaluation.benchmark import Benchmark
from netagentbench.scenarios.scenario import Scenario, ScenarioCategory, ToolCall
from netagentbench.tools.slice_tools import (
    SLICE_TOOLS,
    call_slice_tool_api,
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


def test_call_slice_tool_api_with_post_payload():
    mock_api = Mock()
    mock_api.post.return_value = {"status": "ok"}
    payload = {
        "slice_id": "slice-alpha",
        "tenant_id": "tenant-alpha",
        "lifecycle_state": "CREATED",
    }

    response = call_slice_tool_api("create_slice_state", payload, mock_api)

    mock_api.post.assert_called_once_with("/slice_state", json=payload)
    assert response == {"status": "ok"}


def test_call_slice_tool_api_with_get_params():
    mock_api = Mock()
    mock_api.get.return_value = {"slice_id": "slice-alpha"}
    payload = {"slice_id": "slice-alpha"}

    response = call_slice_tool_api("get_slice_state", payload, mock_api)

    mock_api.get.assert_called_once_with("/slice_state", params=payload)
    assert response["slice_id"] == "slice-alpha"


def test_langsmith_is_invoked_with_mocked_slice_api_flow():
    scenario = Scenario(
        id="slice_create_trace_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Create a new slice for tenant alpha",
        context={"slice_id": "slice-alpha", "tenant_id": "tenant-alpha"},
        expected_tools=[ToolCall(tool_name="create_slice_state", parameters={})],
    )
    agent = LangGraphAgent()
    mock_api = Mock()
    mock_api.post.return_value = {"status": "ok"}

    with patch("langsmith.run_helpers._setup_run", wraps=run_helpers._setup_run) as setup_run:
        tool_calls = agent.process_scenario(scenario, SLICE_TOOLS)

    assert setup_run.call_count >= 1
    assert tool_calls[0]["tool_name"] == "create_slice_state"
    response = call_slice_tool_api(
        "create_slice_state",
        tool_calls[0]["parameters"],
        mock_api,
    )
    mock_api.post.assert_called_once()
    assert response == {"status": "ok"}
