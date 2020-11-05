# Extending Ansible - Lab 03

In this lab exercise, you will create a custom filter for Ansible that uses a third party Python library called `prettytable` to display tabular data as pure text.  This type of filter will save countless hours when using Jinja templates to generate text-based reports.

## Task 1 - Building the Filter Code

To start with, you will create a new filter generates a text-based table using the `prettytable` library.

### Step 1

In your terminal on the lab workstation, change into the `/home/ntc/labs/lab03` folder, creating it if it doesn't exist.

```
ntc@ntc-training:~$ mkdir -p /home/ntc/labs/lab03
ntc@ntc-training:~$ cd /home/ntc/labs/lab03
ntc@ntc-training:lab03$
```

### Step 2

Create a folder named `filter_plugins` and in it a file called `build_table.py`.
```
ntc@ntc-training:lab03$ mkdir filter_plugins
ntc@ntc-training:lab03$ touch filter_plugins/build_table.py
ntc@ntc-training:lab03$ tree
.
└── filter_plugins
    └── build_table.py

1 directory, 1 file
```

### Step 3

Edit the `build_table.py` file and paste in the following content. This is the full script so take a bit of time to read through the code.

```py
from prettytable import PrettyTable


class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "build_table": FilterModule.build_table,
        }

    @staticmethod
    def build_table(table_data):
        """Builds a text table from list data."""
        table = PrettyTable()
        # Set the table column headers
        table.field_names = table_data.get("headers")

        # Add in row data one by one
        for row in table_data.get("rows"):
            table.add_row(row)

        # Return the pure text representation of the table
        return table.get_string()
```

