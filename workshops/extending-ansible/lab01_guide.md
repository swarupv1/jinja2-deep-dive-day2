# Extending Ansible - Lab 01

In this lab exercise, you will create a custom Jinja2 filter for Ansible that expands short interface names - for example `gig` expands to `GigabitEthernet` and `tu` expands to `Tunnel`.  This helps users still use shorthand interface names while expanding the name often required for managing configuration in an idempotent fashion using Ansible. 

## Task 1 - Expanding an Abbreviated Interface Name

To start with, you will create a new filter that expands a single name (i.e. a string) based on a set of predefined mappings.

### Step 1

In your terminal on the lab workstation, change into the `/home/ntc/labs/lab01` folder, creating it if it doesn't exist.

```
ntc@ntc-training:~$ mkdir -p /home/ntc/labs/lab01
ntc@ntc-training:~$ cd /home/ntc/labs/lab01
ntc@ntc-training:lab01$
```

### Step 2

Create a folder named `filter_plugins` and in it a file called `expand_interface_name.py`.

```
ntc@ntc-training:lab01$ mkdir filter_plugins
ntc@ntc-training:lab01$ touch filter_plugins/expand_interface_name.py
ntc@ntc-training:lab01$ tree
.
└── filter_plugins
    └── expand_interface_name.py

1 directory, 1 file
```


> Note: The folder `filter_plugins` is automatically searched for plugins if it is relative to where your playbooks are stored. The path for plugins can also be defined in your `ansible.cfg` file.

### Step 3

Edit the `expand_interface_name.py` file and add the following code to it.

```py
class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "expand_interface_name": FilterModule.expand_interface_name,
        }

    @staticmethod
    def expand_interface_name(interface_name):
        """Expands abbreviated interface names."""
        return "NOT YET IMPLEMENTED"
```

First, you're defining the class `FilterModule` which is required by Ansible - this is where it looks for the custom filters to load. Then, the function `filters` creates a mapping between the filter name `expand_interface_name` (as it will appear in Ansible playbooks or Jinja templates) and the actual function that contains the code, in this instance `FilterModule.expand_interface_name`.

> Note: this is the scaffolding required for the filters you define in this specific file. It doesn't do anything useful yet.

### Step 4

Define the following global variable containing a mapping of two leading characters to the full interface name. Add this at the beginning of your script, right before the `class FilterModule` definition.

```py
INTERFACE_MAPPING = {
    "as": "Async",
    "br": "Bridge",
    "di": "Dialer",
    "et": "Ethernet",
    "fa": "FastEthernet",
    "fo": "FortyGigabitEthernet",
    "gi": "GigabitEthernet",
    "lo": "Loopback",
    "mg": "Mgmt",
    "po": "Port-Channel",
    "se": "Serial",
    "te": "TenGigabitEthernet",
    "tu": "Tunnel",
    "vl": "Vlan",
    "vx": "Vxlan",
}
```

> Note: using a dictionary allows you to easily extract the long name based on the key (leading two characters) in one operation.

### Step 5

Replace the `return` statement in the `expand_interface_name` function so it looks as follows:

```py
    @staticmethod
    def expand_interface_name(interface_name):
        """Expands abbreviated interface names."""
        return INTERFACE_MAPPING.get(
            interface_name.strip().lower()[0:2], interface_name
        )
```

The reference mapping is keyed on the leading two letters, so that's what you're extracting here with `interface_name.strip().lower()[0:2]`, also taking care to remove any whitespace and lowercase the input string.

Since the `INTERFACE_MAPPING` dictionary is by no means all-encompassing, usage of the `get` method ensures that if there is no matching key, a default of the original `interface_name` will be returned unchanged.

### Step 6

Checkpoint! 

The full `expand_interface_name.py` file should look like this:

```py
INTERFACE_MAPPING = {
    "as": "Async",
    "br": "Bridge",
    "di": "Dialer",
    "et": "Ethernet",
    "fa": "FastEthernet",
    "fo": "FortyGigabitEthernet",
    "gi": "GigabitEthernet",
    "lo": "Loopback",
    "mg": "Mgmt",
    "po": "Port-Channel",
    "se": "Serial",
    "te": "TenGigabitEthernet",
    "tu": "Tunnel",
    "vl": "Vlan",
    "vx": "Vxlan",
}


class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "expand_interface_name": FilterModule.expand_interface_name,
        }

    @staticmethod
    def expand_interface_name(interface_name):
        """Expands abbreviated interface names."""
        return INTERFACE_MAPPING.get(
            interface_name.strip().lower()[0:2], interface_name
        )

```

### Step 7

This is a Python script, so you may first test it directly by starting an interactive interpreter. Do that now and play around with the `expand_interface_name` function by throwing various values at it and checking what it returns.

