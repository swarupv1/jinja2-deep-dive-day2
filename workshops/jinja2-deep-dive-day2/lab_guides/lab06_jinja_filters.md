# Lab 06 - Jinja Filters

Goals of this lab:

- Practice the use of Jinja filters.
- Practice filter chaining.
- Understand the result type of filters operating on collections.

## Task 01

> Resources for this task:
>  - [Jinja2 built-in filters](https://jinja2docs.readthedocs.io/en/stable/templates.html#list-of-builtin-filters)
> - [Jinja2 for loop](https://jinja2docs.readthedocs.io/en/stable/templates.html#for)

### Step 1

You will be working with variables defined in the `python/vars/lab06-task1.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create a template named `lab06-task1.j2` in `python/templates` dir.

Your template should use data from the `lab06-task1.yml` file to generate output matching the one below.

You should print only interface objects that are in the blocked state.

The final output should match the below text:

```
Interfaces in blocking state:
{'cost': '4', 'interface': 'Gi1/3', 'port_id': '5', 'port_priority': '128', 'role': 'Altn', 'status': 'BLK', 'type': 'Shr', 'vlan_id': '1'}
{'cost': '4', 'interface': 'Gi1/5', 'port_id': '5', 'port_priority': '128', 'role': 'Altn', 'status': 'BLK', 'type': 'Shr', 'vlan_id': '2'}
{'cost': '4', 'interface': 'Gi1/7', 'port_id': '5', 'port_priority': '128', 'role': 'Altn', 'status': 'BLK', 'type': 'Shr', 'vlan_id': '3'}
```

> HINT: You can use loop to print each of the objects.

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab06-task1.j2 -d lab06-task1.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use the `selectattr` filter with the `eq` test to select only objects whose `status` attribute is equal to `BLK`.

To display selected objects you can use the `for` loop.

```
Interfaces in blocking state:
{% for intf in show_spanning_tree | selectattr('status', 'eq', 'BLK') %}
{{ intf }}
{% endfor %}
```
</details>

### Step 4

Modify your template `lab06-task1.j2` to display a list of interface names only for interfaces that are in the blocking state.

**Output to match**
```
Interfaces in blocking state:
['Gi1/3', 'Gi1/5', 'Gi1/7']
```

### Step 5

Run the below command to test your template.

```
./j2_render.py -t lab06-task1.j2 -d lab06-task1.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You need to chain the `map` filter and specify `attribute='interface'` as an argument. This will give a collection of interface names only.

Filters that give back collection return generator object. You need to convert the result to a list with the `list` filter before the final result can be displayed.

```
Interfaces in blocking state:
{{ show_spanning_tree| selectattr('status', 'eq', 'BLK') | map(attribute='interface') | list }}
```

</details>

### Step 6

Modify your template `lab06-task1.j2` to make the output more human-friendly. List interface names on one line, separated by comma and space.

**output to match**
```
Interfaces in blocking state:
Gi1/3, Gi1/5, Gi1/7
```

### Step 7

Run the below command to test your template.

```
./j2_render.py -t lab06-task1.j2 -d lab06-task1.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use the `join` filter to generate a string resulting from concatenating collection items with the string `, ` as a separator.

You don't have to use the `list` filter here; the `join` filter works with generators as well as with lists.

```
Interfaces in blocking state:
{{ show_spanning_tree | selectattr('status', 'eq', 'BLK') | map(attribute='interface') | join(', ') }}
```

</details>

## Task 02

> Resources for this task:
>  - [Jinja2 built-in filters](https://jinja2docs.readthedocs.io/en/stable/templates.html#list-of-builtin-filters)
> - [Jinja2 for loop](https://jinja2docs.readthedocs.io/en/stable/templates.html#for)

### Step 1

You will be working with variables defined in the `python/vars/lab06-task2.yml` file.

Open this file now and familiarize yourself with the data.

### Step 2

Create a template named `lab06-task2.j2` in `python/templates` dir.

Your template should use data from the `lab06-task2.yml` file to generate report matching the one below.

**Output to match**
```
Server type: app
Servers: [{'name': 'appFend04s', 'type': 'app', 'location': 'Seattle'}, {'name': 'appFend03s', 'type': 'app', 'location': 'Seattle'}]
Server type: db
Servers: [{'name': 'dbAnalytics02s', 'type': 'db', 'location': 'Seattle'}, {'name': 'dbAnalytics01f', 'type': 'db', 'location': 'San Francisco'}, {'name': 'dbAnalytics01s', 'type': 'db', 'location': 'Seattle'}]
Server type: ml
Servers: [{'name': 'mlNeural01s', 'type': 'ml', 'location': 'Seattle'}, {'name': 'mlNeural03s', 'type': 'ml', 'location': 'Seattle'}, {'name': 'mlNeural02s', 'type': 'ml', 'location': 'Seattle'}, {'name': 'mlNeural01p', 'type': 'ml', 'location': 'Portland'}, {'name': 'mlNeural01f', 'type': 'ml', 'location': 'San Francisco'}]
Server type: redis
Servers: [{'name': 'redisCache03p', 'type': 'redis', 'location': 'Portland'}, {'name': 'redisCache01s', 'type': 'redis', 'location': 'Seattle'}, {'name': 'redisCache02f', 'type': 'redis', 'location': 'San Francisco'}]
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab06-task2.j2 -d lab06-task2.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use the `groupby` filter with the `attribute='type'` argument to create groups of servers for each of the server types.

You should use the `for group, group_members` loop to iterate over the sequence generated by the `groupby` filter.

```
{% for server_type, servers in servers | groupby(attribute='type') %}
Server type: {{ server_type }}
Servers: {{ servers }}
{% endfor %}
```
</details>

### Step 4

Modify your template `lab06-task2.j2` to batch servers in units of 2 and display the names of the servers only.

**output to match**
```
Server type: app
['appFend04s', 'appFend03s']
Server type: db
['dbAnalytics02s', 'dbAnalytics01f']
['dbAnalytics01s']
Server type: ml
['mlNeural01s', 'mlNeural03s']
['mlNeural02s', 'mlNeural01p']
['mlNeural01f']
Server type: redis
['redisCache03p', 'redisCache01s']
['redisCache02f']
```

### Step 5

Run the below command to test your template.

```
./j2_render.py -t lab06-task2.j2 -d lab06-task2.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

You should use the `map` filter with the `attribute='name'` argument to create a collection of server names only for each of the server groups.

You should then apply a `batch` filter to the result, with `2` as the argument, to create batches of server names, each with 2 items.

To display resulting batches you should use the `for` loop.

```
{% for server_type, servers in servers | groupby(attribute='type') %}
Server type: {{ server_type }}
{%  for server_batch in servers | map(attribute='name') | batch(2) %}
{{ server_batch }}
{%  endfor %}
{% endfor %}
```

</details>

### Step 6

Modify your template `lab06-task2.j2` to make the output more human-friendly.

- Add a number to each of the batches.
- Display server names in each batch separated by a comma and space.
- Server names in each batch should be displayed in alphabetical order.
- Add `---------------` divider separating server groups. - Divider needs to be centered in the field width of 40 characters.

**output to match**
```
Server type: app
Batch 1: appFend03s, appFend04s
            ---------------             
Server type: db
Batch 1: dbAnalytics01f, dbAnalytics02s
Batch 2: dbAnalytics01s
            ---------------             
Server type: ml
Batch 1: mlNeural01s, mlNeural03s
Batch 2: mlNeural01p, mlNeural02s
Batch 3: mlNeural01f
            ---------------             
Server type: redis
Batch 1: redisCache01s, redisCache03p
Batch 2: redisCache02f
            ---------------             
```

### Step 7

Run the below command to test your template.

```
./j2_render.py -t lab06-task2.j2 -d lab06-task2.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

Use the `loop.index` variable to number each batch.

You should apply the `sort` filter to servers in a batch to have them sorted in alphabetical order.

You should use the `join` filter with `, ` argument to concatenate server names in a batch.

To center `---------------` you should use `center` filter with `40` as an argument.

You should then apply the `batch` filter to the result, with `2` as the argument, to create batches of server names, each with 2 items.

To display resulting batches you should use the `for` loop.

```
{% for server_type, servers in servers | groupby(attribute='type') %}
Server type: {{ server_type }}
{%  for server_batch in servers | map(attribute='name') | batch(2) %}
Batch {{ loop.index }}: {{ server_batch | sort | join(', ') }}
{%  endfor %}
{{ '---------------' | center(40) }}
{% endfor %}
```

</details>

## Task 03

> Resources for this task:
>  - [Jinja2 built-in filters](https://jinja2docs.readthedocs.io/en/stable/templates.html#list-of-builtin-filters)
> - [Jinja2 for loop](https://jinja2docs.readthedocs.io/en/stable/templates.html#for)

### Step 1

You work with API that returned data structure saved in the `python/vars/lab06-task3.yml` file.

This data structure records the name of the prefix-list on some of the interfaces. If an interface has a prefix-list defined, it means the network configured on that interface needs to be added to the specified prefix list.

Open this file now and familiarize yourself with the data.

### Step 2

A starter template, `lab06-task3.j2`, was created for you in `python/templates` dir.

This template has some issues, and it currently generates the below output:

```
ip prefix-list PL_REDIST_OSPF seq 5 10.3.0.0/24
ip prefix-list PL_REDIST_BGP seq 5 10.6.7.0/24
ip prefix-list PL_REDIST_OSPF seq 5 10.23.1.0/24
ip prefix-list PL_REDIST_BGP seq 5 10.145.5.0/24
```

You need to fix this template. It should correctly generate prefix-lists as required with entry sequence numbers starting from 5.

**Output to match**
```
ip prefix-list PL_REDIST_BGP seq 5 10.6.7.0/24
ip prefix-list PL_REDIST_BGP seq 10 10.145.5.0/24
ip prefix-list PL_REDIST_OSPF seq 5 10.3.0.0/24
ip prefix-list PL_REDIST_OSPF seq 10 10.23.1.0/24
```

### Step 3

Run the below command to test your template.

```
./j2_render.py -t lab06-task3.j2 -d lab06-task3.yml -trim
```

<details>
  <summary>Reveal Answer</summary>

Prefix-lists defined in the interface objects can appear multiple times and they're not guaranteed to be ordered.

In cases like this, you should use the `groupby` filter to create groups of objects that have something in common. Here you should specify `attribute='prefix_list'` to create groups of objects with the same prefix-list.

To iterate over groups and members you should use the `for group, group_members` loop.

Next, each of the group members is a collection of interfaces but you want IP addresses only. You should use the `for` loop and `map` filter to get a sequence of `ip` values.

Finally, inside the inner loop, you should use the `loop.index` variable to generate correct sequence numbers.

```
{% for pl_name, pl_members in interfaces | groupby(attribute='prefix_list' ) %}
{%  for ip in pl_members | map(attribute='ip') %}
ip prefix-list {{ pl_name }} seq {{ 5 * loop.index }} {{ ip | ipaddr('network/prefix') }}
{%  endfor %}
{% endfor %}
```

</details>