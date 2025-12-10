"""Tests for scenario definitions and dataset."""

import pytest
from netagentbench.scenarios.scenario import Scenario, ScenarioCategory, ToolCall
from netagentbench.scenarios.dataset import ScenarioDataset
from pathlib import Path
import tempfile


def test_tool_call_creation():
    """Test ToolCall creation."""
    tool_call = ToolCall(
        tool_name="configure_interface",
        parameters={"device_id": "R1", "ip": "192.168.1.1"}
    )
    assert tool_call.tool_name == "configure_interface"
    assert tool_call.parameters["device_id"] == "R1"
    assert tool_call.order is None


def test_scenario_creation():
    """Test Scenario creation."""
    scenario = Scenario(
        id="test_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Test intent",
        context={"device_id": "R1"},
        expected_tools=[
            ToolCall(
                tool_name="test_tool",
                parameters={"param": "value"}
            )
        ],
        difficulty=2
    )
    
    assert scenario.id == "test_001"
    assert scenario.category == ScenarioCategory.CONFIGURATION
    assert scenario.difficulty == 2
    assert len(scenario.expected_tools) == 1


def test_scenario_validation():
    """Test Scenario validation."""
    # Test invalid difficulty
    with pytest.raises(ValueError):
        Scenario(
            id="test_001",
            category=ScenarioCategory.CONFIGURATION,
            intent="Test",
            context={},
            expected_tools=[ToolCall("tool", {})],
            difficulty=10  # Invalid
        )
    
    # Test empty ID
    with pytest.raises(ValueError):
        Scenario(
            id="",
            category=ScenarioCategory.CONFIGURATION,
            intent="Test",
            context={},
            expected_tools=[ToolCall("tool", {})]
        )


def test_scenario_to_dict():
    """Test Scenario serialization."""
    scenario = Scenario(
        id="test_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Test intent",
        context={"device_id": "R1"},
        expected_tools=[
            ToolCall(
                tool_name="test_tool",
                parameters={"param": "value"}
            )
        ]
    )
    
    data = scenario.to_dict()
    assert data["id"] == "test_001"
    assert data["category"] == "configuration"
    assert len(data["expected_tools"]) == 1


def test_scenario_from_dict():
    """Test Scenario deserialization."""
    data = {
        "id": "test_001",
        "category": "configuration",
        "intent": "Test intent",
        "context": {"device_id": "R1"},
        "expected_tools": [
            {
                "tool_name": "test_tool",
                "parameters": {"param": "value"},
                "order": None
            }
        ],
        "difficulty": 1,
        "requires_reasoning": False,
        "metadata": {}
    }
    
    scenario = Scenario.from_dict(data)
    assert scenario.id == "test_001"
    assert scenario.category == ScenarioCategory.CONFIGURATION


def test_dataset_operations():
    """Test ScenarioDataset operations."""
    dataset = ScenarioDataset()
    
    scenario = Scenario(
        id="test_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Test",
        context={},
        expected_tools=[ToolCall("tool", {})]
    )
    
    dataset.add_scenario(scenario)
    assert len(dataset) == 1
    
    found = dataset.get_by_id("test_001")
    assert found is not None
    assert found.id == "test_001"


def test_dataset_filtering():
    """Test dataset filtering."""
    dataset = ScenarioDataset()
    
    dataset.add_scenario(Scenario(
        id="config_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Test",
        context={},
        expected_tools=[ToolCall("tool", {})],
        difficulty=1
    ))
    
    dataset.add_scenario(Scenario(
        id="troubleshoot_001",
        category=ScenarioCategory.TROUBLESHOOTING,
        intent="Test",
        context={},
        expected_tools=[ToolCall("tool", {})],
        difficulty=3,
        requires_reasoning=True
    ))
    
    # Filter by category
    config_scenarios = dataset.filter_by_category(ScenarioCategory.CONFIGURATION)
    assert len(config_scenarios) == 1
    
    # Filter by difficulty
    easy_scenarios = dataset.filter_by_difficulty(1, 2)
    assert len(easy_scenarios) == 1
    
    # Get reasoning scenarios
    reasoning = dataset.get_reasoning_scenarios()
    assert len(reasoning) == 1


def test_dataset_save_load():
    """Test dataset save and load."""
    dataset = ScenarioDataset()
    
    dataset.add_scenario(Scenario(
        id="test_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Test",
        context={},
        expected_tools=[ToolCall("tool", {})]
    ))
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_dataset.json"
        dataset.save_to_file(filepath)
        
        loaded_dataset = ScenarioDataset.load_from_file(filepath)
        assert len(loaded_dataset) == 1
        assert loaded_dataset.scenarios[0].id == "test_001"


def test_dataset_statistics():
    """Test dataset statistics."""
    dataset = ScenarioDataset()
    
    dataset.add_scenario(Scenario(
        id="config_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Test",
        context={},
        expected_tools=[ToolCall("tool", {})],
        difficulty=1
    ))
    
    stats = dataset.get_statistics()
    assert stats["total_scenarios"] == 1
    assert stats["by_category"]["configuration"] == 1
    assert stats["by_difficulty"]["1"] == 1
