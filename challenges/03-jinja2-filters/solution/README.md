# Challenge Exercise Solution Guide

## Using Ansible Jinja Filters on Network Device Data

In this challenge you have to use various Jinja2 filters (some are only available via Ansible's modifications, like ipaddr!) to query, format, filter, and present data from a network device.

You get started by loading the JSON output of a ​`show interfaces` command on an NX-OS switch. This output is provided as a file named ​`show_int_nxos.json` which should be placed next to the exercise
playbook named ​`pb_filters_challenge.yml​`.

## Solution Walkthrough

### Task 1

#### Step 1

Here you are using the filter `length` which returns the number of items in a sequence. Since the actual list of interfaces is nested two levels down inside the data structure, you have to extract the list by walking through the keys `TABLE_interface.ROW_interface`.

```yaml
    - name: T1S1 - GET THE NUMBER OF INTERFACES
      debug:
        msg: "The switch has a total of {{ show_int.TABLE_interface.ROW_interface | length }} interfaces."
```

#### Step 2

To avoid repeating the two keys over and over again and keep lines shorter, you create a new variable (or fact) that contains only the list of interfaces.

```yaml
    - name: T1S2 - EXTRACT THE INTERFACE LIST
      set_fact:
        intf_list: "{{ show_int.TABLE_interface.ROW_interface }}"
```

#### Step 3

Each interface is defined in a fairly large dictionary containing a lot of operational data. The only field you need is `interface` which represents the name. Use the `map` filter to only retrieve the values of that specific key for all the elements of the `intf_list` list. The map filter returns a generator object so you need to convert it to a list so it prints to the terminal.

```yaml
    - name: T1S3 - LIST ALL INTERFACE NAMES
      debug:
        msg: "List of interface names: {{ intf_list | map(attribute='interface') | list }}"
```

#### Step 4

Instead of printing a Python data structure (a list), use the `join(', ')` filter to join together the elements from the list of interface names with commas.

```yaml
    - name: T1S4 - PRINT INTERFACE NAMES AS CSV
      debug:
        msg: "Comma-separated interface names: {{ intf_list | map(attribute='interface') | list | join(', ') }}"
```

#### Step 5

The MAC addresses are held in a different attribute and, since the result is a list of strings, you can apply the `upper` filter to the whole list in one go. Not all filters can work on both a single value and a list!

```yaml
    - name: T1S5 - LIST ALL INTERFACE MAC ADDRESSES AS UPPERCASE
      debug:
        msg: "All MAC addresses: {{ intf_list | map(attribute='eth_hw_addr') | list | upper }}"
```

#### Step 6

The `hwaddr` filter only works with a single value, so it needs some help. `map` can also apply one filter to a list of values, making it possible to convert the previous list of MACs to a different notation.

```yaml
    - name: T1S6 - CONVERT MAC ADDRESSES TO LINUX FORMAT
      debug:
        msg: "All MAC addresses: {{ intf_list | map(attribute='eth_hw_addr') | map('hwaddr', 'linux') | list }} "
```

### Task 2

#### Step 1

Here all you need to do is extract two pieces of information from the first interface, `mgmt0`.

```yaml
    - name: T2S1 - EXTRACT THE MGMT0 IP PREFIX
      set_fact:
        mgmt0_prefix: "{{ intf_list.0.eth_ip_addr }}/{{ intf_list.0.eth_ip_mask }}"
```

#### Step 2

Now you apply various parameters of the `ipaddr` filter as per the documentation.

```yaml
    - name: T2S2 - PRINT THE USABLE IP RANGE FOR THE MGMT0 PREFIX
      debug:
        msg: "Usable IP range: {{ mgmt0_prefix | ipaddr('range_usable') }}"
```

#### Step 3

```yaml
    - name: T2S3 - PRINT THE BROADCAST ADDRESS FOR THE MGMT0 PREFIX
      debug:
        msg: "Broadcast address: {{ mgmt0_prefix | ipaddr('broadcast') }}"
```

#### Step 4

```yaml
    - name: T2S4 - PRINT THE 555TH USABLE ADDRESS FOR THE MGMT0 SUBNET
      debug:
        msg: "The 555th IP in the subnet: {{ mgmt0_prefix | ipaddr('555') }}"
```

### Task 3

#### Step 1

The `selectattr` filter can use a number of operators to apply tests to the data it is parsing. In the documentation they are called [tests](https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-builtin-tests).

Here, you need to check if the `admin_state` is `up` for a given interface, then count how many there are in the resulting list.

```yaml
    - name: T3S1 - COUNT THE INTERFACES IN ADMIN UP STATE
      debug:
        msg: "Number of interfaces in Admin/UP state: {{ intf_list | selectattr('admin_state','eq', 'up') | list | length }}"
```

#### Step 2

The `selectattr` filter does not reduce individual data like `map`, so you still have all of your interface parameters, including the names. Take this expression step by step and see what it returns.

```yaml
    - name: T3S2 - PRINT A CSV LIST OF THE INTERFACE NAMES IN ADMIN UP STATE
      debug:
        msg: "Interfaces in Admin/UP state: {{ intf_list | selectattr('admin_state','eq', 'up') | map(attribute='interface') | list | join(', ') }}"
```

#### Step 3

This task should now be easy to solve - it's just a matter of adding a second `selectattr` condition, chained to the first, creating the equivalent of an `and` operator.

In pseudo code, it would look like: `if admin_state == 'up' and state == 'up'`.

```yaml
    - name: T3S3 - PRINT A CSV LIST OF ALL INTERFACE NAMES IN UP/UP STATE
      debug:
        msg: "Interfaces in Admin/UP Operational/UP state: {{ intf_list | selectattr('admin_state','eq', 'up') | selectattr('state','eq', 'up') | map(attribute='interface') | list | join(', ') }}"
```

