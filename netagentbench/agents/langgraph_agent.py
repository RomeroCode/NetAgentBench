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

        if "configure interface" in intent or "configure.*interface" in intent:
            reasoning_steps.append("Detected interface configuration intent")
            if "configure_interface" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "configure_interface",
                        "parameters": {
                            "device_id": context.get("device_id", "unknown"),
                            "interface_name": "GigabitEthernet0/1",
                            "ip_address": "192.168.1.1",
                            "subnet_mask": "255.255.255.0",
                            "enabled": True,
                        },
                    }
                )
        elif "vlan" in intent:
            reasoning_steps.append("Detected VLAN configuration intent")
            if "configure_vlan" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "configure_vlan",
                        "parameters": {
                            "device_id": context.get("device_id", "unknown"),
                            "vlan_id": 100,
                            "vlan_name": "Sales",
                            "interfaces": ["Eth1", "Eth2"],
                        },
                    }
                )
        elif "connectivity" in intent or "ping" in intent:
            reasoning_steps.append("Detected connectivity troubleshooting intent")
            destination = context.get("server_ip", "10.0.0.5")
            if "ping_test" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "ping_test",
                        "parameters": {
                            "source_device": context.get("device_id", "unknown"),
                            "destination": destination,
                            "count": 4,
                        },
                    }
                )
            if "traceroute" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "traceroute",
                        "parameters": {
                            "source_device": context.get("device_id", "unknown"),
                            "destination": destination,
                            "max_hops": 30,
                        },
                    }
                )
        elif "block" in intent or "acl" in intent:
            reasoning_steps.append("Detected security/ACL configuration intent")
            if "configure_acl" in available_tool_names:
                tool_calls.append(
                    {
                        "tool_name": "configure_acl",
                        "parameters": {
                            "device_id": context.get("device_id", "unknown"),
                            "acl_name": "BLOCK_SUBNET",
                            "acl_type": "extended",
                            "rules": [],
                            "interface": "GigabitEthernet0/0",
                            "direction": "in",
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