Executing a script with the `-i` flag executes the script and then takes you into the interpreter.

```
ntc@ntc-training:lab01$ python3 -i filter_plugins/expand_interface_name.py
>>> FilterModule.expand_interface_name("vl")
'Vlan'
>>> FilterModule.expand_interface_name("vlan")
'Vlan'
>>> FilterModule.expand_interface_name("TUN")
'Tunnel'
>>> FilterModule.expand_interface_name("tenGig")
'TenGigabitEthernet'
>>> # "vi" is not mapped to anything
>>> FilterModule.expand_interface_name("virtual")
'virtual'
```

### Step 8

In the `/home/ntc/labs/lab01` folder, create a playbook called `pb_filters.yml`.  This will be used to test the filter from within an Ansible playbook.

```yaml
---

- name: TEST INTERFACE EXPANSION FILTER
  hosts: localhost
  gather_facts: false
  tasks:
    - debug:
        msg: "{{ 'gi' | expand_interface_name }}"

    - debug:
        msg: "{{ 'loop' | expand_interface_name }}"

    - debug:
        msg: "{{ 'TUN' | expand_interface_name }}"

    - debug:
        msg: "{{ 'po100' | expand_interface_name }}"

    - debug:
        msg: "{{ 'virt' | expand_interface_name }}"
```

> Reminder: Ansible will automatically load filters from the `filter_plugins` folder if it finds it relative to the playbook.

### Step 9

Run the Ansible playbook - note you do not need any inventory since you're just using `localhost` which is implicitly defined.

```
ntc@ntc-training:lab01$ ansible-playbook pb_filters.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [TEST INTERFACE EXPANSION FILTER] ***************************************************************************************************

TASK [debug] ***************************************************************************************************
ok: [localhost] => {
    "msg": "GigabitEthernet"
}

TASK [debug] ***************************************************************************************************
ok: [localhost] => {
    "msg": "Loopback"
}

TASK [debug] ***************************************************************************************************
ok: [localhost] => {
    "msg": "Tunnel"
}

TASK [debug] ***************************************************************************************************
ok: [localhost] => {
    "msg": "Port-Channel"
}

TASK [debug] ***************************************************************************************************
ok: [localhost] => {
    "msg": "virt"
}

PLAY RECAP ***************************************************************************************************
localhost                  : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Task 2 - Expanding a List of Names

What if you had a list of interface names to expand instead of a single one? It's a lot easier (and faster!) to loop in Python than in Ansible, so let's extend the filter to accept a list as well and add some type validation.

### Step 1

In the same `expand_interface_name.py` file, define a new function called `expand_interface_names` - take note of the subtle difference (plural "names"). Normally, you would remove the old function (or extend it in place), but for the purposes of this lab we will leave them be side by side.

This function should be placed inside of the same `class FilterModule` block.

```py
    @staticmethod
    def expand_interface_names(interface_names):
        """Expands abbreviated interface names."""
        if isinstance(interface_names, str):
            # Same as previously, it's just one interface name
            return INTERFACE_MAPPING.get(
                interface_names.strip().lower()[0:2], interface_names
            )
```

First, check the type of the provided `interface_names` parameter. If it is a string, then provide the same functionality as in the original filter. In this case it's a nice touch that provides backwards compatibility.

### Step 2

Add another check and the code to deal with the case when a list is passed to the function.

```py
    @staticmethod
    def expand_interface_names(interface_names):
        """Expands abbreviated interface names."""
        if isinstance(interface_names, str):
            # Same as previously, it's just one interface name
            return INTERFACE_MAPPING.get(
                interface_names.strip().lower()[0:2], interface_names
            )
        elif isinstance(interface_names, list):
            expanded_names = []
            for name in interface_names:
                long_name = INTERFACE_MAPPING.get(name.strip().lower()[0:2], name)
                expanded_names.append(long_name)
            return expanded_names
```

If a list is passed, then you need to perform the same `INTERFACE_MAPPING` lookup operation for each of its components and return a list back with the expanded values.

### Step 3

This steps adds error handling using class objects that Ansible provides to provide more graceful failing and helpful messages to the users when an error occurs.

At the top of the script, add the following import statement:

```py
from ansible import errors
```

### Step 4

If the function receives a parameter that is not a `string` or a `list`, then it will raise an error (in this case an exception specific to Ansible) with a custom message. Modify the `expand_interface_names` function as shown below.

```py
    @staticmethod
    def expand_interface_names(interface_names):
        """Expands abbreviated interface names."""
        if isinstance(interface_names, str):
            # Same as previously, it's just one interface name
            return INTERFACE_MAPPING.get(
                interface_names.strip().lower()[0:2], interface_names
            )
        elif isinstance(interface_names, list):
            expanded_names = []
            for name in interface_names:
                long_name = INTERFACE_MAPPING.get(name.strip().lower()[0:2], name)
                expanded_names.append(long_name)
            return expanded_names
        else:
            raise errors.AnsibleFilterError(
                "expand_interface_names filter error: provide a string or a list of strings!"
            )
