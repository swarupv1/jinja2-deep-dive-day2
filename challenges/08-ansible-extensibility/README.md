# Challenge - Extending Ansible Custom Filters and Modules

The goal of this exercise is to improve the custom filters and modules developed during the [Extending Ansible Workshop](../../workshops/extending-ansible/).

## Exercise Overview

### Prerequisites

For the filters tasks 1 and 2, you only need Ansible locally on your machine.

For the module task 3, you will also need access to a CSR1000v or any other IOS-XE device with the RESTCONF API enabled. The CSR1000v is a virtual machine that can be downloaded from Cisco and is also available as an image in public cloud (e.g. AWS).

If you have not attended the [Extending Ansible Workshop](../../workshops/extending-ansible/) it is highly recommended you first watch the recording and go through the labs each task refers to!

### Tasks

#### Task 1

In [Extending Ansible Workshop - Lab 01](../../workshops/extending-ansible/lab01_guide.md) you wrote a filter that expanded interface names from the first two letter abbreviations to a canonical full name (e.g. "gi" -> "GigabitEthernet")

You may have noticed that if you provided it a string with a number in it (e.g. "gi100"), then it is lost after expansion (e.g. "GigabitEthernet" is the result).

Improve the filter code to preserve any interface numbering during this process. Split the interface type (letters only) from the optional numbering that might follow it (digits, symbols) and preserve the latter in the end result.

For example: "po100" -> "Port-Channel100" and "gi0/0/1" -> "GigabitEthernet0/0/0"

> Hint: Use the code and the playbook from the workshop as a starting point, you can find them in the repository next to the lab guide.

#### Task 2

In [Extending Ansible Workshop - Lab 02](../../workshops/extending-ansible/lab02_guide.md) you wrote a filter that expanded numerical ranges into a list of items.

For example, `GigabitEthernet1/[1:5]` expands into:

```json
[
    "GigabitEthernet1/1",
    "GigabitEthernet1/2",
    "GigabitEthernet1/3",
    "GigabitEthernet1/4",
    "GigabitEthernet1/5"
]
```

This filter only accepts the range spec to be placed at the end of the string: `Eth[1:5]` is valid, but `Eth[1:5]/0` is not.

Modify the filter code so that it also works for cases like `Eth[1:5]/0` or `192.168.[1:100].0/24`. You will need to change the filter's regex to accept a third optional group of characters after the range spec and, if present, preserve this in the resulting output.

Feel free to build the new regex online on sites such as [regex101](https://regex101.com/) and test it as shown in the workshop lab (Task 1/Step 4), with the help of the interactive python interpreter.

> Hint: Use the code and the playbook from the workshop as a starting point, you can find them in the repository next to the lab guide.

#### Task 3

In [Extending Ansible Workshop - Lab 06](../../workshops/extending-ansible/lab06_guide.md) you wrote a custom module that changed (patched) the description of a VRF via the IOS-XE RESTCONF API.

Extend the module code to also perform the following tasks:

1. Make the module idempotent.
    + It should always check if the intended configuration matches the device configuration (hint: send a GET request and compare the attributes).
    + If the VRF is not created, it should fail gracefully, since the PATCH request cannot create the VRF resource, only modify an existing one.
    + If actual configuration changes not are necessary, it should report `ok` (i.e. changed=False) and not send a PATCH request.
2. Enable `check mode` (i.e. dry-run) support in the module.
    + If the `check mode` flag is present, it should only report whether changes would be made, without performing them. This goes hand in hand with the idempotency code.

> Hint: Use the code and the playbook from the workshop as a starting point, you can find them in the repository next to the lab guide.

### Useful links

- [Ansible Documentation](https://docs.ansible.com)
- [Regex101](https://regex101.com/)

### Reference Enablement Material

- Extending Ansible Workshop
- Introduction to REST APIs
- Network Programming and Automation Course

> Note: Recordings of the relevant sessions can be found online at: https://training.networktocode.com/
