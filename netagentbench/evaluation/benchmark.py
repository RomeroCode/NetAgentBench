"""
Main benchmark class for NetAgentBench.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
from netagentbench.scenarios.dataset import ScenarioDataset
from netagentbench.scenarios.scenario import Scenario, ScenarioCategory
from netagentbench.evaluation.evaluator import Evaluator
from netagentbench.evaluation.metrics import Metrics, EvaluationResult
from netagentbench.tools.network_tools import NETWORK_TOOLS
from netagentbench.tools.tool_registry import ToolRegistry


class Benchmark:
    """
    Main benchmark class for evaluating AI agents on network automation tasks.
    """
    
    def __init__(
        self,
        dataset: Optional[ScenarioDataset] = None,
        strict_mode: bool = False
    ):
        """
        Initialize the benchmark.
        
        Args:
            dataset: ScenarioDataset to use for evaluation
            strict_mode: Whether to use strict evaluation mode
        """
        self.dataset = dataset or ScenarioDataset()
        self.evaluator = Evaluator(strict_mode=strict_mode)
        self.metrics = Metrics()
        self.tool_registry = ToolRegistry(NETWORK_TOOLS)
    
    def load_dataset(self, filepath: Path) -> None:
        """
        Load dataset from file.
        
        Args:
            filepath: Path to dataset file
        """
        self.dataset = ScenarioDataset.load_from_file(filepath)
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools for the agent."""
        return self.tool_registry.get_all_tools()
    
    def run_evaluation(
        self,
        agent_runner: Callable[[Scenario, List[Dict[str, Any]]], List[Dict[str, Any]]],
        scenarios: Optional[List[Scenario]] = None,
        category_filter: Optional[ScenarioCategory] = None,
        difficulty_range: Optional[tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Run evaluation on scenarios.
        
        Args:
            agent_runner: Function that takes (scenario, tools) and returns tool calls
            scenarios: Specific scenarios to evaluate (uses dataset if None)
            category_filter: Filter scenarios by category
            difficulty_range: Filter scenarios by difficulty (min, max)
            
        Returns:
            Dictionary with evaluation results and metrics
        """
        # Determine which scenarios to evaluate
        if scenarios is None:
            scenarios = list(self.dataset.scenarios)
        
        # Apply filters
        if category_filter:
            scenarios = [s for s in scenarios if s.category == category_filter]
        
        if difficulty_range:
            min_diff, max_diff = difficulty_range
            scenarios = [s for s in scenarios 
                        if min_diff <= s.difficulty <= max_diff]
        
        if not scenarios:
            raise ValueError("No scenarios match the specified filters")
        
        # Reset metrics
        self.metrics.reset()
        
        # Evaluate each scenario
        tools = self.get_tools()
        
        for scenario in scenarios:
            # Run agent on scenario
            tool_calls = agent_runner(scenario, tools)
            
            # Evaluate results
            result = self.evaluator.evaluate_scenario(scenario, tool_calls)
            self.metrics.add_result(result)
        
        # Return results and metrics
        return {
            "scenarios_evaluated": len(scenarios),
            "results": [r.to_dict() for r in self.metrics.results],
            "metrics": self.metrics.get_summary()
        }
    
    def save_results(self, filepath: str) -> None:
        """
        Save evaluation results to file.
        
        Args:
            filepath: Path to save results
        """
        self.metrics.save_results(filepath)
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the current dataset."""
        return {
            "dataset_size": len(self.dataset),
            "statistics": self.dataset.get_statistics()
        }
