# Lab 10 - Building lists and dictionaries in Ansible

## Task 01

> Resources for this task:
>  - [Ansible - Appending to lists and dictionaries](https://ttl255.com/ansible-appending-to-lists-and-dictionaries/)

### Step 1

An Ansible playbook named `pb_lab10_task1.yml` was created for you in the `ansible` directory.

Open this playbook now and have a look at the tasks.

### Step 2

The playbook contains variable definitions and some tasks. You need to modify Task 2.

Task 2 is missing variable definition. The other code in that task is correct. 

You need to add the missing variable definition. The end value held by the variable should be a list of server names containing strings 'DB' or 'WB'.

### Step 3

Once you finished modifying Task 2, run the playbook with the below command:

```
ansible-playbook pb_lab10_task1.yml
```

The output of debugging task, Task 3, should match the below one:

```
ok: [localhost] => {
    "msg": [
        "srvDB01t",
        "srvWEB03t",
        "srvDB01b",
        "srvDB03g"
    ]
}
```


<details>
  <summary>Reveal Answer</summary>

Ansible loop iterates over the server names and each item is accessible via a variable called `server_name`.

You should define a variable named `db_servers`. This variable will be assigned the value of append operation between itself and the current server name in the loop.

The server name is a string so it needs to be enclosed in square brackets `[]` to make a 1-element list. If you don't do it an error will be raised due to the incompatible types.

```
  - name: "TASK 2: ADD DB AND WEB SERVERS TO THE LIST"
    set_fact:
      db_servers: "{{ db_servers + [server_name] }}"
    loop: "{{ servers }}"
    loop_control:
      loop_var: server_name
    when: "{{ 'DB' in server_name or 'WEB' in server_name }}"
```

</details>

## Task 02

> Resources for this task:
>  - [Ansible - Appending to lists and dictionaries](https://ttl255.com/ansible-appending-to-lists-and-dictionaries/)
>  - [Ansible `combine` filter](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-hashes-dictionaries)

### Step 1

An Ansible playbook named `pb_lab10_task2.yml` was created for you in the `ansible` directory.

Open this playbook now and have a look at the tasks.

### Step 2

The playbook contains variable definitions and some tasks. You need to modify Task 2.

Task 2 is missing variable definition. The other code in that task is correct. 

You need to add the missing variable definition. The end value held by the variable should be dictionary mapping interface names to default access VLAN assignment. Use VID `10` as the default VLAN assignment.

### Step 3

Once you finished modifying Task 2, run the playbook with the below command:

```
ansible-playbook pb_lab10_task2.yml
```

Output of debugging task, Task 3, should match the below one:

```
ok: [localhost] => {
    "msg": {
        "Ethernet1": 10,
        "Ethernet2": 10,
        "Ethernet3": 10,
        "Ethernet4": 10,
        "Ethernet5": 10,
        "Ethernet6": 10,
        "Ethernet7": 10
    }
}
```


<details>
  <summary>Reveal Answer</summary>

Ansible loop iterates over the interface names and each item is accessible via a variable called `intf_name`.

You should define a variable named `interfaces_w_vlan`. This variable will be assigned value resulting from dictionary merge, using filter `combine`, operation. Values merged is the current value of `interfaces_w_vlan` and key-value pair mapping interface name to VID 10.

You essentially update the `interfaces_w_vlan` dictionary with one key-value pair at the time.

```
  - name: "TASK 2: BUILD DICT WITH INTERFACES AND DEFAULT VLAN ASSIGNMENTS"
    set_fact:
      interfaces_w_vlan: "{{ interfaces_w_vlan | combine({intf_name: 10}) }}"
    loop: "{{ interfaces }}"
    loop_control:
      loop_var: intf_name
```

</details>

## Task 03

> Resources for this task:
>  - [Ansible - Appending to lists and dictionaries](https://ttl255.com/ansible-appending-to-lists-and-dictionaries/)

### Step 1

An Ansible playbook named `pb_lab10_task3.yml` was created for you in the `ansible` directory.

Open this playbook now and have a look at the tasks.

### Step 2

The playbook contains variable definitions and some tasks. You need to modify Task 2.

Task 2 is missing variable definition, other code in that task is correct. 

You need to add the missing variable definition. The end value held by the variable should be a list of dictionaries. Each dictionary should contain two keys, `name` and `role`. Key `name` should contain the name of the switch. Key `role` should contain the value `access-switch` for all of the switches.

### Step 3

Once you finished modifying Task 2, run the playbook with the below command:

```
ansible-playbook pb_lab10_task3.yml
```

Output of debugging task, Task 3, should match the below one:

```
ok: [localhost] => {
    "msg": [
        {
            "name": "sw-access-par-01",
            "role": "access-switch"
        },
        {
            "name": "sw-access-waw-02",
            "role": "access-switch"
        },
        {
            "name": "sw-access-ldn-01",
            "role": "access-switch"
        },
        {
            "name": "sw-access-ny-03",
            "role": "access-switch"
        }
    ]
}
```

<details>
  <summary>Reveal Answer</summary>

Ansible loop iterates over the switch names and each item is accessible via a variable called `switch`.

You should define a variable named `switches_w_role`. This variable will be assigned the value of append operation between itself and a dictionary. This dictionary has two keys, `name` and `role`. Key `name` should have the current `switch` as its value. Key `role` has value `access-switch` for all of the switches.

Dictionary you define needs to be enclosed in square brackets `[]` to make a 1-element list. If you don't do it an error will be raised due to the incompatible types.

```
  - name: "TASK 2: BUILD LIST OF DICTS WITH DEVICES AND ROLE ASSIGNMENTS"
    set_fact:
      switches_w_role: "{{ switches_w_role + [{'name': switch, 'role': 'access-switch'}] }}"
    loop: "{{ switches }}"
    loop_control:
      loop_var: switch
```

</details>