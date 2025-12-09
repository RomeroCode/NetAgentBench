"""
Example scenarios for NetAgentBench.
"""

from netagentbench.scenarios.scenario import Scenario, ScenarioCategory, ToolCall
from netagentbench.scenarios.dataset import ScenarioDataset


def create_example_scenarios() -> ScenarioDataset:
    """
    Create a dataset of example scenarios.
    
    Returns:
        ScenarioDataset with example scenarios
    """
    scenarios = []
    
    # Scenario 1: Simple interface configuration
    scenarios.append(Scenario(
        id="config_001",
        category=ScenarioCategory.CONFIGURATION,
        intent="Configure interface GigabitEthernet0/1 on router R1 with IP 192.168.1.1/24",
        context={
            "device_id": "R1",
            "device_type": "router",
            "current_config": "Interface is currently shutdown"
        },
        expected_tools=[
            ToolCall(
                tool_name="configure_interface",
                parameters={
                    "device_id": "R1",
                    "interface_name": "GigabitEthernet0/1",
                    "ip_address": "192.168.1.1",
                    "subnet_mask": "255.255.255.0",
                    "enabled": True
                }
            )
        ],
        difficulty=1,
        requires_reasoning=False,
        metadata={"tags": ["basic", "interface", "configuration"]}
    ))
    
    # Scenario 2: VLAN configuration
    scenarios.append(Scenario(
        id="config_002",
        category=ScenarioCategory.CONFIGURATION,
        intent="Create VLAN 100 named 'Sales' on switch SW1 and assign ports Eth1 and Eth2 to it",
        context={
            "device_id": "SW1",
            "device_type": "switch",
            "available_vlans": [1, 10, 20]
        },
        expected_tools=[
            ToolCall(
                tool_name="configure_vlan",
                parameters={
                    "device_id": "SW1",
                    "vlan_id": 100,
                    "vlan_name": "Sales",
                    "interfaces": ["Eth1", "Eth2"]
                }
            )
        ],
        difficulty=2,
        requires_reasoning=False,
        metadata={"tags": ["vlan", "switch", "configuration"]}
    ))
    
    # Scenario 3: Connectivity troubleshooting
    scenarios.append(Scenario(
        id="troubleshoot_001",
        category=ScenarioCategory.TROUBLESHOOTING,
        intent="Check connectivity between router R1 and server 10.0.0.5, diagnose any issues",
        context={
            "device_id": "R1",
            "device_type": "router",
            "reported_issue": "Cannot reach server",
            "server_ip": "10.0.0.5"
        },
        expected_tools=[
            ToolCall(
                tool_name="ping_test",
                parameters={
                    "source_device": "R1",
                    "destination": "10.0.0.5",
                    "count": 4
                },
                order=0
            ),
            ToolCall(
                tool_name="traceroute",
                parameters={
                    "source_device": "R1",
                    "destination": "10.0.0.5",
                    "max_hops": 30
                },
                order=1
            )
        ],
        difficulty=2,
        requires_reasoning=True,
        metadata={"tags": ["troubleshooting", "connectivity", "diagnostics"]}
    ))
    
    # Scenario 4: Security ACL configuration
    scenarios.append(Scenario(
        id="security_001",
        category=ScenarioCategory.SECURITY,
        intent="Block all traffic from 192.168.50.0/24 to the web server at 10.0.1.10 on router R2",
        context={
            "device_id": "R2",
            "device_type": "router",
            "web_server": "10.0.1.10",
            "blocked_network": "192.168.50.0/24",
            "interface": "GigabitEthernet0/0"
        },
        expected_tools=[
            ToolCall(
                tool_name="configure_acl",
                parameters={
                    "device_id": "R2",
                    "acl_name": "BLOCK_SUBNET",
                    "acl_type": "extended",
                    "rules": [
                        {
                            "action": "deny",
                            "protocol": "ip",
                            "source": "192.168.50.0/24",
                            "destination": "10.0.1.10/32",
                            "port": "any"
                        }
                    ],
                    "interface": "GigabitEthernet0/0",
                    "direction": "in"
                }
            )
        ],
        difficulty=3,
        requires_reasoning=True,
        metadata={"tags": ["security", "acl", "firewall"]}
    ))
    
    # Scenario 5: Static routing configuration
    scenarios.append(Scenario(
        id="config_003",
        category=ScenarioCategory.CONFIGURATION,
        intent="Add a static route on router R1 to reach network 172.16.0.0/16 via next hop 10.0.0.1",
        context={
            "device_id": "R1",
            "device_type": "router",
            "target_network": "172.16.0.0/16",
            "gateway": "10.0.0.1"
        },
        expected_tools=[
            ToolCall(
                tool_name="configure_routing",
                parameters={
                    "device_id": "R1",
                    "routing_protocol": "static",
                    "destination_network": "172.16.0.0/16",
                    "next_hop": "10.0.0.1"
                }
            )
        ],
        difficulty=2,
        requires_reasoning=False,
        metadata={"tags": ["routing", "static", "configuration"]}
    ))
    
    # Scenario 6: Interface monitoring
    scenarios.append(Scenario(
        id="monitor_001",
        category=ScenarioCategory.MONITORING,
        intent="Check the status and bandwidth usage of interface GigabitEthernet0/2 on switch SW1",
        context={
            "device_id": "SW1",
            "device_type": "switch",
            "interface": "GigabitEthernet0/2",
            "concern": "High utilization reported"
        },
        expected_tools=[
            ToolCall(
                tool_name="get_interface_status",
                parameters={
                    "device_id": "SW1",
                    "interface_name": "GigabitEthernet0/2"
                },
                order=0
            ),
            ToolCall(
                tool_name="monitor_bandwidth",
                parameters={
                    "device_id": "SW1",
                    "interface_name": "GigabitEthernet0/2"
                },
                order=1
            )
        ],
        difficulty=2,
        requires_reasoning=True,
        metadata={"tags": ["monitoring", "bandwidth", "interface"]}
    ))
    
    # Scenario 7: Complex multi-step configuration
    scenarios.append(Scenario(
        id="config_004",
        category=ScenarioCategory.CONFIGURATION,
        intent="Set up SNMP monitoring on router R3 with community string 'public', version v2c, and trap receiver 192.168.1.100",
        context={
            "device_id": "R3",
            "device_type": "router",
            "monitoring_server": "192.168.1.100"
        },
        expected_tools=[
            ToolCall(
                tool_name="configure_snmp",
                parameters={
                    "device_id": "R3",
                    "community_string": "public",
                    "version": "v2c",
                    "trap_receivers": ["192.168.1.100"]
                }
            )
        ],
        difficulty=2,
        requires_reasoning=False,
        metadata={"tags": ["snmp", "monitoring", "configuration"]}
    ))
    
    # Scenario 8: QoS configuration
    scenarios.append(Scenario(
        id="optimization_001",
        category=ScenarioCategory.OPTIMIZATION,
        intent="Configure QoS policy 'VOICE_PRIORITY' on router R1 to prioritize VoIP traffic with high priority and 512kbps bandwidth on interface GigabitEthernet0/1",
        context={
            "device_id": "R1",
            "device_type": "router",
            "interface": "GigabitEthernet0/1",
            "traffic_type": "VoIP"
        },
        expected_tools=[
            ToolCall(
                tool_name="configure_qos",
                parameters={
                    "device_id": "R1",
                    "policy_name": "VOICE_PRIORITY",
                    "class_maps": [
                        {
                            "name": "VOIP",
                            "priority": 1,
                            "bandwidth": "512kbps"
                        }
                    ],
                    "interface": "GigabitEthernet0/1"
                }
            )
        ],
        difficulty=3,
        requires_reasoning=True,
        metadata={"tags": ["qos", "optimization", "voip"]}
    ))
    
    # Scenario 9: Backup configuration
    scenarios.append(Scenario(
        id="config_005",
        category=ScenarioCategory.CONFIGURATION,
        intent="Backup the configuration of router R1 to /backups/r1_config.txt",
        context={
            "device_id": "R1",
            "device_type": "router",
            "backup_path": "/backups/r1_config.txt"
        },
        expected_tools=[
            ToolCall(
                tool_name="backup_configuration",
                parameters={
                    "device_id": "R1",
                    "backup_location": "/backups/r1_config.txt"
                }
            )
        ],
        difficulty=1,
        requires_reasoning=False,
        metadata={"tags": ["backup", "configuration", "maintenance"]}
    ))
    
    # Scenario 10: Complex troubleshooting with routing
    scenarios.append(Scenario(
        id="troubleshoot_002",
        category=ScenarioCategory.TROUBLESHOOTING,
        intent="Investigate routing issues on router R2 - check routing table and ARP table to diagnose connectivity problems",
        context={
            "device_id": "R2",
            "device_type": "router",
            "reported_issue": "Intermittent connectivity to remote networks"
        },
        expected_tools=[
            ToolCall(
                tool_name="get_routing_table",
                parameters={
                    "device_id": "R2"
                },
                order=0
            ),
            ToolCall(
                tool_name="get_arp_table",
                parameters={
                    "device_id": "R2"
                },
                order=1
            )
        ],
        difficulty=3,
        requires_reasoning=True,
        metadata={"tags": ["troubleshooting", "routing", "advanced"]}
    ))
    
    return ScenarioDataset(scenarios)


if __name__ == "__main__":
    # Create and save example dataset
    from pathlib import Path
    
    dataset = create_example_scenarios()
    output_path = Path(__file__).parent.parent.parent / "data" / "scenarios.json"
    dataset.save_to_file(output_path)
    
    print(f"Created {len(dataset)} scenarios")
    print(f"Saved to: {output_path}")
    print("\nDataset statistics:")
    stats = dataset.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
