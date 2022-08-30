# Spine-02
# Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [Name Servers](#name-servers)
  - [Clock Settings](#clock-settings)
  - [NTP](#ntp)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
- [Monitoring](#monitoring)
  - [Logging](#logging)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Configuration](#internal-vlan-allocation-policy-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
- [Filters](#filters)
  - [Peer Filters](#peer-filters)
  - [Prefix-lists](#prefix-lists)
- [ACL](#acl)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [Quality Of Service](#quality-of-service)

# Management

## Management Interfaces

### Management Interfaces Summary

#### IPv4

| Management Interface | description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 192.168.22.192/24 | 192.168.22.1 |

#### IPv6

| Management Interface | description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | oob_management | oob | MGMT | -  | - |

### Management Interfaces Device Configuration

```eos
!
interface Management1
   description oob_management
   no shutdown
   vrf MGMT
   ip address 192.168.22.192/24
```

## Name Servers

### Name Servers Summary

| Name Server | Source VRF |
| ----------- | ---------- |
| 8.8.8.8 | MGMT |

### Name Servers Device Configuration

```eos
ip name-server vrf MGMT 8.8.8.8
```

## Clock Settings

### Clock Timezone Settings

Clock Timezone is set to **Asia/Seoul**.

### Clock Configuration

```eos
!
clock timezone Asia/Seoul
```

## NTP

### NTP Summary

#### NTP Local Interface

| Interface | VRF |
| --------- | --- |
| Management1 | MGMT |

#### NTP Servers

| Server | VRF | Preferred | Burst | iBurst | Version | Min Poll | Max Poll | Local-interface | Key |
| ------ | --- | --------- | ----- | ------ | ------- | -------- | -------- | --------------- | --- |
| 0.fr.pool.ntp.org | MGMT | True | - | - | - | - | - | - | - |
| 1.fr.pool.ntp.org | MGMT | False | - | - | - | - | - | - | - |

### NTP Device Configuration

```eos
!
ntp local-interface vrf MGMT Management1
ntp server vrf MGMT 0.fr.pool.ntp.org prefer
ntp server vrf MGMT 1.fr.pool.ntp.org
```

## Management API HTTP

### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

### Management API HTTP Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

# Authentication

## Local Users

### Local Users Summary

| User | Privilege | Role |
| ---- | --------- | ---- |
| admin | 15 | network-admin |
| ansible | 15 | network-admin |

### Local Users Device Configuration

```eos
!
username admin privilege 15 role network-admin secret sha512 $6$sbSVn6IgN2A7VIJJ$8g/z9ibMbFlO06jbpowU/PyB9kJvIgPNeSVyXjjanW8eftykpP7S32CFEdmb0nj0D8JXOKUNWe97T2wNvWSbm1
username ansible privilege 15 role network-admin secret sha512 $6$88e4YP9cN86RUUUZ$LBzKr2P.tfRkEZja4srfLK3t8TXCKx//t1LM59B6sr7AujC2HFTyKAsHZCxV/WOzHE/e7yrdlpMQxbaq/KW370
```

# Monitoring

## Logging

### Logging Servers and Features Summary

| Type | Level |
| -----| ----- |
| Console | informational |
| Monitor | informational |
| Buffer | 1000 |
| Synchronous | all |

### Logging Servers and Features Device Configuration

```eos
!
logging buffered 1000
logging console informational
logging monitor informational
logging synchronous level all
```

# Spanning Tree

## Spanning Tree Summary

STP mode: **none**

## Spanning Tree Device Configuration

```eos
!
spanning-tree mode none
```

# Internal VLAN Allocation Policy

## Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

## Internal VLAN Allocation Policy Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

# Interfaces

## Ethernet Interfaces

### Ethernet Interfaces Summary

#### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |

*Inherited from Port-Channel Interface

#### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | Connection to Leaf-01-Ethernet2 | routed | - | 100.100.0.2/31 | default | 1500 | false | - | - |
| Ethernet2 | Connection to Leaf-02-Ethernet2 | routed | - | 100.100.0.6/31 | default | 1500 | false | - | - |
| Ethernet3 | Connection to Leaf-03-Ethernet2 | routed | - | 100.100.0.10/31 | default | 1500 | false | - | - |
| Ethernet4 | Connection to Leaf-04-Ethernet2 | routed | - | 100.100.0.14/31 | default | 1500 | false | - | - |
| Ethernet5 | Connection to BL-01-Ethernet2 | routed | - | 100.100.0.18/31 | default | 1500 | false | - | - |
| Ethernet6 | Connection to BL-02-Ethernet2 | routed | - | 100.100.0.22/31 | default | 1500 | false | - | - |

### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description Connection to Leaf-01-Ethernet2
   no shutdown
   mtu 1500
   no switchport
   ip address 100.100.0.2/31
!
interface Ethernet2
   description Connection to Leaf-02-Ethernet2
   no shutdown
   mtu 1500
   no switchport
   ip address 100.100.0.6/31
!
interface Ethernet3
   description Connection to Leaf-03-Ethernet2
   no shutdown
   mtu 1500
   no switchport
   ip address 100.100.0.10/31
!
interface Ethernet4
   description Connection to Leaf-04-Ethernet2
   no shutdown
   mtu 1500
   no switchport
   ip address 100.100.0.14/31
!
interface Ethernet5
   description Connection to BL-01-Ethernet2
   no shutdown
   mtu 1500
   no switchport
   ip address 100.100.0.18/31
!
interface Ethernet6
   description Connection to BL-02-Ethernet2
   no shutdown
   mtu 1500
   no switchport
   ip address 100.100.0.22/31
```

## Loopback Interfaces

### Loopback Interfaces Summary

#### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | RouterID_EVPN | default | 1.1.1.202/32 |

#### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | RouterID_EVPN | default | - |


### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description RouterID_EVPN
   no shutdown
   ip address 1.1.1.202/32
```

# Routing
## Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

## IP Routing

### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | true |
| MGMT | false |

### IP Routing Device Configuration

```eos
!
ip routing
no ip routing vrf MGMT
```
## IPv6 Routing

### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | false |
| MGMT | false |

## Static Routes

### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP             | Exit interface      | Administrative Distance       | Tag               | Route Name                    | Metric         |
| --- | ------------------ | ----------------------- | ------------------- | ----------------------------- | ----------------- | ----------------------------- | -------------- |
| MGMT | 0.0.0.0/0 | 192.168.22.1 | - | 1 | - | - | - |

### Static Routes Device Configuration

```eos
!
ip route vrf MGMT 0.0.0.0/0 192.168.22.1
```

## Router BGP

### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65000|  1.1.1.202 |

| BGP Tuning |
| ---------- |
| no bgp default ipv4-unicast |
| maximum-paths 8 ecmp 8 |

### Router BGP Peer Groups

#### EVPN

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Remote AS | 65000 |
| Listen range prefix | 1.1.1.0/24 |
| Next-hop unchanged | True |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

#### UNDERLAY

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65000 |
| Listen range prefix | 100.64.0.0/10 |
| Send community | all |
| Maximum routes | 12000 |

### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- |
| 1.1.1.1 | 65001 | default | - | Inherited from peer group EVPN | Inherited from peer group EVPN | - | Inherited from peer group EVPN | - |
| 1.1.1.2 | 65002 | default | - | Inherited from peer group EVPN | Inherited from peer group EVPN | - | Inherited from peer group EVPN | - |
| 1.1.1.3 | 65003 | default | - | Inherited from peer group EVPN | Inherited from peer group EVPN | - | Inherited from peer group EVPN | - |
| 1.1.1.4 | 65004 | default | - | Inherited from peer group EVPN | Inherited from peer group EVPN | - | Inherited from peer group EVPN | - |
| 1.1.1.5 | 65005 | default | - | Inherited from peer group EVPN | Inherited from peer group EVPN | - | Inherited from peer group EVPN | - |
| 1.1.1.6 | 65005 | default | - | Inherited from peer group EVPN | Inherited from peer group EVPN | - | Inherited from peer group EVPN | - |
| 100.100.0.3 | 65001 | default | - | Inherited from peer group UNDERLAY | Inherited from peer group UNDERLAY | - | - | - |
| 100.100.0.7 | 65002 | default | - | Inherited from peer group UNDERLAY | Inherited from peer group UNDERLAY | - | - | - |
| 100.100.0.11 | 65003 | default | - | Inherited from peer group UNDERLAY | Inherited from peer group UNDERLAY | - | - | - |
| 100.100.0.15 | 65004 | default | - | Inherited from peer group UNDERLAY | Inherited from peer group UNDERLAY | - | - | - |
| 100.100.0.19 | 65005 | default | - | Inherited from peer group UNDERLAY | Inherited from peer group UNDERLAY | - | - | - |
| 100.100.0.23 | 65005 | default | - | Inherited from peer group UNDERLAY | Inherited from peer group UNDERLAY | - | - | - |

### Router BGP EVPN Address Family

#### EVPN Peer Groups

| Peer Group | Activate |
| ---------- | -------- |
| EVPN | True |

### Router BGP Device Configuration

```eos
!
router bgp 65000
   router-id 1.1.1.202
   no bgp default ipv4-unicast
   maximum-paths 8 ecmp 8
   bgp listen range 1.1.1.0/24 peer-group EVPN peer-filter Leaf-Ass
   bgp listen range 100.64.0.0/10 peer-group UNDERLAY peer-filter Leaf-Ass
   neighbor EVPN peer group
   neighbor EVPN remote-as 65000
   neighbor EVPN next-hop-unchanged
   neighbor EVPN update-source Loopback0
   neighbor EVPN bfd
   neighbor EVPN ebgp-multihop 3
   neighbor EVPN send-community
   neighbor EVPN maximum-routes 0
   neighbor UNDERLAY peer group
   neighbor UNDERLAY remote-as 65000
   neighbor UNDERLAY send-community
   neighbor UNDERLAY maximum-routes 12000
   neighbor 1.1.1.1 peer group EVPN
   neighbor 1.1.1.1 remote-as 65001
   neighbor 1.1.1.1 description Leaf-01
   neighbor 1.1.1.2 peer group EVPN
   neighbor 1.1.1.2 remote-as 65002
   neighbor 1.1.1.2 description Leaf-02
   neighbor 1.1.1.3 peer group EVPN
   neighbor 1.1.1.3 remote-as 65003
   neighbor 1.1.1.3 description Leaf-03
   neighbor 1.1.1.4 peer group EVPN
   neighbor 1.1.1.4 remote-as 65004
   neighbor 1.1.1.4 description Leaf-04
   neighbor 1.1.1.5 peer group EVPN
   neighbor 1.1.1.5 remote-as 65005
   neighbor 1.1.1.5 description BL-01
   neighbor 1.1.1.6 peer group EVPN
   neighbor 1.1.1.6 remote-as 65005
   neighbor 1.1.1.6 description BL-02
   neighbor 100.100.0.3 peer group UNDERLAY
   neighbor 100.100.0.3 remote-as 65001
   neighbor 100.100.0.3 description Leaf-01
   neighbor 100.100.0.7 peer group UNDERLAY
   neighbor 100.100.0.7 remote-as 65002
   neighbor 100.100.0.7 description Leaf-02
   neighbor 100.100.0.11 peer group UNDERLAY
   neighbor 100.100.0.11 remote-as 65003
   neighbor 100.100.0.11 description Leaf-03
   neighbor 100.100.0.15 peer group UNDERLAY
   neighbor 100.100.0.15 remote-as 65004
   neighbor 100.100.0.15 description Leaf-04
   neighbor 100.100.0.19 peer group UNDERLAY
   neighbor 100.100.0.19 remote-as 65005
   neighbor 100.100.0.19 description BL-01
   neighbor 100.100.0.23 peer group UNDERLAY
   neighbor 100.100.0.23 remote-as 65005
   neighbor 100.100.0.23 description BL-02
   redistribute connected route-map RM-CONN-2-BGP
   !
   address-family evpn
      neighbor EVPN activate
   !
   address-family ipv4
      no neighbor EVPN activate
      neighbor UNDERLAY activate
```

# BFD

## Router BFD

### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 1200 | 1200 | 3 |

### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 1200 min-rx 1200 multiplier 3
```

# Multicast

# Filters

## Peer Filters

### Peer Filters Summary

#### Leaf-Ass

| Sequence | Match |
| -------- | ----- |
| 10 | as-range 65001-65200 result accept |

### Peer Filters Device Configuration

```eos
!
peer-filter Leaf-Ass
   10 match as-range 65001-65200 result accept
```

## Prefix-lists

### Prefix-lists Summary

#### Loopback

| Sequence | Action |
| -------- | ------ |
| 10 | permit 1.1.1.0/24 eq 32 |

### Prefix-lists Device Configuration

```eos
!
ip prefix-list Loopback
   seq 10 permit 1.1.1.0/24 eq 32
```

# ACL

# VRF Instances

## VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| MGMT | disabled |

## VRF Instances Device Configuration

```eos
!
vrf instance MGMT
```

# Quality Of Service
