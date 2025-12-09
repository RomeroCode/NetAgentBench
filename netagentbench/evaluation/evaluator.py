"""
Evaluator for assessing agent performance on scenarios.
"""

import json
from typing import List, Dict, Any, Callable, Optional
from netagentbench.scenarios.scenario import Scenario, ToolCall
from netagentbench.evaluation.metrics import EvaluationResult


class Evaluator:
    """
    Evaluates agent responses against expected tool calls.
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize evaluator.
        
        Args:
            strict_mode: If True, require exact parameter matches. If False,
                        allow partial matches for non-required parameters.
        """
        self.strict_mode = strict_mode
    
    def evaluate_tool_call(
        self,
        made_call: Dict[str, Any],
        expected_call: ToolCall
    ) -> bool:
        """
        Check if a made tool call matches an expected tool call.
        
        Args:
            made_call: The tool call made by the agent
            expected_call: The expected tool call
            
        Returns:
            True if the tool call matches, False otherwise
        """
        # Check tool name
        if made_call.get("tool_name") != expected_call.tool_name:
            return False
        
        made_params = made_call.get("parameters", {})
        expected_params = expected_call.parameters
        
        # In strict mode, require exact match
        if self.strict_mode:
            return made_params == expected_params
        
        # In non-strict mode, check if all expected parameters are present
        for key, value in expected_params.items():
            if key not in made_params:
                return False
            if made_params[key] != value:
                return False
        
        return True
    
    def evaluate_scenario(
        self,
        scenario: Scenario,
        tool_calls_made: List[Dict[str, Any]],
        execution_time: Optional[float] = None,
        reasoning_steps: Optional[List[str]] = None
    ) -> EvaluationResult:
        """
        Evaluate agent performance on a scenario.
        
        Args:
            scenario: The scenario being evaluated
            tool_calls_made: List of tool calls made by the agent
            execution_time: Time taken to execute (optional)
            reasoning_steps: Reasoning steps taken (optional)
            
        Returns:
            EvaluationResult with evaluation details
        """
        errors = []
        expected_tools = scenario.expected_tools
        
        # Check if the right number of tools were called
        if len(tool_calls_made) != len(expected_tools):
            errors.append(
                f"Expected {len(expected_tools)} tool calls, got {len(tool_calls_made)}"
            )
        
        # Match tool calls
        matched_expected = set()
        matched_made = set()
        
        for i, made_call in enumerate(tool_calls_made):
            for j, expected_call in enumerate(expected_tools):
                if j in matched_expected:
                    continue
                    
                if self.evaluate_tool_call(made_call, expected_call):
                    # If order matters, check it
                    if expected_call.order is not None:
                        if i != expected_call.order:
                            errors.append(
                                f"Tool '{made_call['tool_name']}' called at position {i}, "
                                f"expected at position {expected_call.order}"
                            )
                            continue
                    
                    matched_expected.add(j)
                    matched_made.add(i)
                    break
        
        # Find unmatched tool calls
        for i, made_call in enumerate(tool_calls_made):
            if i not in matched_made:
                errors.append(
                    f"Unexpected or incorrect tool call: {made_call['tool_name']}"
                )
        
        for j, expected_call in enumerate(expected_tools):
            if j not in matched_expected:
                errors.append(
                    f"Missing expected tool call: {expected_call.tool_name}"
                )
        
        # Determine success
        tool_calls_correct = len(matched_expected) == len(expected_tools) and \
                           len(matched_made) == len(tool_calls_made)
        success = tool_calls_correct and len(errors) == 0
        
        # Convert expected tools to dict format for result
        expected_calls_dict = [
            {
                "tool_name": tc.tool_name,
                "parameters": tc.parameters,
                "order": tc.order
            }
            for tc in expected_tools
        ]
        
        return EvaluationResult(
            scenario_id=scenario.id,
            success=success,
            tool_calls_correct=tool_calls_correct,
            tool_calls_made=tool_calls_made,
            expected_tool_calls=expected_calls_dict,
            errors=errors,
            execution_time=execution_time,
            reasoning_steps=reasoning_steps
        )
    
    def batch_evaluate(
        self,
        scenarios: List[Scenario],
        agent_runner: Callable[[Scenario], List[Dict[str, Any]]]
    ) -> List[EvaluationResult]:
        """
        Evaluate agent on multiple scenarios.
        
        Args:
            scenarios: List of scenarios to evaluate
            agent_runner: Function that takes a scenario and returns tool calls
            
        Returns:
            List of evaluation results
        """
        results = []
        
        for scenario in scenarios:
            tool_calls = agent_runner(scenario)
            result = self.evaluate_scenario(scenario, tool_calls)
            results.append(result)
        
        return results
