# Extending Ansible - Lab 02

In this lab exercise, you will create a custom filter for Ansible that expands a range specifier to assist in quickly creating lists of things like interfaces and hostnames. 

For example, `Ethernet[10:20]` would expand into the following list:

```py
[
    "Ethernet10",
    "Ethernet11",
    "Ethernet12",
    "Ethernet13",
    "Ethernet14",
    "Ethernet15",
    "Ethernet16",
    "Ethernet17",
    "Ethernet18",
    "Ethernet19",
    "Ethernet20"
]
```

This comes in to be extremely helpful when managing large YAML files.  For example, think about managing 100s or 1000s of interfaces applying similar configurations to each.  This may look familar:

```yaml
Ethernet10:
  speed: 1000
  duplex: full
  access_vlan: 100
Ethernet11:
  speed: 1000
  duplex: full
  access_vlan: 100
Ethernet12:
  speed: 1000
  duplex: full
  access_vlan: 100
Ethernet13:
  speed: 1000
  duplex: full
  access_vlan: 100

```

You would then have a loop in a Jinja template to consume that data.  To simplify the YAML data in conjunction with using a filter in that template, you could represent that data as follows:

```yaml
Ethernet[10:13]:
  speed: 1000
  duplex: full
  access_vlan: 100
```


## Task 1 - Creating the Expand Range Filter

To start with, you will create a new filter that uses regular expressions to match a specific syntax and then generate the list.

### Step 1

In your terminal on the lab workstation, change into the `/home/ntc/labs/lab02` folder, creating it if it doesn't exist.

```
ntc@ntc-training:~$ mkdir -p /home/ntc/labs/lab02
ntc@ntc-training:~$ cd /home/ntc/labs/lab02
ntc@ntc-training:lab02$
```

### Step 2

Create a folder named `filter_plugins` and in it a file called `expand_range.py`.

```
ntc@ntc-training:lab02$ mkdir filter_plugins
ntc@ntc-training:lab02$ touch filter_plugins/expand_range.py
ntc@ntc-training:lab02$ tree
.
└── filter_plugins
    └── expand_range.py

1 directory, 1 file
```

### Step 3

In the `expand_range.py` file, add the following initial code. This is the filter scaffolding, creating the `FilterModule` class, the filter bindings, and the actual custom code inside of the `expand_range()` function.

For now the function does nothing but raise an error. The rest of the code will be added in the following steps.

```py
import re
from ansible import errors


class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "expand_range": FilterModule.expand_range,
        }

    @staticmethod
    def expand_range(text):
        """Expands a range specifier for interface to a list."""

        # No range provided or no match at all, so raise an error
        raise errors.AnsibleFilterError(
            f"expand_range filter error: No valid range found in '{text}'!"
        )
```

### Step 4

The first step is to build the regular expression (regex) that will match the desired range spec. To keep thing simple, the pattern should allow for any amount of text, followed by one single range at the end of the string.

For example, `Ethernet[1:5]` or `192.168.0.[100:110]` are both valid, but `Ethernet[1:5]/10` is not.

The regex to match is built as follows: `^(\S+)(\[\d+:\d+\])$` - first, match one or more non whitespace characters `(\S+)` as the first group, then match one instance of the range spec for the second group `(\[\d+:\d+\])`. This is made of `[`, followed by at least one digit, then a `:`, then at least one digit, and finally a `]`. The `^` and `$` tell the regex parser to find exactly this whole pattern from the beginning to the end.

Open a Python3 interpreter and test it!

```
ntc@ntc-training:lab02$ python3
Python 3.6.8 (default, Jun 11 2019, 01:16:11)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import re
>>> re.findall(r"^(\S+)(\[\d+:\d+\])$", "Ethernet[1:5]")
[('Ethernet', '[1:5]')]
>>> re.findall(r"^(\S+)(\[\d+:\d+\])$", "192.168.0.[100:110]")
[('192.168.0.', '[100:110]')]
>>> re.findall(r"^(\S+)(\[\d+:\d+\])$", "Ethernet[1:5]/10")
[]
>>> re.findall(r"^(\S+)(\[\d+:\d+\])$", "[1:5]")
[]
```

As you can see here, there is no match for patterns that are not allowed - the range spec MUST be at the end and there MUST be at least one leading character before the spec.

Feel free to experiment with more values to get a feel for how this works and pay special attention to the data structure returned by `re.findall`!

### Step 5

