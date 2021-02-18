# Challenge - Introduction to Data Structures
 
The goal of this exercise is to learn about common types of data structures. You will learn how to recognize data types and how to interact with them using Python.
 
## Exercise Overview
 
### Prerequisites
 
You will need to have a Python interpreter installed on your machine. Optionally you can also use a code editor, like VSCode, to persist your work.
 
### Tasks
 
Submitting your solution for this challenge is optional - feel free to ask for help via email, chat, or at the open office hours if you get stuck!
 
#### Task 1 - Basic data types
 
Listed below are variables containing different data types. You need to identify each of the types.
 
1.
 
```python
hostname = "sALBEles09"
```
 
2. 
 
```python
vc_priority = 15
```
 
 
3. 
 
```python
cpu_load = 72.56
```
 
4.
 
```python
routing_enabled = True
```
 
5. 
   
```python
vlan_ids = [10, 300, 301, 302, 1400]
```
 
6. 
 
```python
vlans = {
    "10": "Production",
    "300": "Engineering",
    "301": "Voice",
    "302": "Printers"
}
```
  
> Hint: Above lines can be copy pasted into your Python interpreter, where you can use `type()` function to check variable type.
 
#### Task 2 - Accessing data - list
 
Given the below list, use Python to retrieve:
 
- Name of the 1st interface on the list.
- Name of the last interface on the list.
 
```python
interfaces = ["GigabitEthernet1", "GigabitEthernet2", "GigabitEthernet3", "GigabitEthernet4"]
```
 
#### Task 3 - Accessing data - dictionary
 
Given the below dictionary, write Python expressions retrieving values of:
 
- Five minute cpu load.
- Name of the process.
- Number of times the process was invoked.
 
What data type are each of these values?
 
```python
cpu_process = {
            "five_min_cpu": 0.46,
            "five_sec_cpu": 0.0,
            "invoked": 11390,
            "one_min_cpu": 0.59,
            "pid": 9,
            "process": "Check heaps",
            "runtime": 192629,
            "tty": 0,
            "usecs": 16912,
        }
```
 
#### Task 4 - Mixing data types
 
Copy the below Python statements into your interpreter and execute them. For each example answer the below questions:
 
- What is the result of the execution?
- Is the observed behavior something you expected?
- Can you think of an explanation for these results?
 
1.
 
```python
is_cisco = "False"
is_switch = "True"
is_cisco and is_switch
```
 
2.
 
```python
is_router = "False"
is_asr1000 = True
is_router or is_asr1000
```
 
3.
 
```python
hostname = "rtr-sydney-01-inet"
chassis_id = 1
hostname + chassis_id
```
 
4.
 
```python
response_time_sec = 2
delay_adjust = 0.1
response_time_sec - delay_adjust
```
 
5.
 
```python
vlans = ["5", "100", "120"]
vlans["5"]
```
 
6.
 
```python
intf_names = {"Eth0": "Uplink to core", "Eth24": "Tap switch"}
intf_names[0]
```
 
> Hint: Think about data types used in each of the statements. 
> Use `type()` to see the type of input variables and the result.
 
#### Task 5 - Accessing data in nested data structures
 
You are given the output of the `show spanning tree` command. You need to retrieve the following values from this data structure:
 
- STP port state of "Port-channel14".
- STP port priority of "Port-channel14".
- Priority of the root bridge.
- Address of the root bridge.
 
What type are each of the above values?
 
```python
show_spanning_tree = {
    "rapid_pvst": {
        "vlans": {
            200: {            
                "interfaces": {
                    "Port-channel14": {
                        "port_state": "forwarding",
                        "port_num": 2390,
                        "port_priority": 128,
                        "type": "P2p",
                        "cost": 3,
                        "role": "root"
                    }
                },
                "root": {
                    "hello_time": 2,
                    "priority": 24776,
                    "forward_delay": 15,
                    "max_age": 20,
                    "cost": 3,
                    "address": "58bf.eaff.e5b6",
                    "interface": "Port-channel14",
                    "port": 2390
                }
            }
        }
    }
}
```
 
