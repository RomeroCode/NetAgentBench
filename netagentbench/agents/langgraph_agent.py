"""
LangGraph-based agent implementation with optional LangSmith tracing.
"""

from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph
from langsmith import traceable

from netagentbench.agents.base_agent import BaseAgent
from netagentbench.scenarios.scenario import Scenario


class AgentState(TypedDict):
    """State flowing through the LangGraph workflow."""

    scenario: Scenario
    available_tools: List[Dict[str, Any]]
    intent: str
    context: Dict[str, Any]
    tool_calls: List[Dict[str, Any]]
    reasoning_steps: List[str]


class LangGraphAgent(BaseAgent):
    """
    Agent implementation powered by a simple LangGraph workflow.
    """

    def __init__(self, name: str = "LangGraphAgent"):
        super().__init__(name=name)
        self._graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("analyze_intent", self._analyze_intent)
        graph.add_node("generate_tool_calls", self._generate_tool_calls)
        graph.add_edge(START, "analyze_intent")
        graph.add_edge("analyze_intent", "generate_tool_calls")
        graph.add_edge("generate_tool_calls", END)
        return graph.compile()

    @traceable(name="netagentbench_analyze_intent", run_type="chain")
    def _analyze_intent(self, state: AgentState) -> Dict[str, Any]:
        scenario = state["scenario"]
        intent = scenario.intent.lower()
        context = scenario.context
        reasoning_steps = [
            f"Analyzing intent: {scenario.intent}",
            f"Available context: {list(context.keys())}",
        ]
        return {
            "intent": intent,
            "context": context,
            "reasoning_steps": reasoning_steps,
        }

    @traceable(name="netagentbench_generate_tool_calls", run_type="chain")
    def _generate_tool_calls(self, state: AgentState) -> Dict[str, Any]:
        intent = state["intent"]
        context = state["context"]
        available_tools = state["available_tools"]
        reasoning_steps = list(state["reasoning_steps"])
        tool_calls: List[Dict[str, Any]] = []

        available_tool_names = set(self.extract_tool_names(available_tools))

        slice_id = context.get("slice_id", "slice-001")
        tenant_id = context.get("tenant_id", "tenant-001")

        if "create" in intent and "slice" in intent:
            reasoning_steps.append("Detected slice creation intent")
            if "create_slice_state" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "create_slice_state",
                        "parameters": {
                            "slice_id": slice_id,
                            "tenant_id": tenant_id,
                            "lifecycle_state": "CREATED",
                        },
                    }
                )
        elif "configure" in intent and "slice" in intent:
            reasoning_steps.append("Detected slice configuration intent")
            if "upsert_slice_configuration_state" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "upsert_slice_configuration_state",
                        "parameters": {
                            "slice_id": slice_id,
                            "configured_nfs": context.get("configured_nfs", []),
                            "policies_applied": context.get("policies_applied", False),
                            "last_config_status": context.get(
                                "last_config_status", "SUCCESS"
                            ),
                        },
                    }
                )
            if "update_slice_lifecycle_state" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "update_slice_lifecycle_state",
                        "parameters": {
                            "slice_id": slice_id,
                            "lifecycle_state": "CONFIGURED",
                        },
                    }
                )
        elif ("activate" in intent or "active" in intent) and "slice" in intent:
            reasoning_steps.append("Detected slice activation intent")
            if "update_slice_lifecycle_state" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "update_slice_lifecycle_state",
                        "parameters": {
                            "slice_id": slice_id,
                            "lifecycle_state": "ACTIVE",
                        },
                    }
                )
        elif "verify" in intent or "verification" in intent:
            reasoning_steps.append("Detected slice verification intent")
            if "upsert_slice_verification_state" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "upsert_slice_verification_state",
                        "parameters": {
                            "slice_id": slice_id,
                            "verification_result": context.get(
                                "verification_result", "OK"
                            ),
                            "issues": context.get("issues", []),
                        },
                    }
                )
        elif "usage" in intent or "traffic" in intent or "ue" in intent:
            reasoning_steps.append("Detected slice usage intent")
            if "upsert_slice_usage_state" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "upsert_slice_usage_state",
                        "parameters": {
                            "slice_id": slice_id,
                            "active_ues": context.get("active_ues", []),
                            "traffic_present": context.get("traffic_present", False),
                            "avg_latency_ms": context.get("avg_latency_ms"),
                            "avg_throughput_mbps": context.get("avg_throughput_mbps"),
                        },
                    }
                )
        elif "history" in intent or "audit" in intent:
            reasoning_steps.append("Detected tool call history intent")
            if "list_tool_call_history" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "list_tool_call_history",
                        "parameters": {
                            "slice_id": slice_id,
                            "limit": context.get("limit", 50),
                        },
                    }
                )

        reasoning_steps.append(f"Generated {len(tool_calls)} tool calls")
        return {"tool_calls": tool_calls, "reasoning_steps": reasoning_steps}

    @traceable(name="netagentbench_process_scenario", run_type="chain")
    def process_scenario(
        self,
        scenario: Scenario,
        available_tools: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        result = self._graph.invoke(
            {
                "scenario": scenario,
                "available_tools": available_tools,
                "intent": "",
                "context": {},
                "tool_calls": [],
                "reasoning_steps": [],
            }
        )
        self.reasoning_steps = result["reasoning_steps"]
        return result["tool_calls"]