The regex from the previous step helpfully splits the input string into two parts: the fixed text and the range spec.

There's a bit more work to be done on the range spec before you can use it, as right now it is a string like `"[1:5]"`. To extract the numbers from it, you may use another regex or just string methods to remove the extra characters as seen below.

Experiment with the following commands in the Python interpreter!

```
>>> # First strip the [ and ] from the string.
>>> "[1:5]".strip("[]")
'1:5'

>>> # Then split based on the : character.
>>> "[1:5]".strip("[]").split(":")
['1', '5']

>>> # Assign the resulting strings to the start and stop variables
>>> start, stop ="[1:5]".strip("[]").split(":")
>>> start
'1'
>>> stop
'5'

>>> # Use the range() construct to obtain a list of values
>>> # Remember: start and stop are strings, so you need to convert them to numbers!
>>> list(range(int(start), int(stop) + 1))
[1, 2, 3, 4, 5]
```

### Step 6

Bring it all together in the `expand_range.py` script - the `expand_range()` function should look like the following:

```py
    @staticmethod
    def expand_range(text):
        """Expands a range specifier for interface to a list."""
        # Look for at least one non-whitespace character for the base
        # followed by a range spec: [x:y] where x and y are integers
        result = re.findall(r"^(\S+)(\[\d+:\d+\])$", text)

        # Check if we have a valid match
        # "Loopback100[1:3]" yields [('Loopback100', '[1:3]')]
        # but "Loopback100" yields []
        if result:
            # Process the range spec '[1:3]' into start and stop as strings
            start, stop = result[0][1].strip("[]").split(":")
            # Generate the expanded list by appending numbers to the
            # base string from the provided range
            base = result[0][0]
            expanded_list = []
            for i in range(int(start), int(stop) + 1):
                expanded_list.append(f"{base}{i}")

            return expanded_list

        # No range provided or no match at all, so raise an error
        raise errors.AnsibleFilterError(
            f"expand_range filter error: No valid range found in '{text}'!"
        )
```

Feel free to refer back to the previous testing you did in the Python interpreter to understand what's going on in there.

### Step 7

Start an interactive Python interpreter session with the `expand_range.py` script and test the new function. Play around with different values!

```
ntc@ntc-training:lab02$ python3 -i filter_plugins/expand_range.py
>>> FilterModule.expand_range("Loopback100[1:3]")
['Loopback1001', 'Loopback1002', 'Loopback1003']
>>>
>>>
>>> FilterModule.expand_range("Loopback100")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "filter_plugins/expand_range.py", line 39, in expand_range
    f"expand_range filter error: No valid range found in '{text}'!"
ansible.errors.AnsibleFilterError: expand_range filter error: No valid range found in 'Loopback100'!
```

> Note: As you can see, if no range is given or the range spec is not at the end, an `AnsibleFilterError` exception will be raised which helps Ansible show a meaningful error message when it executes playbooks.


## Task 2 - Using the Expand Range Filter in Ansible

It's time to use the filter in an Ansible playbook, leveraging it inside Jinja templates to quickly generate and apply configuration.

### Step 1

In the `/home/ntc/labs/lab02` folder, create the `pb_range.yml` file to actually test the filter from within an Ansible playbook.

```yaml
---

- name: USING THE EXPAND RANGE FILTER
  hosts: localhost
  gather_facts: false

  tasks:
    - debug:
        msg: "{{ 'GigabitEthernet1/[1:5]' | expand_range }}"

    - debug:
        msg: "{{ 'GigabitEthernet100' | expand_range }}"
```

### Step 2

Run the Ansible playbook. As you can see below, it works as expected, expanding the range spec if it finds one, or failing with an error message otherwise.

```
ntc@ntc-training:lab02$ ansible-playbook pb_range.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [USING THE EXPAND RANGE FILTER] *****************************************************************************

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": [
        "GigabitEthernet1/1",
        "GigabitEthernet1/2",
        "GigabitEthernet1/3",
        "GigabitEthernet1/4",
        "GigabitEthernet1/5"
    ]
}

TASK [debug] *****************************************************************************************************
fatal: [localhost]: FAILED! => {"msg": "expand_range filter error: No valid range found in 'GigabitEthernet100'!"}

PLAY RECAP *******************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

### Step 3

Create a folder named `templates` and in it a file called `range_shutdown.j2`.

```
ntc@ntc-training:lab02$ mkdir templates
ntc@ntc-training:lab02$ touch templates/range_shutdown.j2
ntc@ntc-training:lab02$ tree
.
├── filter_plugins
│   ├── __pycache__
│   │   └── expand_range.cpython-36.pyc
│   └── expand_range.py
├── pb_range.yml
└── templates
    └── range_shutdown.j2

