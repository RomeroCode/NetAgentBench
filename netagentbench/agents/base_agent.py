"""
Base agent implementation with common functionality.
"""

from typing import List, Dict, Any
from netagentbench.agents.agent_interface import AgentInterface
from netagentbench.scenarios.scenario import Scenario


class BaseAgent(AgentInterface):
    """
    Base implementation of an agent with common utilities.
    
    This is a simple example agent that can be extended.
    """
    
    def __init__(self, name: str = "BaseAgent"):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
        """
        self.name = name
        self.reasoning_steps: List[str] = []
    
    def process_scenario(
        self,
        scenario: Scenario,
        available_tools: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process a scenario and return tool calls.
        
        This is a placeholder implementation that should be overridden.
        
        Args:
            scenario: The scenario to process
            available_tools: List of available tool definitions
            
        Returns:
            List of tool calls
        """
        self.reasoning_steps = [
            f"Received scenario: {scenario.id}",
            f"Intent: {scenario.intent}",
            f"Available tools: {len(available_tools)}",
            "Placeholder implementation - override this method"
        ]
        
        # Placeholder: return empty list
        return []
    
    def get_reasoning_steps(self) -> List[str]:
        """Get the reasoning steps from the last scenario."""
        return self.reasoning_steps.copy()
    
    def reset(self) -> None:
        """Reset agent state."""
        self.reasoning_steps.clear()
    
    def find_tool_by_name(
        self,
        tool_name: str,
        available_tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Find a tool definition by name.
        
        Args:
            tool_name: Name of the tool to find
            available_tools: List of available tools
            
        Returns:
            Tool definition dictionary
            
        Raises:
            ValueError: If tool is not found
        """
        for tool in available_tools:
            if tool["function"]["name"] == tool_name:
                return tool
        raise ValueError(f"Tool '{tool_name}' not found in available tools")
    
    def extract_tool_names(self, available_tools: List[Dict[str, Any]]) -> List[str]:
        """
        Extract tool names from tool definitions.
        
        Args:
            available_tools: List of available tools
            
        Returns:
            List of tool names
        """
        return [tool["function"]["name"] for tool in available_tools]
