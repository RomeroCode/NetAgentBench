"""
Example script showing how to use NetAgentBench to evaluate an agent.
"""

from pathlib import Path
from typing import List, Dict, Any

from netagentbench import Benchmark
from netagentbench.scenarios import Scenario
from netagentbench.agents import BaseAgent


class ExampleAgent(BaseAgent):
    """
    Example agent implementation that demonstrates the interface.
    
    This is a simple rule-based agent that maps intents to tool calls.
    Real agents would use LLMs or more sophisticated reasoning.
    """
    
    def __init__(self):
        super().__init__(name="ExampleRuleBasedAgent")
    
    def process_scenario(
        self,
        scenario: Scenario,
        available_tools: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process a scenario and return tool calls.
        
        This example uses simple keyword matching - a real agent would
        use an LLM to understand the intent and select appropriate tools.
        """
        intent = scenario.intent.lower()
        context = scenario.context
        self.reasoning_steps = []
        
        self.reasoning_steps.append(f"Analyzing intent: {scenario.intent}")
        self.reasoning_steps.append(f"Available context: {list(context.keys())}")
        
        tool_calls = []
        
        # Simple keyword-based routing
        if "configure interface" in intent or "configure.*interface" in intent:
            self.reasoning_steps.append("Detected interface configuration intent")
            # Extract device and interface info from context
            tool_calls.append({
                "tool_name": "configure_interface",
                "parameters": {
                    "device_id": context.get("device_id", "unknown"),
                    "interface_name": "GigabitEthernet0/1",  # Simplified
                    "ip_address": "192.168.1.1",
                    "subnet_mask": "255.255.255.0",
                    "enabled": True
                }
            })
        
        elif "vlan" in intent:
            self.reasoning_steps.append("Detected VLAN configuration intent")
            tool_calls.append({
                "tool_name": "configure_vlan",
                "parameters": {
                    "device_id": context.get("device_id", "unknown"),
                    "vlan_id": 100,
                    "vlan_name": "Sales",
                    "interfaces": ["Eth1", "Eth2"]
                }
            })
        
        elif "connectivity" in intent or "ping" in intent:
            self.reasoning_steps.append("Detected connectivity troubleshooting intent")
            dest = context.get("server_ip", "10.0.0.5")
            tool_calls.append({
                "tool_name": "ping_test",
                "parameters": {
                    "source_device": context.get("device_id", "unknown"),
                    "destination": dest,
                    "count": 4
                }
            })
            tool_calls.append({
                "tool_name": "traceroute",
                "parameters": {
                    "source_device": context.get("device_id", "unknown"),
                    "destination": dest,
                    "max_hops": 30
                }
            })
        
        elif "block" in intent or "acl" in intent:
            self.reasoning_steps.append("Detected security/ACL configuration intent")
            tool_calls.append({
                "tool_name": "configure_acl",
                "parameters": {
                    "device_id": context.get("device_id", "unknown"),
                    "acl_name": "BLOCK_SUBNET",
                    "acl_type": "extended",
                    "rules": [],
                    "interface": "GigabitEthernet0/0",
                    "direction": "in"
                }
            })
        
        self.reasoning_steps.append(f"Generated {len(tool_calls)} tool calls")
        return tool_calls


def run_example():
    """Run example evaluation."""
    print("NetAgentBench Example Evaluation")
    print("=" * 50)
    
    # Load the benchmark dataset
    dataset_path = Path(__file__).parent.parent / "data" / "scenarios.json"
    
    if not dataset_path.exists():
        print(f"\nDataset not found at {dataset_path}")
        print("Generating example scenarios...")
        from netagentbench.scenarios.examples import create_example_scenarios
        dataset = create_example_scenarios()
        dataset.save_to_file(dataset_path)
        print(f"Dataset created with {len(dataset)} scenarios")
    
    # Initialize benchmark
    benchmark = Benchmark()
    benchmark.load_dataset(dataset_path)
    
    print(f"\nLoaded dataset with {len(benchmark.dataset)} scenarios")
    print("\nDataset statistics:")
    stats = benchmark.get_dataset_info()
    for key, value in stats["statistics"].items():
        print(f"  {key}: {value}")
    
    # Create example agent
    agent = ExampleAgent()
    
    # Define agent runner function
    def agent_runner(scenario: Scenario, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return agent.process_scenario(scenario, tools)
    
    # Run evaluation on a subset of scenarios
    print("\n" + "=" * 50)
    print("Running evaluation on difficulty 1-2 scenarios...")
    print("=" * 50)
    
    results = benchmark.run_evaluation(
        agent_runner=agent_runner,
        difficulty_range=(1, 2)
    )
    
    # Print results
    print(f"\nEvaluated {results['scenarios_evaluated']} scenarios")
    print("\nMetrics:")
    for metric, value in results['metrics'].items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.2%}")
        else:
            print(f"  {metric}: {value}")
    
    # Print individual results
    print("\n" + "=" * 50)
    print("Individual Scenario Results:")
    print("=" * 50)
    
    for result in results['results'][:5]:  # Show first 5
        print(f"\nScenario: {result['scenario_id']}")
        print(f"  Success: {result['success']}")
        print(f"  Tool Calls Correct: {result['tool_calls_correct']}")
        if result['errors']:
            print(f"  Errors: {result['errors']}")
    
    # Save results
    output_path = Path(__file__).parent.parent / "results" / "example_evaluation.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    benchmark.save_results(str(output_path))
    print(f"\nFull results saved to: {output_path}")


if __name__ == "__main__":
    run_example()
