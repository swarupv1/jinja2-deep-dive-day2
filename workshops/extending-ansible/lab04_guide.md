# Extending Ansible - Lab 04

Whenever you're working with data in Ansible either comparing data, transforming data, or analzying it, you'll find that performing those operations within Python (in a filter) can save quite a bit of time in the long run for other engineers focused on writing playbooks.

In this lab exercise, you will create a custom filter for Ansible that compares intended interface state to the operational state pulled from an NXOS switch. 

## Task 1 - Reviewing the Filter Code

To start with, you will create a new filter a review the provided code and data structures.

### Step 1

In your terminal on the lab workstation, change into the `/home/ntc/labs/lab04` folder, creating it if it doesn't exist.

```
ntc@ntc-training:~$ mkdir -p /home/ntc/labs/lab04
ntc@ntc-training:~$ cd /home/ntc/labs/lab04
ntc@ntc-training:lab04$
```

### Step 2

Create a folder named `filter_plugins` and in it a file called `verify_intended_state.py`.

```
ntc@ntc-training:lab04$ mkdir filter_plugins
ntc@ntc-training:lab04$ touch filter_plugins/verify_intended_state.py
ntc@ntc-training:lab04$ tree
.
└── filter_plugins
    └── verify_intended_state.py

1 directory, 1 file
```

### Step 3

Edit the `verify_intended_state.py` file and paste in the following content. This is the full script and you will explore it in the following steps (keep the full script and this guide side-by-side if possible).

```py
from ansible import errors


class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "verify_intended_state": FilterModule.verify_intended_state,
        }

    @staticmethod
    def verify_intended_state(operational, intended):
        """Returns a pass/fail comparison of intended and operational state.

        Compares NXOS (operational) state (from the show int brief command)
        to a provided list of interface and state mappings (intended)

        SAMPLE intended
        [
            {
                "name": "Ethernet1/1",
                "state": "up"
            },
            {
                "name": "mgmt0",
                "state": "up"
            },
        ]

        SAMPLE operational
        {
            "TABLE_interface": {
                "ROW_interface": [
                    {
                        "interface": "mgmt0",
                        "state": "up",
                        "ip_addr": "10.0.0.15",
                        "speed": "1000",
                        "mtu": "1500"
                    },
                    {
                        "interface": "Ethernet1/1",
                        "vlan": "1",
                        "type": "eth",
                        "portmode": "access",
                        "state": "up",
                        "state_rsn_desc": "none",
                        "speed": "1000",
                        "ratemode": "D"
                    },
                ]
            }
        }


        Args:
            operational (dict): the output of `show int brief | json`
            intended (list): a list of interfaces and their states

        Returns:
            dict: A dictionary containing the lists of interfaces that
                  passed and failed verification
        """
        # First prepare the data coming from NXOS for ease of lookup
        # Change from a list of interface dictionaries to a dictionary
        # keyed on the interface name
        oper_keyed = {}
        for oper_intf in operational["TABLE_interface"]["ROW_interface"]:
            oper_keyed[oper_intf["interface"]] = oper_intf

        pass_list = []
        fail_list = []
        # This is a list of name/state pairs describing the intended state
        # of a bunch of interfaces (not necessarily the same set).
        for interface in intended:
            # Look for the interface name in the operational dictionary
            # as an exact match only - with UNKNOWN as a safe default
            oper_intf = oper_keyed.get(interface["name"])
            if oper_intf:
                oper_state = oper_intf.get("state", "UNKNOWN")
            else:
                oper_state = "UNKNOWN"

            # Compare operational to intended
            if oper_state != interface["state"]:
                fail_list.append(interface["name"])
            else:
                pass_list.append(interface["name"])

        # Return a dictionary with two keys containing the lists for easy
        # subsequent parsing
        return {"pass": pass_list, "fail": fail_list}
```

### Step 4

Observe the script's general structure - the `class FilterModule` containing the necessary binding for Ansible and the actual `verify_intended_state` function that performs the work.

In this script, you may notice that the docstring (the text between the triple quotes `"""` at the beginning of the function block) for the `verify_intended_state` function is a lot more descriptive than before (and has examples!). This is highly recommended when your functions perform work on complex data structures.

Take some time to read through the docstring.

### Step 5

As you can see, the `operational` and `intended` data structures are fairly different - this is quite common, especially as your data model will many times try to be vendor or OS independent. This means that you need to perfom various transformation operations in order to correlate information from both of these structures.

