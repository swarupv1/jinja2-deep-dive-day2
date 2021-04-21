# Lab 07 - Jinja Macros

Goals of this lab:

- Practice using include statement.
- Practice using import statement.

## Task 01

> Resources for this task:
>  - [Jinja2 macros](https://jinja2docs.readthedocs.io/en/stable/templates.html#macros)

### Step 1

You will be working with variables defined in the `python/vars/lab07-task1.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create a template named `lab07-task1.j2` in `python/templates` dir.

Your template should use data from the `lab07-task1.yml` file to generate output matching the one below.

**Output to match**
```
interface Ethernet10
  description Unused port, dedicated to data devices
interface Ethernet11
  description Unused port, dedicated to data devices
interface Ethernet12
  description Unused port, dedicated to voice devices
interface Ethernet24
  description Unused port, dedicated to wap devices
```

In your template, you should create a macro named `default_interface_desc` which takes one argument.

Use the `default_interface_desc` macro to generate interface descriptions.

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab07-task1.j2 -d lab07-task1.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should define macro using `{% macro macro_name(arg_name) %}` syntax.

Your macro should take the role of the interface as an argument and return the interface description.

You then use macro inside `for` loop to generate description for each of the interface. Use syntax `default_interface_desc(<intf_role>)` to execute defined macro.

```
{% macro default_interface_desc(intf_role) %}
Unused port, dedicated to {{ intf_role }} devices
{%- endmacro %}
{% for intf in interfaces %}
interface {{ intf['name'] }}
 description {{ default_interface_desc(intf['role']) }}
{% endfor %}
```

</details>


## Task 02

> Resources for this task:
>  - [Jinja2 macros](https://jinja2docs.readthedocs.io/en/stable/templates.html#macros)

### Step 1

You will be working with variables defined in the `ansible/vars/lab07-task2.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create a template named `lab07-task2.j2` in `ansible/templates` dir.

Your template should use data from the `lab07-task2.yml` file to generate output matching the one below.

**Output to match**
```
ip access-list standard local-interfaces
 permit 10.20.0.240 0.0.0.7
 permit 10.15.62.128 0.0.0.127
 permit 10.39.0.0 0.0.0.255
 permit 10.51.2.0 0.0.1.255
 permit 172.21.0.0 0.0.255.255
```

You're building a standard ACL and want to include all of the networks defined on your IP interfaces.

You need to write a macro named `ip_w_wildcard` which takes one argument.

Your macro should take IP address with prefix length and return network address in the 
`{network} {wildcard}` format. E.g.

For the below input:

`172.16.0.1/24`

The macro should generate the below output:

`172.16.0.0 0.0.0.255`

### Step 3

Change into `ansible` directory.

Run the below command to test your template.

```
ansible-playbook pb_lab07_task2.yml
```

The output of the rendering will be saved in the `output/lab07-task2.txt` file.

<details>
  <summary>Reveal Answer</summary>

You should define macro using `{% macro ip_w_wildcard(arg_name) %}` syntax.

Your macro should take IP address in the `{ip}/{pfx length}` format and return IP network in the `{network} {wildcard}` format.

To achieve that, you should use Ansible `ipaddr` filter. To get network part use `ipaddr('network')` and to get wildcard part use `ipaddr('hostmask')`

You should use the `map` filter to get IP addresses only from the list of interface objects. Then you should loop over the IPs and apply the `ip_w_wildcard` macro to each of the IPs.

```
{% macro ip_w_wildcard(ip_network) %}
{{ ip_network | ipaddr('network') }} {{ ip_network | ipaddr('hostmask')}}
{%- endmacro -%}

ip access-list standard {{ in_std_acl_name }}
{% for ip_address in interfaces | map(attribute='ipv4_address') %}
 permit {{ ip_w_wildcard(ip_address) }}
{% endfor %}
```
</details>
