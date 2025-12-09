#!/usr/bin/env python3
"""
Command-line interface for NetAgentBench.
"""

import argparse
import sys
from pathlib import Path
from netagentbench import Benchmark
from netagentbench.scenarios.examples import create_example_scenarios


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NetAgentBench - Benchmark for AI Agents in Network Automation"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show benchmark information")
    info_parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/scenarios.json"),
        help="Path to dataset file"
    )
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate example dataset")
    generate_parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/scenarios.json"),
        help="Output path for dataset"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List scenarios")
    list_parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/scenarios.json"),
        help="Path to dataset file"
    )
    list_parser.add_argument(
        "--category",
        help="Filter by category"
    )
    list_parser.add_argument(
        "--difficulty",
        type=int,
        help="Filter by difficulty level"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "info":
        return info_command(args)
    elif args.command == "generate":
        return generate_command(args)
    elif args.command == "list":
        return list_command(args)
    
    return 0


def info_command(args):
    """Show benchmark information."""
    try:
        benchmark = Benchmark()
        
        if args.dataset.exists():
            benchmark.load_dataset(args.dataset)
            print(f"Dataset: {args.dataset}")
        else:
            print(f"Dataset not found: {args.dataset}")
            print("Use 'netagentbench generate' to create example dataset")
            return 1
        
        info = benchmark.get_dataset_info()
        stats = info["statistics"]
        
        print(f"\nTotal Scenarios: {info['dataset_size']}")
        print("\nBy Category:")
        for category, count in stats["by_category"].items():
            if count > 0:
                print(f"  {category}: {count}")
        
        print("\nBy Difficulty:")
        for difficulty, count in stats["by_difficulty"].items():
            if count > 0:
                print(f"  Level {difficulty}: {count}")
        
        print(f"\nReasoning Required: {stats['reasoning_scenarios']}")
        
        print(f"\nAvailable Tools: {len(benchmark.get_tools())}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def generate_command(args):
    """Generate example dataset."""
    try:
        print(f"Generating example scenarios...")
        dataset = create_example_scenarios()
        
        args.output.parent.mkdir(parents=True, exist_ok=True)
        dataset.save_to_file(args.output)
        
        print(f"Generated {len(dataset)} scenarios")
        print(f"Saved to: {args.output}")
        
        stats = dataset.get_statistics()
        print("\nDataset Statistics:")
        print(f"  Total: {stats['total_scenarios']}")
        print(f"  Categories: {len([c for c, v in stats['by_category'].items() if v > 0])}")
        print(f"  Difficulty range: 1-{max(int(k) for k, v in stats['by_difficulty'].items() if v > 0)}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def list_command(args):
    """List scenarios."""
    try:
        if not args.dataset.exists():
            print(f"Dataset not found: {args.dataset}", file=sys.stderr)
            print("Use 'netagentbench generate' to create example dataset")
            return 1
        
        benchmark = Benchmark()
        benchmark.load_dataset(args.dataset)
        
        scenarios = benchmark.dataset.scenarios
        
        # Apply filters
        if args.category:
            from netagentbench.scenarios.scenario import ScenarioCategory
            try:
                category = ScenarioCategory(args.category.lower())
                scenarios = [s for s in scenarios if s.category == category]
            except ValueError:
                print(f"Invalid category: {args.category}", file=sys.stderr)
                return 1
        
        if args.difficulty:
            scenarios = [s for s in scenarios if s.difficulty == args.difficulty]
        
        print(f"Found {len(scenarios)} scenarios:\n")
        
        for scenario in scenarios:
            print(f"ID: {scenario.id}")
            print(f"  Category: {scenario.category.value}")
            print(f"  Difficulty: {scenario.difficulty}")
            print(f"  Reasoning: {scenario.requires_reasoning}")
            print(f"  Intent: {scenario.intent}")
            print(f"  Tools: {len(scenario.expected_tools)}")
            print()
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
