# Lab 01 - Jinja basics

Goals of this lab:

- Refresh use of Jinja variable substitution.
- Understand limitations of the '.' (dot) method of accessing attributes.
- Practice creating new variables.
- Practice applying math operator.
- Understand when to use `~` concatenation operator.

## Task 1

### Step 1

You will be working with variables defined in the `python/vars/lab01-task1.yml` file.

Open this file now and familiarize yourself with the data.
### Step 2

Create a template named `lab01-task1.j2` in `python/templates` dir.

Your template should use data from the `lab01-task1.yml` file to generate output matching the one below.

Don't use loops in your solution.

The final output should match the below text:
```
hostname lab-nxos

no ip domain lookup
ip domain name lab.local
ip name-server 8.8.8.8
ip name-server 8.8.4.4

ntp server 10.5.5.2 prefer
ntp server 10.7.5.2

snmp-server community snmpS3cr4t! RO
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab01-task1.j2 -d lab01-task1.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use variable substitution within `{{ }}` blocks.

You can use `.` or `[]` notation for accessing dictionary keys and list items. It is recommended to use the `[]` notation to make explicit difference between key names and variables.

For keys containing special characters, e.g. `-`, you need to use `[]` notation.


```
hostname {{ hostname }}

no ip domain lookup
ip domain name {{ dns['domain'] }}
ip name-server {{ dns['servers'][0] }}
ip name-server {{ dns['servers'][1] }}

ntp server {{ ntp_servers[0] }} prefer
ntp server {{ ntp_servers[1] }}

snmp-server community {{ snmp['community-string'] }} RO
```
</details>

## Task 2

### Step 1

You will be working with variables defined in the `python/vars/lab01-task2.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

You will now create a template named `lab01-task2.j2` in `python/templates` dir. This template will generate an inventory report for the lab devices.

Lab devices are installed in cabinets in groups of 4. First 4 devices will be installed in cab # 10, next 4 in cab # 11 and so on.

Each device is installed in racks starting from the bottom. Starting rack units are 6 units apart between devices. So 1st device in lab 1 will be installed at U height 8. 2nd device in lab 1 at U height 14, and so on.

The final hostname is built by appending the cabinet number and starting rack position to the device name.

Your template should use data from the `lab01-task2.yml` file to generate output matching the one below.

Final output to match:
```
Lab device onboarding report

Device hostname lab-cat9k1320
Cabinet number: 13
Racks units occupied: 20 - 23
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab01-task2.j2 -d lab01-task2.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

Use `{% set %}` statements to define new variables. This makes the rest of the template simpler.

Apply mathematical operators to compute lab numbers, U height, etc.

Use the `~` operator to concatenate a string with integers.

```
{% set unit_in_lab = lab_number % 4 %}
{% set cabinet = lab_cab_start + unit_in_lab %}
{% set rack_u_start = lab_rack_u_start + (6 * (unit_in_lab -1 )) %}
Lab device onboarding report

Device hostname {{ name ~ cabinet ~ rack_u_start }}
Cabinet number: {{ cabinet }}
Racks units occupied: {{ rack_u_start }} - {{ rack_u_start + rack_u_height - 1 }}
```

</details>

## Task 3

### Step 1

You will be working with variables defined in the `python/vars/lab01-task3.yml` file.

Open this file now and familiarize yourself with the data.

## Step 2

In this task, you are a writing template generating stub of the base config for network devices.

You will now create a template named `lab01-task3.j2` in `python/templates` that accomplishes this task. Your template will use data from the `lab01-task3.yml` file.

Some of the data structures are a bit tricky to work with so pay attention to the syntax.

The output of your template after rendering should match the below one:
```
hostname sw-dist-lon-01

no ip domain lookup
ip domain name jinja2.lab

snmp-server location London Telehouse East
snmp-server contact_info support@th-east.null

archive
 log config
  logging enable
  logging size 500
  notify syslog contenttype plaintext
  hidekeys

logging alarm informational
logging trap notifications
logging origin-id hostname
logging source-interface Loopback0
logging host 10.1.54.4
logging host 10.4.6.16
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab01-task3.j2 -d lab01-task3.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

Use variable substitution `{{ }}` syntax to access values of the variables.

Use `[]` notation for accessing keys containing special characters.

Define helper variable to make it easier to access nested data elements.

```
{% set device_region = sites[site]['region'] %}
hostname {{ hostname }}

no ip domain lookup
ip domain name {{ domain_name }}

snmp-server location {{ sites[site]['location-name'] }}
snmp-server contact_info support@th-east.null

archive
 log config
  logging enable
  logging size {{ logging_settings['archive_logging_size'] }}
  notify syslog contenttype plaintext
  hidekeys

logging alarm informational
logging trap notifications
logging origin-id hostname
logging source-interface {{ logging_settings['source_interface'] }}
logging host {{ regions[device_region]['logging_hosts'][0] }}
logging host {{ regions[device_region]['logging_hosts'][1] }}
```

</details>