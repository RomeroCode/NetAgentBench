"""
Scenario definitions for network automation benchmarking.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class ScenarioCategory(Enum):
    """Categories of network automation scenarios."""
    CONFIGURATION = "configuration"
    TROUBLESHOOTING = "troubleshooting"
    MONITORING = "monitoring"
    SECURITY = "security"
    OPTIMIZATION = "optimization"


@dataclass
class ToolCall:
    """Represents an expected tool call."""
    tool_name: str
    parameters: Dict[str, Any]
    order: Optional[int] = None  # For scenarios requiring specific order


@dataclass
class Scenario:
    """
    Represents a network automation scenario for benchmarking.
    
    Attributes:
        id: Unique identifier for the scenario
        category: Category of the scenario
        intent: Natural language description of the network intent
        context: Additional context information (topology, current state, etc.)
        expected_tools: List of expected tool calls to fulfill the intent
        difficulty: Difficulty level (1-5)
        requires_reasoning: Whether the scenario requires multi-step reasoning
        metadata: Additional metadata for the scenario
    """
    id: str
    category: ScenarioCategory
    intent: str
    context: Dict[str, Any]
    expected_tools: List[ToolCall]
    difficulty: int = 1
    requires_reasoning: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate scenario after initialization."""
        if not 1 <= self.difficulty <= 5:
            raise ValueError(f"Difficulty must be between 1 and 5, got {self.difficulty}")
        if not self.id:
            raise ValueError("Scenario ID cannot be empty")
        if not self.intent:
            raise ValueError("Intent cannot be empty")
        if not self.expected_tools:
            raise ValueError("Expected tools cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scenario to dictionary format."""
        return {
            "id": self.id,
            "category": self.category.value,
            "intent": self.intent,
            "context": self.context,
            "expected_tools": [
                {
                    "tool_name": tool.tool_name,
                    "parameters": tool.parameters,
                    "order": tool.order
                }
                for tool in self.expected_tools
            ],
            "difficulty": self.difficulty,
            "requires_reasoning": self.requires_reasoning,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scenario":
        """Create scenario from dictionary format."""
        return cls(
            id=data["id"],
            category=ScenarioCategory(data["category"]),
            intent=data["intent"],
            context=data["context"],
            expected_tools=[
                ToolCall(
                    tool_name=tool["tool_name"],
                    parameters=tool["parameters"],
                    order=tool.get("order")
                )
                for tool in data["expected_tools"]
            ],
            difficulty=data.get("difficulty", 1),
            requires_reasoning=data.get("requires_reasoning", False),
            metadata=data.get("metadata", {})
        )