> Hint: This is a deeply nested dictionary. You might need to traverse a few levels before you can access the final value.
> Think about key names for each of the levels you need to access.
 
#### Task 6 - Modifying data structure - list
 
BGP neighbors for one of your devices are stored in the below list. Neighbor "10.78.0.13" had IP conflict and needs to change its IP to "10.78.0.15". 
 
- Write a Python expression replacing the old IP value with the new one. 
 
**Do NOT** create a new list, work with the existing one.
 
```python
bgp_neighbors = ["10.40.0.5", "10.60.0.11", "10.78.0.13", "10.90.0.11", "10.90.0.13"]
```
 
> Hint: Values can be assigned to individual items on the list.
 
#### Task 7 - Modifying data structure - dictionary
 
Below NetBox site is being moved into production. 
 
- Update status of the site to "active" to reflect that.
 
```python
site = {
    "name": "Lessines",
    "status": {
        "value": "planned",
    },
    "region": {
        "name": "Belgium",
    }
}
```

> Hint: Similar to lists, values can be assigned to individual keys in a dictionary.
 
#### Task 8 - Bonus - converting unstructured text into structured data 1
 
Convert the below unstructured text to a structured data. Use a data structure type that fits this data best.
 
Record the final data structure using Python syntax. Assign it to `interface_state` variable.
 
Think about data types for each of the values you are capturing.
 
**Do NOT** use nested data structures.
 
```
GigabitEthernet0/0/0 is up, line protocol is up
  Internet address is 10.134.253.57/29
  Broadcast address is 255.255.255.255
  MTU is 1500 bytes
  Local Proxy ARP is disabled
  Split horizon is enabled
```
 
> Hint: This task is open-ended, you're free to choose any names that make sense to you.
 
#### Task 9 - Bonus - converting unstructured text into structured data 2
 
Convert the below unstructured text to nested data structure.
 
Multicast groups should be recorded in a list.
 
Record the final data structure using Python syntax. Assign it to `interface_state` variable.
 
```
GigabitEthernet0/2.1 is up, line protocol is up
  Internet address is 192.168.154.1/24
  MTU is 1500 bytes
  Broadcast address is 255.255.255.255
  Multicast reserved groups joined: 224.0.0.1 224.0.0.2 224.0.0.22 224.0.0.13
      224.0.0.5 224.0.0.6
```
 
> Hint: You're free to choose names in your data structures that feel most appropriate to you.
 
#### Task 10 - Bonus - Exploring JSON data
 
In this task you will explore, using Python, JSON data describing single device, returned by NetBox API.
 
This is an open-ended task. Follow instructions below to load data into your Python interpreter.
 
Try to access values of different attributes at varying levels of nesting. Investigate data types for values you’re accessing.

##### Steps for loading data

- Navigate to the directory named `files` contained within the challenge directory.

For example:

```
 /home/przemek/enablement/enablement-program-baxter/challenges/09-data-structures
❯ cd files
❯ pwd
/home/przemek/enablement/enablement-program-baxter/challenges/09-data-structures/files
```
 
- Once you're in the `files` directory, execute the below command to load JSON data and launch the Python interpreter.
 
```
python -i netbox_device.py
```
 
You should see output similar to the one below.
 
```python
❯ python -i netbox_device.py
Loaded JSON data into 'nb_device' variable.

You can use 'pp(nb_device)' to display all of the data.
>>>
```
 
- Loaded JSON data is assigned to the `nb_device` variable. You can use the `pp(nb_device)` statement to show you the structure of the data.
 
 
### Reference Enablement Material
 
- Introduction to Data Structures
 
> Note: Recordings of the relevant sessions can be found online at: https://training.networktocode.com/ 