```

### Step 5

Finally, register the new function as a filter so Ansible can find it. Add a new entry in the `def filters()` function of the `FilterModule` class.

```py
    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "expand_interface_name": FilterModule.expand_interface_name,
            "expand_interface_names": FilterModule.expand_interface_names,
        }
```

> Note: If you try to use it before this step, Ansible will give you an error like the following.

```
fatal: [localhost]: FAILED! => {"msg": "template error while templating string: no filter named 'expand_interface_names'. String: {{ 'gi' | expand_interface_names }}"}
```

### Step 6

Checkpoint!

The full `expand_interface_name.py` file should now look like this:

```py
from ansible import errors

INTERFACE_MAPPING = {
    "as": "Async",
    "br": "Bridge",
    "di": "Dialer",
    "et": "Ethernet",
    "fa": "FastEthernet",
    "fo": "FortyGigabitEthernet",
    "gi": "GigabitEthernet",
    "lo": "Loopback",
    "mg": "Mgmt",
    "po": "Port-Channel",
    "se": "Serial",
    "te": "TenGigabitEthernet",
    "tu": "Tunnel",
    "vl": "Vlan",
    "vx": "Vxlan",
}


class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "expand_interface_name": FilterModule.expand_interface_name,
            "expand_interface_names": FilterModule.expand_interface_names,
        }

    @staticmethod
    def expand_interface_name(interface_name):
        """Expands abbreviated interface names."""
        return INTERFACE_MAPPING.get(
            interface_name.strip().lower()[0:2], interface_name
        )

    @staticmethod
    def expand_interface_names(interface_names):
        """Expands abbreviated interface names."""
        if isinstance(interface_names, str):
            # Same as previously, it's just one interface name
            return INTERFACE_MAPPING.get(
                interface_names.strip().lower()[0:2], interface_names
            )
        elif isinstance(interface_names, list):
            expanded_names = []
            for name in interface_names:
                long_name = INTERFACE_MAPPING.get(name.strip().lower()[0:2], name)
                expanded_names.append(long_name)
            return expanded_names
        else:
            raise errors.AnsibleFilterError(
                "expand_interface_names filter error: provide a string or a list of strings!"
            )
```


### Step 7

In the `pb_filters.yml` playbook, create a new play to test this filter. First, check that for single strings, its behavior is unchanged. Then, pass lists of names and finally an invalid value to test all code paths.

```yaml
- name: TEST MULTIPLE INTERFACE EXPANSION FILTER
  hosts: localhost
  gather_facts: false
  tasks:
    - debug:
        msg: "{{ 'gi' | expand_interface_names }}"

    - debug:
        msg: "{{ ['gig', 'port', 'mg' ] | expand_interface_names }}"

    - debug:
        msg: "{{ ['loop', 'virt', 'PRI0' ] | expand_interface_names }}"

    - debug:
        msg: "{{ 100 | expand_interface_names }}"
```

### Step 8

Run the Ansible playbook. The last task will intentionally fail, the playbook is passing a number to the filter to check that the error message is sent accordingly.

```
ntc@ntc-training:lab01$ ansible-playbook pb_filters.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not
match 'all'

PLAY [TEST INTERFACE EXPANSION FILTER] ***************************************************************************

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": "GigabitEthernet"
}

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": "Loopback"
}

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": "Tunnel"
}

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": "Port-Channel"
}

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": "virt"
}

PLAY [TEST MULTIPLE INTERFACE EXPANSION FILTER] ******************************************************************

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": "GigabitEthernet"
}

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": [
        "GigabitEthernet",
        "Port-Channel",
        "Mgmt"
    ]
}

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": [
        "Loopback",
        "virt",
        "PRI0"
    ]
}

TASK [debug] *****************************************************************************************************
fatal: [localhost]: FAILED! => {"msg": "expand_interface_names filter error: provide a string or a list of strings!"}

PLAY RECAP *******************************************************************************************************
localhost                  : ok=8    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```


## Task 3 - Homework Challenge (Optional)

Try to do this task in your own time after the workshop and test it with as many possible combinations as you can!

You may have noticed that if you provide a string with a number in it (e.g. "gi100") then it is lost after expansion (e.g. "GigabitEthernet" is the result).

Improve the filter to preserve any interface numbering during this process. 

**Hint**: you should find a way to split the name (likely letters and symbols) from the numbering part (digits and symbols like - or /) before expanding only the first part.
