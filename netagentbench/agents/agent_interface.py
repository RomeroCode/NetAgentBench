"""
Interface definition for agents to be evaluated.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from netagentbench.scenarios.scenario import Scenario


class AgentInterface(ABC):
    """
    Abstract interface that agents must implement to be evaluated.
    """
    
    @abstractmethod
    def process_scenario(
        self,
        scenario: Scenario,
        available_tools: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process a scenario and return tool calls.
        
        Args:
            scenario: The scenario to process
            available_tools: List of available tool definitions
            
        Returns:
            List of tool calls in format:
            [
                {
                    "tool_name": str,
                    "parameters": dict
                },
                ...
            ]
        """
        pass
    
    @abstractmethod
    def get_reasoning_steps(self) -> List[str]:
        """
        Get the reasoning steps taken for the last scenario.
        
        Returns:
            List of reasoning steps as strings
        """
        pass
    
    def reset(self) -> None:
        """Reset agent state (optional, can be overridden)."""
        pass
