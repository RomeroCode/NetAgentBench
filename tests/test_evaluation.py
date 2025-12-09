"""Tests for evaluation framework."""

import pytest
from netagentbench.evaluation.evaluator import Evaluator
from netagentbench.evaluation.metrics import Metrics, EvaluationResult
from netagentbench.scenarios.scenario import Scenario, ScenarioCategory, ToolCall


def test_evaluator_tool_call_matching():
    """Test tool call matching in evaluator."""
    evaluator = Evaluator(strict_mode=False)
    
    made_call = {
        "tool_name": "configure_interface",
        "parameters": {
            "device_id": "R1",
            "interface_name": "eth0",
            "ip_address": "192.168.1.1",
            "subnet_mask": "255.255.255.0"
        }
    }
    
    expected_call = ToolCall(
        tool_name="configure_interface",
        parameters={
            "device_id": "R1",
            "interface_name": "eth0",
            "ip_address": "192.168.1.1",
            "subnet_mask": "255.255.255.0"
        }
    )
    
    assert evaluator.evaluate_tool_call(made_call, expected_call) is True


def test_evaluator_tool_call_mismatch():
    """Test tool call mismatch detection."""
    evaluator = Evaluator(strict_mode=False)
    
    made_call = {
        "tool_name": "configure_interface",
        "parameters": {"device_id": "R1"}
    }
    
    expected_call = ToolCall(
        tool_name="configure_vlan",
        parameters={"device_id": "R1"}
    )
    
    assert evaluator.evaluate_tool_call(made_call, expected_call) is False


def test_evaluator_scenario_success():
    """Test successful scenario evaluation."""
    evaluator = Evaluator()
    
    scenario = Scenario(
        id="test_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Configure interface",
        context={},
        expected_tools=[
            ToolCall(
                tool_name="configure_interface",
                parameters={"device_id": "R1", "ip": "192.168.1.1"}
            )
        ]
    )
    
    tool_calls_made = [
        {
            "tool_name": "configure_interface",
            "parameters": {"device_id": "R1", "ip": "192.168.1.1"}
        }
    ]
    
    result = evaluator.evaluate_scenario(scenario, tool_calls_made)
    assert result.success is True
    assert result.tool_calls_correct is True
    assert len(result.errors) == 0


def test_evaluator_scenario_failure():
    """Test failed scenario evaluation."""
    evaluator = Evaluator()
    
    scenario = Scenario(
        id="test_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Configure interface",
        context={},
        expected_tools=[
            ToolCall(
                tool_name="configure_interface",
                parameters={"device_id": "R1"}
            )
        ]
    )
    
    tool_calls_made = [
        {
            "tool_name": "configure_vlan",
            "parameters": {"device_id": "R1"}
        }
    ]
    
    result = evaluator.evaluate_scenario(scenario, tool_calls_made)
    assert result.success is False
    assert result.tool_calls_correct is False
    assert len(result.errors) > 0


def test_metrics_accuracy():
    """Test metrics accuracy calculation."""
    metrics = Metrics()
    
    # Add successful result
    metrics.add_result(EvaluationResult(
        scenario_id="test_001",
        success=True,
        tool_calls_correct=True,
        tool_calls_made=[],
        expected_tool_calls=[]
    ))
    
    # Add failed result
    metrics.add_result(EvaluationResult(
        scenario_id="test_002",
        success=False,
        tool_calls_correct=False,
        tool_calls_made=[],
        expected_tool_calls=[]
    ))
    
    assert metrics.calculate_accuracy() == 0.5


def test_metrics_precision_recall():
    """Test precision and recall calculation."""
    metrics = Metrics()
    
    metrics.add_result(EvaluationResult(
        scenario_id="test_001",
        success=True,
        tool_calls_correct=True,
        tool_calls_made=[
            {"tool_name": "tool1", "parameters": {"a": 1}}
        ],
        expected_tool_calls=[
            {"tool_name": "tool1", "parameters": {"a": 1}}
        ]
    ))
    
    precision = metrics.calculate_precision()
    recall = metrics.calculate_recall()
    
    assert precision == 1.0
    assert recall == 1.0


def test_metrics_f1_score():
    """Test F1 score calculation."""
    metrics = Metrics()
    
    metrics.add_result(EvaluationResult(
        scenario_id="test_001",
        success=True,
        tool_calls_correct=True,
        tool_calls_made=[
            {"tool_name": "tool1", "parameters": {"a": 1}}
        ],
        expected_tool_calls=[
            {"tool_name": "tool1", "parameters": {"a": 1}}
        ]
    ))
    
    f1 = metrics.calculate_f1_score()
    assert f1 == 1.0


def test_metrics_summary():
    """Test metrics summary generation."""
    metrics = Metrics()
    
    metrics.add_result(EvaluationResult(
        scenario_id="test_001",
        success=True,
        tool_calls_correct=True,
        tool_calls_made=[],
        expected_tool_calls=[],
        errors=[]
    ))
    
    summary = metrics.get_summary()
    
    assert "total_scenarios" in summary
    assert "accuracy" in summary
    assert "precision" in summary
    assert "recall" in summary
    assert "f1_score" in summary
    assert summary["total_scenarios"] == 1
