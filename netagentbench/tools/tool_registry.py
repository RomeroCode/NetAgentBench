"""
Tool registry for managing network automation tools.
"""

from typing import Dict, Any, List, Optional


class ToolRegistry:
    """
    Registry for managing and accessing network automation tools.
    """
    
    def __init__(self, tools: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the tool registry.
        
        Args:
            tools: List of tool definitions
        """
        self._tools: Dict[str, Dict[str, Any]] = {}
        if tools:
            for tool in tools:
                self.register_tool(tool)
    
    def register_tool(self, tool: Dict[str, Any]) -> None:
        """
        Register a tool in the registry.
        
        Args:
            tool: Tool definition dictionary
        """
        if "function" not in tool:
            raise ValueError("Tool must have 'function' key")
        
        function = tool["function"]
        if "name" not in function:
            raise ValueError("Tool function must have 'name' key")
        
        tool_name = function["name"]
        self._tools[tool_name] = tool
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool definition or None if not found
        """
        return self._tools.get(tool_name)
    
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_tool_names(self) -> List[str]:
        """Get names of all registered tools."""
        return list(self._tools.keys())
    
    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool is registered."""
        return tool_name in self._tools
    
    def unregister_tool(self, tool_name: str) -> bool:
        """
        Unregister a tool.
        
        Args:
            tool_name: Name of the tool to unregister
            
        Returns:
            True if tool was unregistered, False if not found
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()
    
    def __len__(self) -> int:
        """Return number of registered tools."""
        return len(self._tools)
    
    def __contains__(self, tool_name: str) -> bool:
        """Check if tool is in registry."""
        return tool_name in self._tools
