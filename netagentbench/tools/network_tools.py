"""
Network automation tool definitions.
"""

from typing import Dict, Any, List

# Network tool definitions compatible with OpenAI function calling format
NETWORK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "configure_interface",
            "description": "Configure a network interface with IP address, subnet mask, and other settings",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "interface_name": {
                        "type": "string",
                        "description": "The name of the interface (e.g., 'GigabitEthernet0/1', 'eth0')"
                    },
                    "ip_address": {
                        "type": "string",
                        "description": "IP address to assign to the interface"
                    },
                    "subnet_mask": {
                        "type": "string",
                        "description": "Subnet mask for the interface"
                    },
                    "enabled": {
                        "type": "boolean",
                        "description": "Whether the interface should be enabled",
                        "default": True
                    }
                },
                "required": ["device_id", "interface_name", "ip_address", "subnet_mask"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "configure_routing",
            "description": "Configure static or dynamic routing on a network device",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "routing_protocol": {
                        "type": "string",
                        "enum": ["static", "ospf", "bgp", "eigrp", "rip"],
                        "description": "The routing protocol to configure"
                    },
                    "destination_network": {
                        "type": "string",
                        "description": "Destination network in CIDR notation"
                    },
                    "next_hop": {
                        "type": "string",
                        "description": "Next hop IP address or interface"
                    },
                    "metric": {
                        "type": "integer",
                        "description": "Routing metric/cost"
                    }
                },
                "required": ["device_id", "routing_protocol", "destination_network"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "configure_vlan",
            "description": "Create and configure VLANs on a network switch",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "vlan_id": {
                        "type": "integer",
                        "description": "VLAN ID (1-4094)"
                    },
                    "vlan_name": {
                        "type": "string",
                        "description": "Name of the VLAN"
                    },
                    "interfaces": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of interfaces to assign to this VLAN"
                    }
                },
                "required": ["device_id", "vlan_id", "vlan_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "configure_acl",
            "description": "Configure Access Control List (ACL) rules for security policies",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "acl_name": {
                        "type": "string",
                        "description": "Name of the ACL"
                    },
                    "acl_type": {
                        "type": "string",
                        "enum": ["standard", "extended"],
                        "description": "Type of ACL"
                    },
                    "rules": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["permit", "deny"]},
                                "protocol": {"type": "string"},
                                "source": {"type": "string"},
                                "destination": {"type": "string"},
                                "port": {"type": "string"}
                            }
                        },
                        "description": "List of ACL rules"
                    },
                    "interface": {
                        "type": "string",
                        "description": "Interface to apply the ACL"
                    },
                    "direction": {
                        "type": "string",
                        "enum": ["in", "out"],
                        "description": "Direction to apply ACL"
                    }
                },
                "required": ["device_id", "acl_name", "acl_type", "rules"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_interface_status",
            "description": "Get the current status and statistics of a network interface",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "interface_name": {
                        "type": "string",
                        "description": "The name of the interface to query"
                    }
                },
                "required": ["device_id", "interface_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_device_info",
            "description": "Get general information about a network device",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    }
                },
                "required": ["device_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ping_test",
            "description": "Perform a ping test to check network connectivity",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_device": {
                        "type": "string",
                        "description": "Device to ping from"
                    },
                    "destination": {
                        "type": "string",
                        "description": "IP address or hostname to ping"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of ping packets to send",
                        "default": 4
                    }
                },
                "required": ["source_device", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "traceroute",
            "description": "Perform a traceroute to analyze network path",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_device": {
                        "type": "string",
                        "description": "Device to run traceroute from"
                    },
                    "destination": {
                        "type": "string",
                        "description": "IP address or hostname to trace"
                    },
                    "max_hops": {
                        "type": "integer",
                        "description": "Maximum number of hops",
                        "default": 30
                    }
                },
                "required": ["source_device", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_routing_table",
            "description": "Retrieve the routing table from a network device",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "protocol": {
                        "type": "string",
                        "enum": ["all", "static", "ospf", "bgp", "eigrp"],
                        "description": "Filter by routing protocol"
                    }
                },
                "required": ["device_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_arp_table",
            "description": "Retrieve the ARP table from a network device",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    }
                },
                "required": ["device_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "monitor_bandwidth",
            "description": "Monitor bandwidth usage on an interface",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "interface_name": {
                        "type": "string",
                        "description": "The name of the interface to monitor"
                    },
                    "duration": {
                        "type": "integer",
                        "description": "Duration in seconds to monitor"
                    }
                },
                "required": ["device_id", "interface_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "configure_qos",
            "description": "Configure Quality of Service (QoS) policies",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "policy_name": {
                        "type": "string",
                        "description": "Name of the QoS policy"
                    },
                    "class_maps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "priority": {"type": "integer"},
                                "bandwidth": {"type": "string"}
                            }
                        },
                        "description": "Traffic classes and their QoS settings"
                    },
                    "interface": {
                        "type": "string",
                        "description": "Interface to apply the QoS policy"
                    }
                },
                "required": ["device_id", "policy_name", "class_maps"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "backup_configuration",
            "description": "Backup device configuration",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "backup_location": {
                        "type": "string",
                        "description": "Location to store the backup"
                    }
                },
                "required": ["device_id", "backup_location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "restore_configuration",
            "description": "Restore device configuration from backup",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "backup_file": {
                        "type": "string",
                        "description": "Path to the backup file"
                    }
                },
                "required": ["device_id", "backup_file"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "configure_snmp",
            "description": "Configure SNMP monitoring",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The identifier of the network device"
                    },
                    "community_string": {
                        "type": "string",
                        "description": "SNMP community string"
                    },
                    "version": {
                        "type": "string",
                        "enum": ["v1", "v2c", "v3"],
                        "description": "SNMP version"
                    },
                    "trap_receivers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of SNMP trap receiver IP addresses"
                    }
                },
                "required": ["device_id", "community_string", "version"]
            }
        }
    }
]


def get_tool_by_name(tool_name: str) -> Dict[str, Any]:
    """
    Get tool definition by name.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Tool definition dictionary
    """
    for tool in NETWORK_TOOLS:
        if tool["function"]["name"] == tool_name:
            return tool
    raise ValueError(f"Tool '{tool_name}' not found")


def get_all_tool_names() -> List[str]:
    """Get list of all available tool names."""
    return [tool["function"]["name"] for tool in NETWORK_TOOLS]
