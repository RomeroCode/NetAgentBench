"""
Metrics for evaluating agent performance.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json


@dataclass
class EvaluationResult:
    """Results from evaluating an agent on a scenario."""
    scenario_id: str
    success: bool
    tool_calls_correct: bool
    tool_calls_made: List[Dict[str, Any]]
    expected_tool_calls: List[Dict[str, Any]]
    errors: List[str] = field(default_factory=list)
    execution_time: Optional[float] = None
    reasoning_steps: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "scenario_id": self.scenario_id,
            "success": self.success,
            "tool_calls_correct": self.tool_calls_correct,
            "tool_calls_made": self.tool_calls_made,
            "expected_tool_calls": self.expected_tool_calls,
            "errors": self.errors,
            "execution_time": self.execution_time,
            "reasoning_steps": self.reasoning_steps
        }


class Metrics:
    """
    Calculate and aggregate metrics for agent evaluation.
    """
    
    def __init__(self):
        """Initialize metrics calculator."""
        self.results: List[EvaluationResult] = []
    
    def add_result(self, result: EvaluationResult) -> None:
        """Add an evaluation result."""
        self.results.append(result)
    
    def calculate_accuracy(self) -> float:
        """Calculate overall accuracy (percentage of successful scenarios)."""
        if not self.results:
            return 0.0
        successful = sum(1 for r in self.results if r.success)
        return successful / len(self.results)
    
    def calculate_tool_call_accuracy(self) -> float:
        """Calculate accuracy of tool calls."""
        if not self.results:
            return 0.0
        correct = sum(1 for r in self.results if r.tool_calls_correct)
        return correct / len(self.results)
    
    def calculate_precision(self) -> float:
        """
        Calculate precision: correctly made tool calls / total tool calls made.
        """
        total_made = 0
        correct_made = 0
        
        for result in self.results:
            made_tools = set((tc["tool_name"], json.dumps(tc["parameters"], sort_keys=True))
                           for tc in result.tool_calls_made)
            expected_tools = set((tc["tool_name"], json.dumps(tc["parameters"], sort_keys=True))
                                for tc in result.expected_tool_calls)
            
            total_made += len(made_tools)
            correct_made += len(made_tools & expected_tools)
        
        return correct_made / total_made if total_made > 0 else 0.0
    
    def calculate_recall(self) -> float:
        """
        Calculate recall: correctly made tool calls / expected tool calls.
        """
        total_expected = 0
        correct_made = 0
        
        for result in self.results:
            made_tools = set((tc["tool_name"], json.dumps(tc["parameters"], sort_keys=True))
                           for tc in result.tool_calls_made)
            expected_tools = set((tc["tool_name"], json.dumps(tc["parameters"], sort_keys=True))
                                for tc in result.expected_tool_calls)
            
            total_expected += len(expected_tools)
            correct_made += len(made_tools & expected_tools)
        
        return correct_made / total_expected if total_expected > 0 else 0.0
    
    def calculate_f1_score(self) -> float:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        precision = self.calculate_precision()
        recall = self.calculate_recall()
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def get_average_execution_time(self) -> Optional[float]:
        """Get average execution time."""
        times = [r.execution_time for r in self.results if r.execution_time is not None]
        return sum(times) / len(times) if times else None
    
    def get_error_analysis(self) -> Dict[str, int]:
        """Get count of different error types."""
        error_counts: Dict[str, int] = {}
        for result in self.results:
            for error in result.errors:
                error_counts[error] = error_counts.get(error, 0) + 1
        return error_counts
    
    def get_summary(self) -> Dict[str, Any]:
        """Get complete metrics summary."""
        return {
            "total_scenarios": len(self.results),
            "accuracy": self.calculate_accuracy(),
            "tool_call_accuracy": self.calculate_tool_call_accuracy(),
            "precision": self.calculate_precision(),
            "recall": self.calculate_recall(),
            "f1_score": self.calculate_f1_score(),
            "average_execution_time": self.get_average_execution_time(),
            "error_analysis": self.get_error_analysis()
        }
    
    def reset(self) -> None:
        """Reset all results."""
        self.results.clear()
    
    def save_results(self, filepath: str) -> None:
        """Save results to a JSON file."""
        data = {
            "results": [r.to_dict() for r in self.results],
            "summary": self.get_summary()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
