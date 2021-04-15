# Lab 02 - Jinja loops, conditionals and tests

Goals of this lab:

- Practice use of tests.
- Use loops to iterate over lists and dictionaries.
- Practice use of loop variables.
- Write templates combining loops, conditionals, and tests.
## Task 01

### Step 1

You will be working with variables defined in the `python/vars/lab02-task1.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create a template named `lab02-task1.j2` in `python/templates` dir.

In your template, write tests checking if variables in `lab02-task1.j2` are of a specific type.

Your output should match the below one:
```
Is dc_name a string?
- Yes

Is number_of_devices an integer?
- Yes

Is dc_temp a float?
- No

Is vrfs a dictionary?
- Yes

```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab02-task1.j2 -d lab02-task1.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use built-in tests with `{% if %}` conditionals.

```
Is dc_name a string?
{% if dc_name is string %}
- Yes
{% else %}
- No
{% endif %}

Is number_of_devices an integer?
{% if number_of_devices is integer %}
- Yes
{% else %}
- No
{% endif %}

Is dc_temp a float?
{% if dc_temp is float %}
- Yes
{% else %}
- No
{% endif %}

Is vrfs a dictionary?
{% if vrfs is mapping %}
- Yes
{% else %}
- No
{% endif %}
```

</details>

## Task 02

### Step 1

You will be working with variables defined in the `python/vars/lab02-task2.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

A template, `python/templates/lab02-task2.j2` has been created for you. This template is used to render the site contact number read from the `lab02-task2.yml`

Unfortunately, something strange happens during the rendering.

This is the output we get, which is different than the phone number recorded in the data file:

```
Site contact number: 15106296
```

Change either the template or the data, or both, so that the number is rendered correctly.
### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab02-task2.j2 -d lab02-task2.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

YAML tries to decide data types dynamically. Number starting with `0` consisting of digits `0-7` will be treated as octal.

You should place quotation marks around the number to explicitly make it a string.

```
---
site_contact: "071500370"
```

Optionally you can also add a conditional check to the template. This won't prevent the template from being rendered but you can easily search files for lines containing `!ERROR!` string.

{% if site_contact is string %}
Site contact number: {{ site_contact }}
{% else %}
Site contact number: !ERROR!: 'site_contact' MUST be string.
{% endif %}

</details>

## Task 03

### Step 1

You will be working with variables defined in the `python/vars/lab02-task3.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create template named `lab02-task3.j2` in `python/templates` dir.

Your template should generate interface configuration using the data in `lab02-task3.yml`.

Output from your template should match the below text:

```
interface Loopback0
 description Control Plane traffic
 ip address 10.255.255.34/32
!
interface Management1
 description Management interface
 ip address 10.10.0.5/24
!
interface Ethernet1
 description Span port - SPAN1
 ip address 
!
interface Ethernet2
 description PortChannel50 - port 1
 ip address 
!
interface Ethernet51
 description leaf01-eth51
 ip address 10.50.0.0/31
!
interface Ethernet52
 description leaf02-eth51
 ip address 10.50.0.2/31
!
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab02-task3.j2 -d lab02-task3.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use `{% for %}` loop iterating over the dictionary item.

Then you should access the keys of the dictionary inside of the loop.

```
{% for intf_name, intf_data in interfaces.items() %}
interface {{ intf_name }}
 description {{ intf_data['description'] }}
 ip address {{ intf_data['ipv4_address'] }}
!
{% endfor %}
```

</details>

## Task 04

### Step 1

You will be working with variables defined in the `python/vars/lab02-task4.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

A template named `lab02-task4.j2` in `python/templates` dir was created for you.

This template is not working correctly at the moment. See below the template and output it generates.

**Template**
```
{% for line in secure_acl['lines'] %}
ip access-list standard {{ secure_acl['name'] }}
 10 permit {{ line['network'] }} {{ line['mask'] }}
! Total ACL lines: {{ secure_acl['lines'] | length }}
{% endfor %}
```

**Output**
```
ip access-list standard SECURE_ACCESS_IN
 10 permit 10.0.0.0 0.0.0.255
! Total ACL lines: 3
ip access-list standard SECURE_ACCESS_IN
 10 permit 10.0.1.0 0.0.0.255
! Total ACL lines: 3
ip access-list standard SECURE_ACCESS_IN
 10 permit 10.0.2.0 0.0.0.255
! Total ACL lines: 3
```

The access list definition repeats 3 times, the sequence numbers are not correct, and the summary line is repeated 3 times.

You need to fix this template so that the output is a valid configuration. See below output for comparison.

**Desired output**
```
ip access-list standard SECURE_ACCESS_IN
 10 permit 10.0.0.0 0.0.0.255
 20 permit 10.0.1.0 0.0.0.255
 30 permit 10.0.2.0 0.0.0.255
! Total ACL lines: 3
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab02-task4.j2 -d lab02-task4.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use loop index variables `first` and `last` to conditionally display lines on the first and last iteration of the loop only.

Use the `index` loop variable to compute ACL sequence numbers.

```
{% for line in secure_acl['lines'] %}
{%  if loop.first %}
ip access-list standard {{ secure_acl['name'] }}
{%  endif %}
 {{ loop.index * 10 }} permit {{ line['network'] }} {{ line['mask'] }}
{%  if loop.last %}
! Total ACL lines: {{ secure_acl['lines'] | length }}
{%  endif %}
{% endfor %}
```

</details>

## Task 05 (Optional)

This task combines the use of different Jinja features and it might take a bit longer to complete.


### Step 1

You will be working with variables defined in the `python/vars/lab02-task5.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create template named `lab02-task5.j2` in `python/templates` dir.

Your template should generate interface configuration using the data in `lab02-task5.yml`.

Output from your template should match the below text:

```
Device: sw-dist-waw-01
Layer3 switch?: No
Name with stack pos.: sw-dist-waw-01-1
OS > 4.19: No
SD WAN site?: No
----------
Device: sw-dist-waw-01
Layer3 switch?: No
Name with stack pos.: sw-dist-waw-01-2
OS > 4.19: No
SD WAN site?: No
----------
Device: sw-dist-par-01
Layer3 switch?: Yes
OS > 4.19: Yes
SD WAN site?: Yes
----------
Device: rtr-core-ty-01
Layer3 switch?: No
OS > 4.19: Yes
SD WAN site?: Yes
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab02-task5.j2 -d lab02-task5.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use `{% for %}` loop to iterate over the list of devices.

Use containment `in` operator and logical operators where appropriate.

Pay attention to the placement of `{% if %}` blocks.

```
{% for device in devices %}
Device: {{ device['name'] }}
Layer3 switch?: {% if device['device_type'] == "switch" and device['layer'] == "layer3" %}Yes{% else %}No{% endif %}

{%  if device['stack_pos'] is defined %}
Name with stack pos.: {{ device['name'] ~ '-' ~ device['stack_pos'] }}
{%  endif %}
OS > 4.19: {% if device['os_ver'] > 4.19 %}Yes{% else %}No{% endif %}

SD WAN site?: {% if device['site'] in sdwan_sites %}Yes{% else %}No{% endif %}

{%  if not loop.last %}
----------
{%  endif %}
{% endfor %}
```

</details>