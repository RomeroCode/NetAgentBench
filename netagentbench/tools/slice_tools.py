"""
LangGraph-compatible tool definitions for slice state APIs.
"""

from typing import Any, Dict, List


SLICE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_slice_state",
            "description": "Call the API to create a new record in slice_state",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"},
                    "tenant_id": {"type": "string", "description": "Tenant identifier"},
                    "lifecycle_state": {
                        "type": "string",
                        "enum": ["NONE", "CREATED", "CONFIGURED", "ACTIVE"],
                        "description": "Slice lifecycle state",
                    },
                },
                "required": ["slice_id", "tenant_id", "lifecycle_state"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_slice_state",
            "description": "Call the API to read a record from slice_state by slice_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"}
                },
                "required": ["slice_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_slice_lifecycle_state",
            "description": "Call the API to update lifecycle_state in slice_state",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"},
                    "lifecycle_state": {
                        "type": "string",
                        "enum": ["NONE", "CREATED", "CONFIGURED", "ACTIVE"],
                        "description": "New lifecycle state",
                    },
                },
                "required": ["slice_id", "lifecycle_state"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_slice_state",
            "description": "Call the API to delete a record from slice_state (cascade to related states)",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"}
                },
                "required": ["slice_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "upsert_slice_configuration_state",
            "description": "Call the API to create or update a record in slice_configuration_state",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"},
                    "configured_nfs": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Configured network functions",
                    },
                    "policies_applied": {
                        "type": "boolean",
                        "description": "Whether policies were applied",
                        "default": False,
                    },
                    "last_config_status": {
                        "type": "string",
                        "enum": ["SUCCESS", "PARTIAL", "FAILED"],
                        "description": "Last configuration status",
                    },
                },
                "required": [
                    "slice_id",
                    "configured_nfs",
                    "policies_applied",
                    "last_config_status",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_slice_configuration_state",
            "description": "Call the API to read a record from slice_configuration_state by slice_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"}
                },
                "required": ["slice_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "upsert_slice_verification_state",
            "description": "Call the API to create or update a record in slice_verification_state",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"},
                    "verification_result": {
                        "type": "string",
                        "enum": ["OK", "DEGRADED", "NOK"],
                        "description": "Verification result",
                    },
                    "issues": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of detected issues",
                    },
                },
                "required": ["slice_id", "verification_result"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_slice_verification_state",
            "description": "Call the API to read a record from slice_verification_state by slice_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"}
                },
                "required": ["slice_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "upsert_slice_usage_state",
            "description": "Call the API to create or update a record in slice_usage_state",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"},
                    "active_ues": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of active UEs",
                    },
                    "traffic_present": {
                        "type": "boolean",
                        "description": "Whether traffic is present",
                        "default": False,
                    },
                    "avg_latency_ms": {
                        "type": "integer",
                        "description": "Average latency in milliseconds",
                    },
                    "avg_throughput_mbps": {
                        "type": "integer",
                        "description": "Average throughput in Mbps",
                    },
                },
                "required": ["slice_id", "active_ues", "traffic_present"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_slice_usage_state",
            "description": "Call the API to read a record from slice_usage_state by slice_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"}
                },
                "required": ["slice_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_tool_call_history",
            "description": "Call the API to insert a record in tool_call_history",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {
                        "type": "string",
                        "description": "Unique slice identifier linked to the call",
                    },
                    "tool_name": {"type": "string", "description": "Called tool name"},
                    "tool_input": {
                        "type": "object",
                        "description": "Input payload sent to the tool",
                    },
                    "tool_output": {
                        "type": "object",
                        "description": "Output payload returned by the tool",
                    },
                    "result": {"type": "string", "description": "Result label or status"},
                },
                "required": ["tool_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tool_call_history",
            "description": "Call the API to list records from tool_call_history for a slice",
            "parameters": {
                "type": "object",
                "properties": {
                    "slice_id": {"type": "string", "description": "Unique slice identifier"},
                    "limit": {
                        "type": "integer",
                        "description": "Maximum records to return",
                        "default": 50,
                    },
                },
                "required": ["slice_id"],
            },
        },
    },
]


def get_slice_tool_by_name(tool_name: str) -> Dict[str, Any]:
    """
    Get slice tool definition by name.

    Args:
        tool_name: Name of the tool

    Returns:
        Slice tool definition dictionary
    """
    for tool in SLICE_TOOLS:
        if tool["function"]["name"] == tool_name:
            return tool
    raise ValueError(f"Slice tool '{tool_name}' not found")


def get_all_slice_tool_names() -> List[str]:
    """Get list of all available slice tool names."""
    return [tool["function"]["name"] for tool in SLICE_TOOLS]
