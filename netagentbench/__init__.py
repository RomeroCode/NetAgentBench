"""
NetAgentBench: A benchmark for evaluating AI Agents in Intent-Based Network Automation.

This package provides tools and datasets for evaluating Large Language Models (LLMs)
and AI Agents on their ability to:
1. Interpret network management intentions (Intent-based Networking)
2. Orchestrate correct tool calls (function calling)
3. Perform network automation tasks
"""

__version__ = "0.1.0"
__author__ = "RomeroCode"

from netagentbench.evaluation.benchmark import Benchmark
from netagentbench.evaluation.metrics import Metrics

__all__ = ["Benchmark", "Metrics", "__version__"]
