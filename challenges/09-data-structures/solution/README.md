### Data Structures solution

# Challenge Exercise Solution Guide

## Introduction to Data Structures

In this challenge you are exploring data structures, and learning how to work with them using Python.

## Solution Walkthrough

#### Task 1 - Basic data types

In this task you are asked to identify different data types.

1.

```
hostname = "sALBEles09"
```

Here `hostname` holds the value of `"sALBEles09" `, which is a `string` date type. Notice quotation marks, `""`, around the word, which tell us this is a `string`.

2.

```
vc_priority = 15
```

You assign the value of `15` to `vc_priority`. The data type here is `integer` as `15` is a whole number.

3.

```
cpu_load = 72.56
```

This is a `float`, we can see it's a float because there is a decimal point in the number `72.56`.

4.

```
routing_enabled = True
```

This is a `boolean`. We use `boolean` type to represent truth values of logic. We can tell it's boolean because the word `True` is capitalized and is not enclosed in quotation marks.

5.

```
vlan_ids = [10, 300, 301, 302, 1400]
```

This data type is called `list` in Python. In other languages it might be also referred to as an `array`. 

We can tell it's a `list` because this is a comma `,`, separated collection of elements enclosed in square brackets `[]`.

6.

```
vlans = {
    "10": "Production",
    "300": "Engineering",
    "301": "Voice",
    "302": "Printers"
}
```

This data type is called `dictionary` in Python. In other languages it might be referred to as `hash`, `map` or `object`.

We can tell it's a `dictionary` because we have a comma `,` separated list of `key: value` pairs separated by colon `:`. And the collection is enclosed in curly braces `{}`.
 
#### Task 2 - Accessing data - list 
 
The below data structure is a `list` so you need to use index value using square brackets `[]` to retrieve corresponding values.

```
interfaces = ["GigabitEthernet1", "GigabitEthernet2", "GigabitEthernet3", "GigabitEthernet4"]
```

Below statements retrieve 1st and last interface on the list. Remember that list indexes start from `0`.

```
>>> interfaces[0]
'GigabitEthernet1'
>>> interfaces[3]
'GigabitEthernet4'
```

#### Task 3 - Accessing data - dictionary

The below data structure is a `dictionary` so you need to use the key name enclosed in square brackets `[]` to access the given value.

