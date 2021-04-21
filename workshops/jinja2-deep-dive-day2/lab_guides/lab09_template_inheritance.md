# Lab 09 - Template inheritance

## Task 01

> Resources for this task:
>  - [Jinja2 template inheritance](https://jinja2docs.readthedocs.io/en/stable/templates.html#template-inheritance)

### Step 1

Create directories named `base`, `router--edge` and `router--edge--inet` inside of the `ansible/templates` directory.

```
cd ansible/templates
mkdir base
mkdir router--edge
mkdir router--edge--inet
```

### Step 2

Create a template named `bgp.j2` inside of `base` directory. Copy the below contents into it.

```
ip bgp-community new-format
{% block community_lists %}
ip community-list standard LEVEL3_HIGH_PRIORITY permit 65001:120
{% endblock %}

route-map RM_EDGE_OUT permit 100
 match ip address prefix-list PL_EDGE_OUT
{% block rm_edge_out %}
{% endblock %}
route-map RM_EDGE_OUT deny 9999

ip prefix-list PL_RFC1918 seq 10 permit 10.0.0.0/8
ip prefix-list PL_RFC1918 seq 20 permit 172.16.0.0/12
ip prefix-list PL_RFC1918 seq 30 permit 192.168.0.0/16
{% block prefix_lists %}
{% endblock %}
```

### Step 3

Create a template named `bgp.j2` inside of `router--edge` directory. Copy the below contents into it.

```
{% block prefix_lists %}
ip prefix-list PL_EDGE_OUT seq 10 permit 10.50.0.0/24
ip prefix-list PL_EDGE_OUT seq 20 permit 10.60.0.0/24
{% endblock %}
```

### Step 4

Create a template named `bgp.j2` inside of `router--edge--init` directory. Copy the below contents into it.

```
{% block community_lists %}
{{ super () }}
ip community-list standard NTT_LOW_PRIORITY permit 65005:75
{% endblock %}

{% block rm_edge_out %}
route-map RM_EDGE_OUT permit 200
 match ip address prefix-list PL_INET_OUT
{% endblock %}

{% block prefix_lists %}
ip prefix-list PL_INET_OUT seq 10 permit 192.168.254.0/24
{{ super () }}
{% endblock %}
```

### Step 5

Templates named `bgp.j2` inside of `router--edge` and `router--edge--inet` should rely on the `base/bgp.j2` template. They won't work as they are right now.

Add Jinja2 expression at the top of the `bgp.j2` templates in `router--edge` and `router--edge--inet` that will extend the base `bgp.j2` template.

### Step 6

An Ansible playbook was created for you to test these templates.

Navigate to the `ansible` directory and execute the command below:

```
ansible-playbook pb_inheritance.yml
```

If your additions were correct, a file named `router--edge_bgp.cfg` will be generated in the `output` directory.

### Step 7

Modify `pb_inheritance.yml` playbook and update the variable `device_role` to `router--edge--inet`.

```
  vars:
    device_role: "router--edge--inet"
```

Execute the command below:

```
ansible-playbook pb_inheritance.yml
```

A file named `router--edge--inet_bgp.cfg` will be generated in the `output` directory.

You should review both of the generated files as well as all of the templates.

Try to follow the logic involved in inheritance and see how block override is being used.

<details>
  <summary>Reveal Answer</summary>

You should use `{% extends 'parent_template_path' }` expression in unfinished `bgp.j2` templates. This will cause child templates to inherit template elements from the parent template.

```
{% extends 'base/route_map.j2' %}
```

You can now refer to the named blocks from the parent template and override them with content specific to the role using the child template.

E.g.
```
{% block prefix_lists %}
ip prefix-list PL_INET_OUT seq 10 permit 192.168.254.0/24
{% endblock %}
```

If you want to keep the block content from the parent template, you should use the `{{ super() }}` statement.

E.g.
{% block community_lists %}
{{ super() }}
ip community-list standard NTT_LOW_PRIORITY permit 65005:75
{% endblock %}
```

</details>