The first step is to make the `operational` data easier to search through. You may have noticed that it contains a **list** of interfaces, which means that if you ever needed to look up an interface in this list, you had to search through the whole list every time (this may become computationally expensive with large datasets).

In order to make this lookup process more optimal, the first step is to convert this list of interfaces into a dictionary, which is the perfect construct for direct single item access (there is a trade-off as always, in this case memory usage will be higher, but computational complexity lower).

```py
        # First prepare the data coming from NXOS for ease of lookup
        # Change from a list of interface dictionaries to a dictionary
        # keyed on the interface name
        oper_keyed = {}
        for oper_intf in operational["TABLE_interface"]["ROW_interface"]:
            oper_keyed[oper_intf["interface"]] = oper_intf
```

### Step 6

To see what is the exact end-result of the code, you may quickly load it into a Python interpreter and explore the results of applying it to the example from the docstring.

```
ntc@ntc-training:lab04$ python3
Python 3.6.8 (default, Jun 11 2019, 01:16:11)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>>
>>> operational = {
...             "TABLE_interface": {
...                 "ROW_interface": [
...                     {
...                         "interface": "mgmt0",
...                         "state": "up",
...                         "ip_addr": "10.0.0.15",
...                         "speed": "1000",
...                         "mtu": "1500"
...                     },
...                     {
...                         "interface": "Ethernet1/1",
...                         "vlan": "1",
...                         "type": "eth",
...                         "portmode": "access",
...                         "state": "up",
...                         "state_rsn_desc": "none",
...                         "speed": "1000",
...                         "ratemode": "D"
...                     },
...                 ]
...             }
...         }
>>> oper_keyed = {}
>>> for oper_intf in operational["TABLE_interface"]["ROW_interface"]:
...     oper_keyed[oper_intf["interface"]] = oper_intf
...
>>> import json
>>> print(json.dumps(oper_keyed, indent=4))
{
    "mgmt0": {
        "interface": "mgmt0",
        "state": "up",
        "ip_addr": "10.0.0.15",
        "speed": "1000",
        "mtu": "1500"
    },
    "Ethernet1/1": {
        "interface": "Ethernet1/1",
        "vlan": "1",
        "type": "eth",
        "portmode": "access",
        "state": "up",
        "state_rsn_desc": "none",
        "speed": "1000",
        "ratemode": "D"
    }
}
>>> oper_keyed["mgmt0"]
{'interface': 'mgmt0', 'state': 'up', 'ip_addr': '10.0.0.15', 'speed': '1000', 'mtu': '1500'}
```

Observe how you can now extract a single specific interface with just one operation `oper_keyed["mgmt0"]`.

### Step 7

That was the hardest part. What comes after it is building two lists: `pass_list` to contain interface names that match the intended with the operational state - and `fail_list` for those that don't match. The state is simply either `up` or `down`.

Since the `intended` structure is a list of interfaces, the code will loop through them one by one and try to find if they exist within the `oper_keyed` data. As per the above steps, this is now easily achieved with one dictionary lookup.

```py
        for interface in intended:
            # Look for the interface name in the operational dictionary
            # as an exact match only - with UNKNOWN as a safe default
            oper_intf = oper_keyed.get(interface["name"])
            if oper_intf:
                oper_state = oper_intf.get("state", "UNKNOWN")
            else:
                oper_state = "UNKNOWN"
```

If the interface is found in the operational data, then extract its operational state from the underlying dictionary. Notice the usage of the dictionary `get()` method here to make these uncertain (data may not always exist!) lookups reliable.

### Step 8

The intended and operational states are compared, and based on the result, the interface name is added to the appropriate list.

```py
            # Compare operational to intended
            if oper_state != interface["state"]:
                fail_list.append(interface["name"])
            else:
                pass_list.append(interface["name"])
```

### Step 9

Finally, the function returns a dictionary containing the two pass and fail lists for easy lookup in the Ansible playbook or Jinja templates.

```py
        return {"pass": pass_list, "fail": fail_list}
```


## Task 2 - Using the Filter in an Ansible Playbook

You will write an Ansible playbook that compares static intent (stored in the playbook) to actual operational data from NXOS devices in the lab pod.

### Step 1

In the `/home/ntc/labs/lab04` folder, create the `inventory` file and add the following lines to it.

```
[nxos]
nxos-spine1
nxos-spine2

[nxos:vars]
ansible_user=ntc
ansible_password=ntc123
ansible_connection=network_cli
ansible_network_os=nxos
```

