"""
Dataset management for network automation scenarios.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from netagentbench.scenarios.scenario import Scenario, ScenarioCategory


class ScenarioDataset:
    """
    Manages a collection of network automation scenarios.
    """
    
    def __init__(self, scenarios: Optional[List[Scenario]] = None):
        """
        Initialize the dataset.
        
        Args:
            scenarios: List of scenarios to initialize with
        """
        self.scenarios = scenarios or []
    
    def add_scenario(self, scenario: Scenario) -> None:
        """Add a scenario to the dataset."""
        self.scenarios.append(scenario)
    
    def get_by_id(self, scenario_id: str) -> Optional[Scenario]:
        """Get a scenario by its ID."""
        for scenario in self.scenarios:
            if scenario.id == scenario_id:
                return scenario
        return None
    
    def filter_by_category(self, category: ScenarioCategory) -> List[Scenario]:
        """Filter scenarios by category."""
        return [s for s in self.scenarios if s.category == category]
    
    def filter_by_difficulty(self, min_difficulty: int = 1, max_difficulty: int = 5) -> List[Scenario]:
        """Filter scenarios by difficulty range."""
        return [
            s for s in self.scenarios
            if min_difficulty <= s.difficulty <= max_difficulty
        ]
    
    def get_reasoning_scenarios(self) -> List[Scenario]:
        """Get scenarios that require multi-step reasoning."""
        return [s for s in self.scenarios if s.requires_reasoning]
    
    def save_to_file(self, filepath: Path) -> None:
        """
        Save dataset to a JSON file.
        
        Args:
            filepath: Path to save the dataset
        """
        data = {
            "version": "0.1.0",
            "scenarios": [s.to_dict() for s in self.scenarios]
        }
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: Path) -> "ScenarioDataset":
        """
        Load dataset from a JSON file.
        
        Args:
            filepath: Path to load the dataset from
            
        Returns:
            ScenarioDataset instance
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        scenarios = [Scenario.from_dict(s) for s in data["scenarios"]]
        return cls(scenarios)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the dataset."""
        if not self.scenarios:
            return {
                "total_scenarios": 0,
                "by_category": {},
                "by_difficulty": {},
                "reasoning_scenarios": 0
            }
        
        category_counts = {}
        for category in ScenarioCategory:
            category_counts[category.value] = len(self.filter_by_category(category))
        
        difficulty_counts = {}
        for difficulty in range(1, 6):
            difficulty_counts[str(difficulty)] = len([
                s for s in self.scenarios if s.difficulty == difficulty
            ])
        
        return {
            "total_scenarios": len(self.scenarios),
            "by_category": category_counts,
            "by_difficulty": difficulty_counts,
            "reasoning_scenarios": len(self.get_reasoning_scenarios())
        }
    
    def __len__(self) -> int:
        """Return the number of scenarios in the dataset."""
        return len(self.scenarios)
    
    def __iter__(self):
        """Iterate over scenarios."""
        return iter(self.scenarios)
