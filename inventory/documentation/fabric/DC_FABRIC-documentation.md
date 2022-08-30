# DC_FABRIC

# Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

# Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision |
| --- | ---- | ---- | ------------- | -------- | -------------------------- |
| DC_FABRIC | l3leaf | BL-01 | 192.168.22.197/24 | vEOS | Provisioned |
| DC_FABRIC | l3leaf | BL-02 | 192.168.22.198/24 | vEOS | Provisioned |
| DC_FABRIC | l3leaf | Leaf-01 | 192.168.22.193/24 | vEOS | Provisioned |
| DC_FABRIC | l3leaf | Leaf-02 | 192.168.22.194/24 | vEOS | Provisioned |
| DC_FABRIC | l3leaf | Leaf-03 | 192.168.22.195/24 | vEOS | Provisioned |
| DC_FABRIC | l3leaf | Leaf-04 | 192.168.22.196/24 | vEOS | Provisioned |
| DC_FABRIC | spine | Spine-01 | 192.168.22.191/24 | vEOS | Provisioned |
| DC_FABRIC | spine | Spine-02 | 192.168.22.192/24 | vEOS | Provisioned |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

## Fabric Switches with inband Management IP
| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

# Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l3leaf | BL-01 | Ethernet1 | spine | Spine-01 | Ethernet5 |
| l3leaf | BL-01 | Ethernet2 | spine | Spine-02 | Ethernet5 |
| l3leaf | BL-01 | Ethernet7 | mlag_peer | BL-02 | Ethernet7 |
| l3leaf | BL-01 | Ethernet8 | mlag_peer | BL-02 | Ethernet8 |
| l3leaf | BL-02 | Ethernet1 | spine | Spine-01 | Ethernet6 |
| l3leaf | BL-02 | Ethernet2 | spine | Spine-02 | Ethernet6 |
| l3leaf | Leaf-01 | Ethernet1 | spine | Spine-01 | Ethernet1 |
| l3leaf | Leaf-01 | Ethernet2 | spine | Spine-02 | Ethernet1 |
| l3leaf | Leaf-02 | Ethernet1 | spine | Spine-01 | Ethernet2 |
| l3leaf | Leaf-02 | Ethernet2 | spine | Spine-02 | Ethernet2 |
| l3leaf | Leaf-03 | Ethernet1 | spine | Spine-01 | Ethernet3 |
| l3leaf | Leaf-03 | Ethernet2 | spine | Spine-02 | Ethernet3 |
| l3leaf | Leaf-04 | Ethernet1 | spine | Spine-01 | Ethernet4 |
| l3leaf | Leaf-04 | Ethernet2 | spine | Spine-02 | Ethernet4 |

# Fabric IP Allocation

## Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 100.100.0.0/30 | 4 | 0 | 0.0 % |

## Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| BL-01 | Ethernet1 | 100.100.0.25/31 | Spine-01 | Ethernet5 | 100.100.0.24/31 |
| BL-01 | Ethernet2 | 100.100.0.27/31 | Spine-02 | Ethernet5 | 100.100.0.26/31 |
| BL-02 | Ethernet1 | 100.100.0.29/31 | Spine-01 | Ethernet6 | 100.100.0.28/31 |
| BL-02 | Ethernet2 | 100.100.0.31/31 | Spine-02 | Ethernet6 | 100.100.0.30/31 |
| Leaf-01 | Ethernet1 | 100.100.0.9/31 | Spine-01 | Ethernet1 | 100.100.0.8/31 |
| Leaf-01 | Ethernet2 | 100.100.0.11/31 | Spine-02 | Ethernet1 | 100.100.0.10/31 |
| Leaf-02 | Ethernet1 | 100.100.0.13/31 | Spine-01 | Ethernet2 | 100.100.0.12/31 |
| Leaf-02 | Ethernet2 | 100.100.0.15/31 | Spine-02 | Ethernet2 | 100.100.0.14/31 |
| Leaf-03 | Ethernet1 | 100.100.0.17/31 | Spine-01 | Ethernet3 | 100.100.0.16/31 |
| Leaf-03 | Ethernet2 | 100.100.0.19/31 | Spine-02 | Ethernet3 | 100.100.0.18/31 |
| Leaf-04 | Ethernet1 | 100.100.0.21/31 | Spine-01 | Ethernet4 | 100.100.0.20/31 |
| Leaf-04 | Ethernet2 | 100.100.0.23/31 | Spine-02 | Ethernet4 | 100.100.0.22/31 |

## Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 1.1.1.0/30 | 4 | 2 | 50.0 % |

## Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| DC_FABRIC | BL-01 | 1.1.1.8/32 |
| DC_FABRIC | BL-02 | 1.1.1.9/32 |
| DC_FABRIC | Leaf-01 | 1.1.1.4/32 |
| DC_FABRIC | Leaf-02 | 1.1.1.5/32 |
| DC_FABRIC | Leaf-03 | 1.1.1.6/32 |
| DC_FABRIC | Leaf-04 | 1.1.1.7/32 |
| DC_FABRIC | Spine-01 | 1.1.1.1/32 |
| DC_FABRIC | Spine-02 | 1.1.1.2/32 |

## VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| --------------------- | ------------------- | ------------------ | ------------------ |
| 3.3.3.0/24 | 256 | 6 | 2.35 % |

## VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| DC_FABRIC | BL-01 | 3.3.3.8/32 |
| DC_FABRIC | BL-02 | 3.3.3.8/32 |
| DC_FABRIC | Leaf-01 | 3.3.3.4/32 |
| DC_FABRIC | Leaf-02 | 3.3.3.5/32 |
| DC_FABRIC | Leaf-03 | 3.3.3.6/32 |
| DC_FABRIC | Leaf-04 | 3.3.3.7/32 |
