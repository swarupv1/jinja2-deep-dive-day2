# Lab 04 - Jinja template rendering with Python

Goals of this lab:

- Practice using the `jinja2` package for rendering template.
- Practice using the `FileSystemLoader` mode of loading templates.
- Learn how to use the `Environment` object.
- Practice customizing the `Environment` object to change the rendering behavior.

## Task 01

### Step 1

Copy the below Python code into the file called `j2_string_template.py` in `python` directory.

```python
from jinja2 import Template

data = {
    "name": "waw-rtr-core-01",
    "location": "Warsaw",
}

template = "Device {{ name }} is located in {{ location }}."

j2_template = Template(template)

print(j2_template.render(data))
```

### Step 2

Run the program using the below command:

```python j2_string_template.py```

### Step 3

This is the simplest example of a Python program rendering template with Jinja.

Read through the code and see if you can follow the logic. Then you can read the short walk-through below.

#### Code Walk-through

You created a new `Template` object using the template stored in the string.

You then passed the dictionary with variables to the `render()` method of the `Template` object.

Notice that we did not define a Jinja Environment. When using the `Template` object directly, a shared `Environment` object is created for us by Jinja in the background.

This way of rendering templates is great for quick testing but does not allow us to customize our environment.

## Task 02

### Step 1

Change into the `python` directory and create two new directories:

```
mkdir my_vars
mkdir my_templates
```

### Step 2

Copy the data and template from Lab 01, tasks 1 and 2.

Your directories should look like so:

```
tree my_vars/
my_vars/
├── lab01-task1.yml
└── lab01-task2.yml

tree my_templates/
my_templates/
├── lab01-task1.j2
└── lab01-task2.j2
```

### Step 3

Copy the below Python code into the file called `j2_file_loader.py` in `python` directory.

```python
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml

TEMPLATES_DIR = "./my_templates"
VARS_DIR = Path("./my_vars")


def main():
    vars_file = "lab01-task1.yml"
    template_name = "lab01-task1.j2"

    with Path(VARS_DIR / vars_file).open(mode="r", encoding="utf8") as file_in:
        template_data = yaml.safe_load(file_in)

    j2_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    j2_template = j2_env.get_template(template_name)
    rendered_template = j2_template.render(template_data)

    print(rendered_template)


if __name__ == "__main__":
    main()
```

## Step 4

Run the program using the below command:

```python j2_file_loader.py```

You should see the output of the template `lab01-task1.j2` rendered with variables from `lab01-task1.yml`.

# Step 5

Change the below lines:

```python
    vars_file = "lab01-task1.yml"
    template_name = "lab01-task1.j2"
```

To:

```python
    vars_file = "lab01-task2.yml"
    template_name = "lab01-task2.j2"
```

# Step 6

Run the program using the below command:

```python j2_file_loader.py```

You should see the output of the template `lab02-task1.j2` rendered with variables from `lab02-task1.yml`.

# Step 7

This program uses Jinja `Environment` and `FileSystemLoader` objects to load templates stored in files in the specified location.

You get more flexibility when choosing this approach. File names can be decided dynamically at the runtime, and Jinja Environment can now be customized as needed.

Read through the code and see if you can follow the logic. Then you can read the short walk-through below.

#### Code Walk-through

You created a new `Environment` and specified template loader as `FileSystemLoader`. `FileSystemLoader` takes a path to the directory on the disk as an argument.

Once `Environment` object is created you use `get_template(<template_file>)` method to retrieve template stored in the `<template_file>` name. This method will return `Template` object.

With template retrieved, you pass a dictionary with variables to the `render()` method of the `Template` object.

## Task 03

### Step 1

Open source code of the `j2_file_loader.py` program, which you created in the previous task.

### Step 2

Create data file `lab04-task3.yml` in `./my_vars`. Copy the below content into it:

```yaml
---
server_name: machineLearning-cluster01-ch

algo: neural_network
```

Create template file `lab04-task3.j2` in `./my_templates`. Copy the below content into it:

```
Machine Learning cluster: {{ server_name }}
Selected algorithm: {{ algo }}
Processing power: {{ cluster_mflops }}
```

### Step 3

Change the values of `vars_file` and `template_name` to match the below ones:

```python
    vars_file = "lab04-task3.yml"
    template_name = "lab04-task3.j2"
```

### Step 4

Run the program using the below command:

```python j2_file_loader.py```

You should see the output of the rendered template.

Notice that the line with `Processing power` has no value even though you placed a variable substitution statement in the template.

This is the default behavior of the Jinja rendering engine. Undefined variables don't generate errors, you simply get empty space in the final output.

### Step 5

Go back to the source code of the program and import class `StrictUndefined` from `jinja2` package.

See the final `jinja2` imports below for reference:

```python
from jinja2 import Environment, FileSystemLoader, StrictUndefined
```

Add `undefined=StrictUndefined` argument when instantiating `Environment` object.

Your line where the `Environment` is created should look like so:

```python
    j2_env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR), undefined=StrictUndefined
    )
```

### Step 6

Run the program using the below command:

```python j2_file_loader.py```

### Step 7

Your program should fail with the `jinja2.exceptions.UndefinedError` error.

Using `StrictUndefined` in your Jinja Environment means the template will error out when encountering an undefined variable instead of silently ignoring the error.

## Task 04

### Step 1 

Open source code of the `j2_file_loader.py` program which you worked with in the previous tasks.

### Step 2

Copy files `vars/lab04-task4.yml` and `templates/lab04-task4.j2` to `my_vars` and `my_templates` directories.

### Step 3

Change the values of `vars_file` and `template_name` to match the below ones:

```python
    vars_file = "lab04-task4.yml"
    template_name = "lab04-task4.j2"
```

### Step 4

Run the program using the below command:

```python j2_file_loader.py```

### Step 5

Observe resulting whitespace rendering.

### Step 6

Go back to the source code of the program and add `trim_blocks=True` argument when instantiating `Environment` object.

Your line where the `Environment` is created should look like so:

```python
    j2_env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        undefined=StrictUndefined,
        trim_blocks=True
    )
```

### Step 7

Run the program again using the below command:

```python j2_file_loader.py```

### Step 8

Observe resulting whitespace rendering.

`trim_blocks=True` told Jinja engine to automatically remove new lines placed after block statements.

### Step 9

Go back to the source code of the program. Add `lstrip_blocks=True` argument when instantiating the `Environment` object.

Your line where the `Environment` is created should look like so:

```python
    j2_env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        undefined=StrictUndefined,
        lstrip_blocks=True,
        trim_blocks=True
    )
```

### Step 10

Run the program again using the below command:

```python j2_file_loader.py```

### Step 11

Observe resulting whitespace rendering.

`lstrip_blocks=True` told Jinja engine to automatically remove spaces and tabs preceding the block statements.