```
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

Below is an example of retrieving asked for values and their corresponding data types:

```
>>> cpu_process["five_min_cpu"]
0.46
>>> type(cpu_process["five_min_cpu"])
<class 'float'>
>>> cpu_process["process"]
'Check heaps'
>>> type(cpu_process["process"])
<class 'str'>
>>> cpu_process["invoked"]
11390
>>> type(cpu_process["invoked"])
<class 'int'>
```

#### Task 4 - Mixing data types

This task shows you the importance of understanding data types you're working with. When mixing data types some of the operations are not allowed, some generate unexpected results.

1. 

```
>>> is_cisco = "False"
>>> is_switch = "True"
>>> is_cisco and is_switch
'True'
```

At first glance the result of the operation should be `False` since we used logical `and` operator. Notice however that both of the arguments are of type `string` and not `boolean`. `"False"` and `"True"` have quotation marks around words which makes them strings.

Operator `and` behaves differently with `string` type than it does with `boolean` type. 

Once we use correct `boolean` types we get expected result:

```
>>> is_cisco = False
>>> is_switch = True
>>> is_cisco and is_switch
False
```

2.

This is similar to 1. but here one variable is of type `boolean` while the other is `string`. This is why the result of `or` operation is `"False"`. The result is actually a `string` and not `boolean`.

```
>>> is_router = "False"
>>> is_asr1000 = True
>>> is_router or is_asr1000
'False'
```

To get expected result change assign `boolean` value of `False` to `is_router`:

```
>>> is_router = False
>>> is_asr1000 = True
>>> is_router or is_asr1000
True
```
3.

You should get `TypeError` when executing the code. Adding `integer` type to `string` type is not allowed in Python and many other languages.

```
>>> hostname = "rtr-sydney-01-inet"
>>> chassis_id = 1
>>> hostname + chassis_id
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```

4.

You can generally mix `int` and `float` types together. Resulting value will be of type `float`.

```
>>> response_time_sec = 2
>>> delay_adjust = 0.1
>>> response_time_sec - delay_adjust
1.9
```

5.

You should get `TypeError` when executing the code. List items need to be accessed by corresponding index number. 

```
>>> vlans = ["5", "100", "120"]
>>> vlans["5"]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: list indices must be integers or slices, not str
```

To get the item `"5"` from the below list we should use its index, `0`. Index value has to be an integer and not a string.

```python
>>> vlans[0]
'5'
```

6.

You should get `KeyError` when executing the code. This data structure is a `dictionary` so you need to use a key name to access the value of interest.

```python
>>> intf_names = {"Eth0": "Uplink to core", "Eth24": "Tap switch"}
>>> intf_names[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 0
```

Instead of `0` use the key name `"Eth0"` to retrieve the corresponding value.

```python
>>> intf_names["Eth0"]
'Uplink to core'
```

> Note that `0` could be used as a key, but you can't treat it like a list index, it would be just another key name.

#### Task 5 - Accessing data in nested data structures

Output you work with in this task is a deeply nested data structure composed of many dictionaries.

To access requested values you need to navigate the hierarchy of data structures from the outermost to the innermost. At each level you need to think of the key name that contains the data structure nested below it.

Below we retrieve values requested in the task and check their data types.

```python
>>> show_spanning_tree["rapid_pvst"]["vlans"][200]["interfaces"]["Port-channel14"]["port_state"]
'forwarding'
>>> type(show_spanning_tree["rapid_pvst"]["vlans"][200]["interfaces"]["Port-channel14"]["port_state"])
<class 'str'>
>>>
>>> show_spanning_tree["rapid_pvst"]["vlans"][200]["interfaces"]["Port-channel14"]["port_priority"]
128
>>> type(show_spanning_tree["rapid_pvst"]["vlans"][200]["interfaces"]["Port-channel14"]["port_priority"])
<class 'int'>
>>>
>>> show_spanning_tree["rapid_pvst"]["vlans"][200]["root"]["priority"]
24776
>>> type(show_spanning_tree["rapid_pvst"]["vlans"][200]["root"]["priority"])
<class 'int'>
>>>
>>> show_spanning_tree["rapid_pvst"]["vlans"][200]["root"]["address"]
'58bf.eaff.e5b6'
>>> type(show_spanning_tree["rapid_pvst"]["vlans"][200]["root"]["address"])
<class 'str'>
```

This task shows the importance of understanding container data structures like `list` and `dictionary`. Both of those types can be found at different levels of nesting and you need to know how to traverse the hierarchy to access values of interest.

#### Task 6 - Modifying data structure - list

In this task you're asked to make an in-place update of the list.

To do this you need to use index and square brackets `[]` to point to the item you want to replace. Then you assign new value to that index.

```python
>>> bgp_neighbors = ["10.40.0.5", "10.60.0.11", "10.78.0.13", "10.90.0.11", "10.90.0.13"]
>>> bgp_neighbors[2] = "10.78.0.15"
>>> bgp_neighbors
['10.40.0.5', '10.60.0.11', '10.78.0.15', '10.90.0.11', '10.90.0.13']
```

#### Task 7 - Modifying data structure - dictionary

In this task you're updating the value of one of the keys in an existing dictionary.

To do this update you need to point to the item by navigating the hierarchy of this nested data structure. Then you assign a new value to the item referenced by that pointer.

```python
>>> site = {
...     "name": "Lessines",
...     "status": {
...         "value": "planned",
...     },
...     "region": {
...         "name": "Belgium",
...     }
... }
>>> site["status"]["value"] = "active"
>>> site
{'name': 'Lessines', 'status': {'value': 'active'}, 'region': {'name': 'Belgium'}}
```

#### Task 8 - Bonus - converting unstructured text into structured data 1

In this task you're asked to build data structure from unstructured text. You're asked to use a data type that fits input text the best and you're not allowed to use nested data structures.

You should notice that the input text contains the name of an interface and various attributes describing its state. For ease of retrieval these attributes would be best represented by key names, so you should build a dictionary and convert attributes into `key: value` pairs.

Choice of key names is arbitrary, below is one of possible solutions.

```python
interface_state = {
    "name": "GigabitEthernet0/0/0",
    "status": "up",
    "ip_address": "10.134.253.57/29",
    "broadcast_address": "255.255.255.255",
    "mtu": 1500,
    "local_proxy_arp_enabled": False,
    "split_horizon_enabled": True
}
```

#### Task 9 - Bonus - converting unstructured text into structured data 2

In this task you're asked to convert unstructured text into structured data. This task is similar to task `8.` but here we are asking to record values of one of the attributes as a `list`.

In this task you should create a `dictionary`. Key names are again arbitrary but the key name you used to record multicast groups should contain a nested `list` with its items being multicast groups.

Below is an example solution.

```python
interface_status = {
    "name": "GigabitEthernet0/2.1",
    "status": "up",
    "ip_address": "192.168.154.1/24",
    "broadcast_address": "255.255.255.255",
    "mtu": 1500,
    "mcast_reserved_grups_joined": [
        "224.0.0.1",
        "224.0.0.2",
        "224.0.0.22",
        "224.0.0.13",
        "224.0.0.5",
        "224.0.0.6",
    ]
}
```

#### Task 10 - Bonus - Exploring JSON data

In this task you have an opportunity to explore JSON data returned from the production system.

Command `python -i netbox_device.py` will load JSON data for one device. That JSON payload has been returned by NetBox API. This data is assigned to `nb_device` variable to allow you easy access.

Some examples of working with the data are below.

- Name of the device:

```python
>>> nb_device["name"]
'sALBEles09'
```

- Device model:

```python
>>> nb_device["device_type"]["display_name"]
'Cisco C9300-48P'
```

- Device role:

```python
>>> nb_device["device_role"]["name"]
'switch--access-lan'
```

- Primary IP of this device:

```python
>>> nb_device["primary_ip"]["address"]
'10.101.122.26/24'
```

- Site where this device is located:

```python
>>> nb_device["site"]["name"]
'Lessines'
```