3 directories, 4 files
```

### Step 4

Edit the `templates/range_shutdown.j2` file and add the following contents.

```
{% for name in interface_range | expand_range %}
interface {{ name }}
 shutdown
{% endfor %}
```

### Step 5

Edit a new file named `pb_range_template.yml` playbook and define a play that makes use of this Jinja template to generate a file.

```yaml
---

- name: USING FILTERS IN TEMPLATES
  hosts: localhost
  gather_facts: false

  vars:
    interface_range: GigabitEthernet[5:9]

  tasks:
    - debug:
        msg: "{{ interface_range | expand_range }}"

    - name: GENERATE CONFIG TO SHUTDOWN INTERFACES
      template:
        src: range_shutdown.j2
        dest: range_shutdown.cfg
```

> Note: This playbook simply generates config that shuts down interfaces, functionality that may already exist in certain CLIs. You may build any type of configuration here, from incrementing IPs, custom descriptions, or using more advanced range patterns that are not available on the CLI.

### Step 6

Run the `pb_range_template.yml` Ansible playbook. Verify the contents of the `range_shutdown.cfg` file.

```
ntc@ntc-training:lab02$ ansible-playbook pb_range_template.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [USING FILTERS IN TEMPLATES] ********************************************************************************

TASK [debug] *****************************************************************************************************
ok: [localhost] => {
    "msg": [
        "GigabitEthernet5",
        "GigabitEthernet6",
        "GigabitEthernet7",
        "GigabitEthernet8",
        "GigabitEthernet9"
    ]
}

TASK [GENERATE CONFIG TO SHUTDOWN INTERFACES] ********************************************************************
changed: [localhost]

PLAY RECAP *******************************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

ntc@ntc-training:lab02$ cat range_shutdown.cfg
interface GigabitEthernet5
 shutdown
interface GigabitEthernet6
 shutdown
interface GigabitEthernet7
 shutdown
interface GigabitEthernet8
 shutdown
interface GigabitEthernet9
 shutdown
```

### Step 7

In the `/home/ntc/labs/lab02` folder, create the `inventory` file and add the following lines to it.

```
[iosxe]
csr[1:3]

[iosxe:vars]
ansible_user=ntc
ansible_password=ntc123
ansible_connection=network_cli
ansible_network_os=ios
```

### Step 8

In the `pb_range_template.yml` file, update the `hosts: localhost` line to `hosts: csr3`.

### Step 9

Add a new task to the playbook to deploy the generated configurations:

```yaml
    - name: APPLY RANGE SHUTDOWN TO DEVICE DIRECTLY
      ios_config:
        src: range_shutdown.j2
```

The fully playbook should look like this:

```yaml
---

- name: USING FILTERS IN TEMPLATES
  hosts: csr3
  gather_facts: false

  vars:
    interface_range: GigabitEthernet[5:9]

  tasks:
    - debug:
        msg: "{{ interface_range | expand_range }}"

    - name: GENERATE CONFIG TO SHUTDOWN INTERFACES
      template:
        src: range_shutdown.j2
        dest: range_shutdown.cfg

    - name: APPLY RANGE SHUTDOWN TO DEVICE DIRECTLY
      ios_config:
        src: range_shutdown.j2
```


### Step 10

Run the `pb_range_template.yml` Ansible playbook. It should now connect to the `csr3` router and apply the templated config leveraging your custom range expansion filter!

```
ntc@ntc-training:lab02$ ansible-playbook -i inventory pb_range_template.yml

PLAY [USING FILTERS IN TEMPLATES] ********************************************************************************

TASK [debug] *****************************************************************************************************
ok: [csr3] => {
    "msg": [
        "GigabitEthernet5",
        "GigabitEthernet6",
        "GigabitEthernet7",
        "GigabitEthernet8",
        "GigabitEthernet9"
    ]
}

TASK [GENERATE CONFIG TO SHUTDOWN INTERFACES] ********************************************************************
changed: [csr3]

TASK [APPLY RANGE SHUTDOWN TO DEVICE DIRECTLY] *******************************************************************
changed: [csr3]

PLAY RECAP *******************************************************************************************************
csr3                       : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
