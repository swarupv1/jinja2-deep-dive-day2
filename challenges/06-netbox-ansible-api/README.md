# Challenge - Using NetBox data from Ansible

The goal of this exercise is to start interacting with the NetBox API from Ansible and make use of the dynamic inventory plugin.

## Exercise Overview

### Prerequisites

You will need to have Ansible installed and read-only access to a Netbox instance.

### Tasks

Submitting your solution for this challenge is optional - feel free to ask for help via email or at the open office hours if you get stuck! If do you send your files, make sure you remove any sensitive data like credentials/tokens!

#### Task 1

Write an Ansible Playbook that queries the NetBox API for IPAM data as follows:

- Query the NetBox API for all RIRs. If you don't have multiple RIRs, query for all Aggregates instead.
- Print the total number of RIRs/Aggregates returned by the API.
- Print a comma separated list of the RIR names from the API results.

**DO NOT** hardcode the API token inside of the playbook - you should only provide it at execution time to `ansible-playbook`.

> Hint: You do not need an inventory for this playbook as it can (and SHOULD) be run only once on localhost!

#### Task 2

Use the Ansible NetBox inventory plugin to build a dynamic inventory as per the following:

- Instruct the plugin to group devices based on their `site` and `manufacturer`.
- You should also use a `query_filter` to limit the amount of devices returned (especially if they are too many) by filtering devices matching only a specific field, such as `tenant` or `tag` or `rack-id`.
- Using the `compose` function, add the `id` field (the unique numeric identifier from the NetBox API) to the inventory device facts.

> Hint: Use the `ansible-inventory --graph -i netbox_inventory.yml` command to quickly view the structure of the dynamic inventory.
> Use the `ansible-inventory -v --list -i netbox_inventory.yml` command to view the inventory structure and additional metadata pulled from NetBox.

#### Task 3

Write an Ansible Playbook that uses the inventory built in `Task 2` to query NetBox for additional device metadata via the NetBox REST API.

**DO NOT** hardcode the API token inside of the playbook - you should only provide it at execution time to `ansible-playbook`.

The playbook should perform the following tasks:

- Print, for each device, its `id`, `manufacturer`, `platform` and `device_type` (this information should already be provided by the inventory plugin).
- Query the NetBox API for the full device data based on its `id`. Use the `uri` module.
- Print the device's `serial number` and/or `asset tag`.


### Useful links

- [NetBox Inventory Plugin](https://docs.ansible.com/ansible/latest/plugins/inventory/netbox.html)
- [NetBox Documentation](https://netbox.readthedocs.io/en/stable/)
- NetBox Live API Reference - `https://<YOUR_NETBOX_URL>/api/docs/`

### Reference Enablement Material

- NetBox & Source of Truth
- Introduction to REST APIs
- Network Programming and Automation Course
- Using Ansible Jinja Filters Challenge

> Note: Recordings of the relevant sessions can be found online at: https://training.networktocode.com/ 
