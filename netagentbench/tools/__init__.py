"""Network automation tool definitions."""

from netagentbench.tools.tool_registry import ToolRegistry
from netagentbench.tools.network_tools import NETWORK_TOOLS
from netagentbench.tools.slice_tools import SLICE_TOOLS

__all__ = ["ToolRegistry", "NETWORK_TOOLS", "SLICE_TOOLS"]
