### Batfish Solution

# Challenge Exercise Solution Guide

## Introduction to Batfish

The goal of this exercise is to learn about the common operations in Batfish. In You will learn how to interact with Batfish and work with its output.
 
For certain parts of this challenge you will need to refer to https://pybatfish.readthedocs.io/en/latest/questions.html to understand the question that we will need to ask. 

## Solution Walkthrough

#### Task 1 - Snapshot Import
 
In this question you were asked:
> From the helper file `bf_snapshot_importer.py` can you determine the line where the snapshot is initialized using the supplied snapshot path.
 
From looking into this file you will see that the following line is used to initialize the snapshot.
```python
def main(network, snapshot_path, snapshot, bf_host):
    ...

    bf_set_network(network)
=>  bf_session.init_snapshot(snapshot_path, name=snapshot, overwrite=True)
```
#### Task 2 - Snapshot Validation

In this question you were asked: 
> Use Batfish to:
> * obtain a parsing summary of the snapshot files.
> * confirm the problematic configuration lines for each of the configurations. 

To see the parsing summary, we use the following command:
```
bfq.fileParseStatus().answer().frame()
                   File_Name                  Status                          Nodes
0          configs/leaf1.cfg  PARTIALLY_UNRECOGNIZED                      ['leaf1']
1          configs/leaf2.cfg  PARTIALLY_UNRECOGNIZED                      ['leaf2']
2         configs/spine1.cfg  PARTIALLY_UNRECOGNIZED                     ['spine1']
3         configs/spine2.cfg  PARTIALLY_UNRECOGNIZED                     ['spine2']
4         hosts/server1.json                  PASSED                    ['server1']
5         hosts/server2.json                  PASSED                    ['server2']
6  iptables/server1.iptables                  PASSED  ['iptables/server1.iptables']
7  iptables/server2.iptables                  PASSED  ['iptables/server2.iptables']
```

To see the individual configuration elements that Batfish is unable to parse we use:
```
bfq.parseWarning().answer().frame()
              Filename Line                                               Text                                     Parser_Context                      Comment
0    configs/leaf1.cfg   20                         no password strength-check          [s_no statement cisco_nxos_configuration]  This syntax is unrecognized
1    configs/leaf1.cfg   30  rmon event 1 log trap public description FATAL...                         [cisco_nxos_configuration]  This syntax is unrecognized
2    configs/leaf1.cfg   31  rmon event 2 log trap public description CRITI...                         [cisco_nxos_configuration]  This syntax is unrecognized
3    configs/leaf1.cfg   32  rmon event 3 log trap public description ERROR...                         [cisco_nxos_configuration]  This syntax is unrecognized
4    configs/leaf1.cfg   33  rmon event 4 log trap public description WARNI...                         [cisco_nxos_configuration]  This syntax is unrecognized
5    configs/leaf1.cfg   34  rmon event 5 log trap public description INFOR...                         [cisco_nxos_configuration]  This syntax is unrecognized
...
```

#### Task 3 - MTU Validation

In this question you were asked:
> Use Batfish to confirm the MTU for each of the interfaces within our snapshot.
 
To validate the MTUs we can use the `interfaceProperites` question as shown below. As you will see all the interfaces are set to `1500` bytes.
```
bfq.interfaceProperties(properties="MTU").answer().frame()
                Interface   MTU
0    spine1[Ethernet1/21]  1500
1    spine2[Ethernet1/24]  1500
2    spine1[Ethernet1/23]  1500
3           server1[eth1]  1500
4    spine1[Ethernet1/22]  1500
...
```

#### Task 4 - OSPF Validation

In this question you were asked: 
> Use Batfish to validate all OSPF adjacencies are correctly established. If they are not, please confirm reason.

To validate the OSPF sessions we use `ospfSessionCompatibility()`. This will also tell us the reason for the session failure.
We will see there is an OSPF area mismatch between the 2 neighbors.
**Note:** All the possible status values can be found at https://pybatfish.readthedocs.io/en/latest/specifiers.html#ospf-session-status-specifier.

```
bfq.ospfSessionCompatibility().answer().frame()
              Interface      VRF          IP Area     Remote_Interface Remote_VRF   Remote_IP Remote_Area Session_Status
0    leaf2[Ethernet1/3]  default  10.1.128.2    0  spine1[Ethernet1/3]    default  10.1.128.1           0    ESTABLISHED
1   spine1[Ethernet1/3]  default  10.1.128.1    0   leaf2[Ethernet1/3]    default  10.1.128.2           0    ESTABLISHED
2   spine2[Ethernet1/1]  default  10.2.128.1    0   leaf2[Ethernet1/1]    default  10.2.128.2           0    ESTABLISHED
3   spine2[Ethernet1/3]  default    10.2.0.1    0   leaf1[Ethernet1/3]    default    10.2.0.2           0    ESTABLISHED
4   spine2[Ethernet1/4]  default    10.2.0.5    0   leaf1[Ethernet1/4]    default    10.2.0.6           0    ESTABLISHED
5    leaf2[Ethernet1/4]  default    10.1.0.2    0  spine1[Ethernet1/4]    default    10.1.0.1           0    ESTABLISHED
6   spine1[Ethernet1/2]  default  10.0.128.1    0   leaf1[Ethernet1/2]    default  10.0.128.2           2  AREA_MISMATCH
7    leaf1[Ethernet1/3]  default    10.2.0.2    0  spine2[Ethernet1/3]    default    10.2.0.1           0    ESTABLISHED
8    leaf1[Ethernet1/4]  default    10.2.0.6    0  spine2[Ethernet1/4]    default    10.2.0.5           0    ESTABLISHED
9   spine2[Ethernet1/2]  default  10.2.128.5    0   leaf2[Ethernet1/2]    default  10.2.128.6           0    ESTABLISHED
10   leaf2[Ethernet1/1]  default  10.2.128.2    0  spine2[Ethernet1/1]    default  10.2.128.1           0    ESTABLISHED
11  spine1[Ethernet1/4]  default    10.1.0.1    0   leaf2[Ethernet1/4]    default    10.1.0.2           0    ESTABLISHED
12   leaf1[Ethernet1/2]  default  10.0.128.2    2  spine1[Ethernet1/2]    default  10.0.128.1           0  AREA_MISMATCH
13   leaf2[Ethernet1/2]  default  10.2.128.6    0  spine2[Ethernet1/2]    default  10.2.128.5           0    ESTABLISHED
```