The `PrettyTable` class is fairly straightforward to work with, the code uses the following functionality (for more examples check out its [repository](https://github.com/jazzband/prettytable)):

- `table.field_names` this property sets the table column headers and is a list of strings
- `table.add_row()` this method allows you to add a row into the table as a list of values
- `table.get_string()` this method returns a text representation of the table for printing

### Step 4

In the terminal, ensure that the `prettytable` Python package is installed.

```
ntc@ntc-training:lab03$ pip3 install prettytable --user
Collecting prettytable
  Downloading https://files.pythonhosted.org/packages/39/da/8336296a830caa495a25304e12ffb32a8c3a9d2d08ba995f066fe16152e1/prettytable-1.0.1-py2.py3-none-any.whl
Requirement already satisfied: setuptools in /usr/local/lib/python3.6/site-packages (from prettytable) (41.0.1)
Collecting wcwidth (from prettytable)
  Downloading https://files.pythonhosted.org/packages/59/7c/e39aca596badaf1b78e8f547c807b04dae603a433d3e7a7e04d67f2ef3e5/wcwidth-0.2.5-py2.py3-none-any.whl
Installing collected packages: wcwidth, prettytable
Successfully installed prettytable-1.0.1 wcwidth-0.2.5
```

### Step 5

Start a Python interpreter and test your filter code.

```
ntc@ntc-training:lab03$ python3 -i filter_plugins/build_table.py
>>> table_data = {}
>>> table_data["headers"] = ['NAME','DATE CREATED', 'STATUS', 'ID', 'IP ADDRESS']
>>> table_data["rows"] = []
>>> table_data["rows"].append(['IOSXE', 'today', 'up', '098435', '10.10.10.1'])
>>> table_data["rows"].append(['NXOS', 'today', 'down', '098435', '10.10.10.2'])
>>> table_data["rows"].append(['JUNIPER', 'today', 'down', '098078', '10.10.10.3'])
>>>
>>> print(FilterModule.build_table(table_data))
+---------+--------------+--------+--------+------------+
|   NAME  | DATE CREATED | STATUS |   ID   | IP ADDRESS |
+---------+--------------+--------+--------+------------+
|  IOSXE  |    today     |   up   | 098435 | 10.10.10.1 |
|   NXOS  |    today     |  down  | 098435 | 10.10.10.2 |
| JUNIPER |    today     |  down  | 098078 | 10.10.10.3 |
+---------+--------------+--------+--------+------------+
```

## Task 2 - Using the Filter in an Ansible Playbook

Write an Ansible Playbook that uses the `build_table` filter to save a text table representation to a file.

### Step 1

In the `/home/ntc/labs/lab03` folder, create the `pb_build_table.yml` file and add the following lines to it.

```yaml
---

- name: BUILD TEXT TABLE
  hosts: localhost
  gather_facts: false

  vars:
    table_data:
      headers: ['NAME','DATE CREATED', 'STATUS', 'ID', 'IP ADDRESS']
      rows:
        - ['IOSXE', 'today', 'up', '098435', '10.10.10.1']
        - ['NXOS', 'today', 'down', '098435', '10.10.10.2']
        - ['JUNIPER', 'today', 'down', '098078', '10.10.10.3']
```

In this case, you are defining the input structured data as play vars inline - but in practice, you might get this data from other modules, CSV files, output from API calls etc.

### Step 2

Finalize the `pb_build_table.yml` playbook by adding the tasks shown below (final file included for reference):

```yaml
---

- name: BUILD TEXT TABLE
  hosts: localhost
  gather_facts: false

  vars:
    table_data:
      headers: ['NAME','DATE CREATED', 'STATUS', 'ID', 'IP ADDRESS']
      rows:
        - ['IOSXE', 'today', 'up', '098435', '10.10.10.1']
        - ['NXOS', 'today', 'down', '098435', '10.10.10.2']
        - ['JUNIPER', 'today', 'down', '098078', '10.10.10.3']

  tasks:
    # This is the Python dictionary parsed from the playbook YAML vars
    - name: DISPLAY STRUCTURED INPUT DATA
      debug:
        var: table_data

    # This is the text table with whitespace and newlines
    - name: DISPLAY TEXT OUTPUT DATA
      debug:
        var: table_data | build_table

    # Save to a file the formatted text table
    - name: SAVE TABLE REPRESENTATION TO FILE
      copy:
        content: "{{ table_data | build_table }}"
        dest: table.txt
```

### Step 3

Run the Ansible playbook and inspect the output.

```
ntc@ntc-training:lab03$ ansible-playbook pb_build_table.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not
match 'all'

PLAY [BUILD TEXT TABLE] ******************************************************************************************

TASK [DISPLAY STRUCTURED INPUT DATA] *****************************************************************************
ok: [localhost] => {
    "table_data": {
        "headers": [
            "NAME",
            "DATE CREATED",
            "STATUS",
            "ID",
            "IP ADDRESS"
        ],
        "rows": [
            [
                "IOSXE",
                "today",
                "up",
                "098435",
                "10.10.10.1"
            ],
            [
                "NXOS",
                "today",
                "down",
                "098435",
                "10.10.10.2"
            ],
            [
                "JUNIPER",
                "today",
                "down",
                "098078",
                "10.10.10.3"
            ]
        ]
    }
}

TASK [DISPLAY TEXT OUTPUT DATA] **********************************************************************************
ok: [localhost] => {
    "table_data | build_table": "+---------+--------------+--------+--------+------------+\n|   NAME  | DATE CREATED | STATUS |   ID   | IP ADDRESS |\n+---------+--------------+--------+--------+------------+\n|  IOSXE  |    today     |   up   | 098435 | 10.10.10.1 |\n|   NXOS  |    today     |  down  | 098435 | 10.10.10.2 |\n| JUNIPER |    today     |  down  | 098078 | 10.10.10.3 |\n+---------+--------------+--------+--------+------------+"
}

TASK [SAVE TABLE REPRESENTATION TO FILE] *************************************************************************
changed: [localhost]

PLAY RECAP *******************************************************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Step 4

Check the contents of the `table.txt` file.

```
ntc@ntc-training:lab03$ cat table.txt
+---------+--------------+--------+--------+------------+
|   NAME  | DATE CREATED | STATUS |   ID   | IP ADDRESS |
+---------+--------------+--------+--------+------------+
|  IOSXE  |    today     |   up   | 098435 | 10.10.10.1 |
|   NXOS  |    today     |  down  | 098435 | 10.10.10.2 |
| JUNIPER |    today     |  down  | 098078 | 10.10.10.3 |
+---------+--------------+--------+--------+------------+
```

### Step 5

Add some more row data and regenerate the table!

**Optional challenge**: 

Try to figure out how to save the output as HTML instead of pure text. Hint... check the PrettyTable documentation!