### Step 2

In the `/home/ntc/labs/lab04` folder, create the `pb_verify.yml` file and add the following lines to it.

```
---

- name: NXOS INTERFACES STATE VERIFICATION
  hosts: nxos
  gather_facts: false

  vars:
    interface_intent:
      - name: Ethernet1/1
        state: up
      - name: Ethernet1/2
        state: up
      - name: Ethernet1/10
        state: up
      - name: Ethernet1/11
        state: down

  tasks:
    - name: GET INTERFACE STATE FROM SWITCH
      nxos_command:
        commands: show int brief | json
      register: show_int_brief

    - name: COMPARE INTENT TO OPERATIONAL STATE
      set_fact:
        interface_pass_fail: "{{ show_int_brief.stdout.0 | verify_intended_state(interface_intent) }}"

    - name: SHOW COMPARISON RESULTS
      debug:
        var: interface_pass_fail
```

First, the playbook connects to the NXOS device and retrieves the output of the `show int brief | json` command. Then, it provides the data structure together with the `interface_intent` to the `verify_intended_state` filter to do its comparison. Finally, it displays the pass/fail dictionary returned by the filter.


### Step 3

Run the `pb_verify.yml` playbook and observe the results.

```
ntc@ntc-training:lab04$ ansible-playbook -i inventory pb_verify.yml

PLAY [NXOS INTERFACES STATE VERIFICATION] ************************************************************************

TASK [GET INTERFACE STATE FROM SWITCH] ***************************************************************************
ok: [nxos-spine2]
ok: [nxos-spine1]

TASK [COMPARE INTENT TO OPERATIONAL STATE] ***********************************************************************
ok: [nxos-spine1]
ok: [nxos-spine2]

TASK [SHOW COMPARISON RESULTS] ***********************************************************************************
ok: [nxos-spine1] => {
    "interface_pass_fail": {
        "fail": [
            "Ethernet1/10"
        ],
        "pass": [
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/11"
        ]
    }
}
ok: [nxos-spine2] => {
    "interface_pass_fail": {
        "fail": [
            "Ethernet1/10"
        ],
        "pass": [
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/11"
        ]
    }
}

PLAY RECAP *******************************************************************************************************
nxos-spine1                : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
nxos-spine2                : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

> Note: If you wish to view data in flight, feel free to increase Ansible's verbosity by adding one or more `-v` to the command line.

### Step 4

This information can be used in a report or, as exemplified here, in an in-playbook assertion. Add the following task at the end of the `pb_verify.yml` playbook.

```yaml
    - name: ASSERT THAT NO INTERFACES HAVE FAILED THE CHECKS
      assert:
        that:
          - interface_pass_fail.fail | length == 0
```

### Step 5

Run the playbook again.

```
ntc@ntc-training:lab04$ ansible-playbook -i inventory pb_verify.yml

PLAY [NXOS INTERFACES STATE VERIFICATION] ************************************************************************

TASK [GET INTERFACE STATE FROM SWITCH] ***************************************************************************
ok: [nxos-spine2]
ok: [nxos-spine1]

TASK [COMPARE INTENT TO OPERATIONAL STATE] ***********************************************************************
ok: [nxos-spine1]
ok: [nxos-spine2]

TASK [SHOW COMPARISON RESULTS] ***********************************************************************************
ok: [nxos-spine2] => {
    "interface_pass_fail": {
        "fail": [
            "Ethernet1/10"
        ],
        "pass": [
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/11"
        ]
    }
}
ok: [nxos-spine1] => {
    "interface_pass_fail": {
        "fail": [
            "Ethernet1/10"
        ],
        "pass": [
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/11"
        ]
    }
}

TASK [ASSERT THAT NO INTERFACES HAVE FAILED THE CHECKS] **********************************************************
fatal: [nxos-spine2]: FAILED! => {
    "assertion": "interface_pass_fail.fail | length == 0",
    "changed": false,
    "evaluated_to": false,
    "msg": "Assertion failed"
}
fatal: [nxos-spine1]: FAILED! => {
    "assertion": "interface_pass_fail.fail | length == 0",
    "changed": false,
    "evaluated_to": false,
    "msg": "Assertion failed"
}

PLAY RECAP *******************************************************************************************************
nxos-spine1                : ok=3    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
nxos-spine2                : ok=3    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

### Step 6

Feel free to play around with the data and change both the `interface_intent` dictionary and the configuration on the actual devices themselves!
