# Extending Ansible - Lab 05

Ansible modules are the building blocks of Ansible playbooks. Modules are reusable, standalone scripts that Ansible runs on your behalf, either locally or remotely to interface with a local machine, an API, or a remote system to perform specific tasks. Ansible modules are used inside tasks within a playbook, and do all the automation work based on the purpose of the module.

Ansible already comes installed with a good number of modules to cover many of the automation tasks out there, but sometimes there are going to be certain tasks that some modules might not fully support.

This lab will show you how to build an Ansible module from scratch to abstract the ability to make an HTTP API call to `GET` device configuration from the IOS-XE RESTCONF API.

## Task 1 - Building the initial stages of an Ansible module

This task will show how to build a basic Python script that will be used as the initial module to test with an Ansible playbook. 

### Step 1

In the terminal of the workstation, change or create if not present to `/home/ntc/labs/lab05` folder. Use the `mkdir` command to create the `/home/ntc/labs/lab05` folders. 

```
ntc@ntc-training:~$ mkdir -p /home/ntc/labs/lab05
ntc@ntc-training:~$ cd /home/ntc/labs/lab05
ntc@ntc-training:lab05$
```

### Step 2

Create a folder named `modules` and an empty file called `iosxe_gather_configs.py`. Use the `mkdir` command to create the folder and the `touch` command to create the empty file. The `tree` command will display the folder structure.

```
ntc@ntc-training:lab05$ mkdir modules
ntc@ntc-training:lab05$ touch modules/iosxe_gather_configs.py
ntc@ntc-training:lab05$ tree
.
└── modules
    └── iosxe_gather_configs.py

1 directory, 1 file
```

### Step 3

Open up the `iosxe_gather_configs.py` script with an editor of choice. Inside the file add `#!/usr/bin/python3` on the first line and on the next line import the `AnsibleModule` class from the `ansible.module_utils.basic` library.

> Note: The `AnsibleModule` class is used to pass parameters in and out of the module. 

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
```

### Step 4

After importing the `AnsibleModule` class object build a `main()` function and create a variable called `module` to store the `AnsibleModule` object. Inside the `AnsibleModule` object pass in `argument_spec` as an argument with an empty dictionary for now. Later the `argument_spec` will be used to create the Ansible module parameters.

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def main():

    module = AnsibleModule(argument_spec={})
```

### Step 5

Create a variable called `response` with a value containing a dictionary of `{"host": "csr1"}`. For now the `response` value will be the output displayed when the Ansible playbook is executed. 

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def main():

    module = AnsibleModule(argument_spec={})

    response = {"host": "csr1"}
```

### Step 6

The `AnsibleModule` class will help handle incoming parameters and exiting the program using the `module.exit_json()` method at the end of the script. The `module.exit_json()` method will take in `msg=response` as an argument to display the output.

The `exit_json()` method is what is going to be returned from the module without error.

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def main():

    module = AnsibleModule(argument_spec={})

    response = {"host": "csr1"}

    module.exit_json(msg=response)
```

### Step 7

At the end of the file add the entry point to the script. This will make sure the `main()` function is executed when `__name__` equals to the string `__main__` which happens when the module is ran as a Python script. 

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def main():

    module = AnsibleModule(argument_spec={})

    response = {"host": "csr1"}

    module.exit_json(msg=response)
  
if __name__ == '__main__':
    main()
```

## Task 2 Testing the Ansible module with a Playbook

After building the Python script that will be used for the module, it's time to test it out using an Ansible playbook.

### Step 1

Create a `YAML` file in the `lab05` folder called `test_module.yml`. Use the `touch` command to create the file and use the `tree` command to make sure the file is stored in the correct location.

```shell
ntc@ntc-training:modules$ cd ../
ntc@ntc-training:lab05$ touch test_module.yml
ntc@ntc-training:lab05$ tree
.
├── modules
│   └── iosxe_gather_configs.py
└── test_module.yml

1 directory, 2 files
ntc@ntc-training:lab05$ 
```

### Step 2

Open and start editing the `test_module.yml` file and add the play definition first.

> Note: Since the module is not built to communicate with networking devices, use `localhost` first to just run the task locally.

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: localhost
  gather_facts: false
  
  tasks:
```

### Step 3

Below the `tasks` key add two tasks. The first one will be the name of the module created `iosxe_gather_configs` and add the register argument to the task to store the output.

In ansible `iosxe_gather_configs` is the module name which will be the same name of the Python script previously built called `iosxe_gather_configs.py`. 

Every module has to return JSON data. In the `iosxe_gather_configs.py` script, the `module.exit_json(msg=response)` method will return that JSON data stored in the `result` variable created by the `register` argument. 

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: localhost
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs: 
      register: result
```

### Step 4

Add another task using the `debug` module and the `var` parameter to view the data stored inside the `result` variable from the previous task.

> Note: The `debug` module allows the user to view data stored in variables. 

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: localhost
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs: 
      register: result

    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result 
```

### Step 5

Execute the Ansible playbook by running the command `ansible-playbook test_module.yml`

```shell
ntc@ntc-training:lab05$ ansible-playbook test_module.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
ERROR! couldn't resolve module/action 'iosxe_gather_configs'. This often indicates a misspelling, missing collection, or incorrect module path.

The error appears to be in '/home/ntc/labs/lab05/test_module.yml': line 9, column 7, but may
be elsewhere in the file depending on the exact syntax problem.

The offending line appears to be:


    - name: GATHER IOSXE CONFIGS
      ^ here
ntc@ntc-training:lab05$ 
```

### Step 6

On the previous step the playbook failed, because it could not find the module it was trying to run. The error shows:

```
ERROR! couldn't resolve module/action 'iosxe_gather_configs'. This often indicates a misspelling, missing collection, or incorrect module path.
```

To fix this issue check where the `ansible.cfg` file is located and copy it over to the current local directory to modify the location of the Ansible module. Execute the `ansible --version` command to view the location.

```shell
ntc@ntc-training:lab05$ ansible --version
ansible 2.9.9
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/etc/ntc/ansible/library']
  ansible python module location = /usr/local/lib/python3.6/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.6.8 (default, Jun 11 2019, 01:16:11) [GCC 6.3.0 20170516]
ntc@ntc-training:lab05$ 
```
> Note: Take a look at `config file` and `configured module search path` because these will change after modifying the `ansible.cfg` file.
> When creating a custom module also known as a third party module, Ansible needs to know where to find that custom module. To do that you need to edit the `ansible.cfg` file and indicate the location of the `iosxe_gather_configs.py` script. 

### Step 7

Copy the `ansible.cfg` file from `/etc/ansible/ansible.cfg` to the current working directory using the `cp` Linux command. Make sure it's copied into the current working directory using the `tree` command.

```shell
ntc@ntc-training:lab05$ 
ntc@ntc-training:lab05$ cp /etc/ansible/ansible.cfg .
ntc@ntc-training:lab05$ 
ntc@ntc-training:lab05$ tree
.
├── ansible.cfg
├── modules
│   └── iosxe_gather_configs.py
└── test_module.yml

1 directory, 3 files
ntc@ntc-training:lab05$ 
```

### Step 8

To indicate the location of the custom module, modify the `ansible.cfg` file by providing the absolute path to the `modules` folder. Change into the `modules` folder and use the `pwd` Linux command to show the current working directory. 


```shell
ntc@ntc-training:lab05$ cd modules/
ntc@ntc-training:modules$ pwd
/home/ntc/labs/lab05/modules
ntc@ntc-training:modules$ 
```

### Step 9

Use the path provided by `pwd` and modify the `library` argument under the `[defaults]` options of the `ansible.cfg` file. 

```
[defaults]
library        = /home/ntc/labs/lab05/modules
filter_plugins = /etc/ntc/ansible/plugins/filter
roles_path    = /etc/ntc/ansible/roles
interpreter_python = /usr/local/bin/python
host_key_checking = False
nocows = 1
retry_files_enabled = False
deprecation_warnings = False

[inventory]
enable_plugins = ini, host_list, script, auto, yaml, toml
```

### Step 10

After saving the changes, execute the `ansible --version` command in the `lab05` folder to view the changes from the output. The output should display a different value on the `config file` and `configured module search path`, both pointing the current working directory. 

```
ntc@ntc-training:modules$ 
ntc@ntc-training:modules$ cd ../
ntc@ntc-training:lab05$ ansible --version
ansible 2.9.9
  config file = /home/ntc/labs/lab05/ansible.cfg
  configured module search path = ['/home/ntc/labs/lab05/modules']
  ansible python module location = /usr/local/lib/python3.6/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.6.8 (default, Jun 11 2019, 01:16:11) [GCC 6.3.0 20170516]
ntc@ntc-training:lab05$ 
```

> Note: Take a look at the values stored in `config file` and `configured module search path` to see how it changed from the previous change.

### Step 11

Execute the Ansible playbook again and view the results. 

```
ntc@ntc-training:lab05$ ansible-playbook test_module.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit
localhost does not match 'all'

PLAY [TEST CUSTOM MODULE WORKS] ********************************************************************

TASK [GATHER IOSXE CONFIGS] ************************************************************************
ok: [localhost]

TASK [VIEW THE DATA STORED IN RESULT] **************************************************************
ok: [localhost] => {
    "result": {
        "changed": false,
        "failed": false,
        "msg": {
            "host": "csr1"
        }
    }
}

PLAY RECAP *****************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

### Step 12

Modify the `test_module.yml` playbook to see if you can access the `host` key and only return the `csr1` string from the output.

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: localhost
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs: 
      register: result

    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result['msg']['host']
```

### Step 13

Execute the Ansible playbook again and view the results. 

```
ntc@ntc-training:lab05$ ansible-playbook test_module.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit
localhost does not match 'all'

PLAY [TEST CUSTOM MODULE WORKS] **********************************************************************

TASK [GATHER IOSXE CONFIGS] **************************************************************************
ok: [localhost]

TASK [VIEW THE DATA STORED IN RESULT] ****************************************************************
ok: [localhost] => {
    "result['msg']['host']": "csr1"
}

PLAY RECAP *******************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

## Task 3 Building the getter module

Now that a basic module has been built to display some data, this task will focus on implementing the code that will make an API call against IOSXE devices to `GET` configuration data.

### Step 1

Open the `iosxe_gather_configs.py` inside the `modules` folder to start editing the code. In the Python script import the needed libraries to make the API calls against the networking devices.

The `requests` library will be used to make HTTP or HTTPS API REST calls against servers that have APIs. The `HTTPBasicAuth` class object will be used to provide authentication details about the server and `requests.packages.urllib3.disable_warnings()` will be used to disable any warnings from the API call (since we are using self-signed certificates in the lab environment).

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


def main():

    module = AnsibleModule(argument_spec={})

    response = {"host": "csr1"}

    module.exit_json(changed=False, msg=response)
  
if __name__ == '__main__':
    main()
```

### Step 2

Inside the `def main()` function add the `url`, `auth`, `headers` and modify the `response` variable. The `url` variable will contain the resource path to the device configuration. The `auth` variable is used to store the device credentials and the `headers` is used to indicate what data encoding to expect from the server/csr1 device. Modify the value of the `response` variable so it contains the response from the API call.

Also modify the `module.exit_json()` method so it can display the data stored inside `response.json()`. 

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


def main():
    
    module = AnsibleModule(argument_spec={})
    
    auth = HTTPBasicAuth('ntc', 'ntc123')
    
    url = 'https://csr1/restconf/data/Cisco-IOS-XE-native:native/'

    headers = {"Accept": "application/yang-data+json"}
    
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    
    module.exit_json(msg=response.json())
  
if __name__ == '__main__':
    main()
```

### Step 3

Change back to the `lab05` folder and change back the `debug` task to print the whole contents of the `result` variable.

```yaml
    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result
```

Execute the `test_module.yml` playbook again to see the output.

> Note: Currently this module is only targeting a single device since the `module` script has the host statically defined in the `url` variable.

```
ntc@ntc-training:lab05$ ansible-playbook test_module.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [TEST CUSTOM MODULE WORKS] *************************************************************************************************************

TASK [GATHER IOSXE CONFIGS] *****************************************************************************************************************
ok: [localhost]

TASK [VIEW THE DATA STORED IN RESULT] *******************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": false,
        "failed": false,
        "msg": {
            "Cisco-IOS-XE-native:native": {
                "Cisco-IOS-XE-diagnostics:diagnostic": {
                    "bootup": {
                        "level": "minimal"
                    }
                },
                "Cisco-IOS-XE-lldp:lldp": {
                    "run": [
                        null
                    ]
                },
                "alias": {
                    "exec": [
                        {
                            "alias-name": "ntcclear",
                            "new-alias-name": "clear platform software vnic-if nv"
                        }
                    ]
                },
                "archive": {
                    "path": "bootflash:archive"
                },
                "boot-end-marker": [
                    null
                ],
                "boot-start-marker": [
                    null
                ],
                "call-home": {
                    "Cisco-IOS-XE-call-home:contact-email-addr": "sch-smart-licensing@cisco.com",
                    "Cisco-IOS-XE-call-home:profile": [
                        {
                            "active": true,
                            "destination": {
                                "transport-method": "http"
                            },
                            "profile-name": "CiscoTAC-1"
                        }
                    ]
                },
                "cdp": {
                    "Cisco-IOS-XE-cdp:run-enable": true
                },
                "control-plane": {},
                "crypto": {
                    "Cisco-IOS-XE-crypto:pki": {
                        "certificate": {
                            "chain": [
                                {
                                    "certificate": [
                                        {
                                            "certtype": "ca",
                                            "serial": "01"
                                        }
                                    ],
                                    "name": "SLA-TrustPoint"
                                },
                                {
                                    "certificate": [
                                        {
                                            "certtype": "self-signed",
                                            "serial": "01"
                                        }
                                    ],
                                    "name": "TP-self-signed-1088426642"
                                }
                            ]
                        },
                        "trustpoint": [
                            {
                                "enrollment": {
                                    "pkcs12": [
                                        null
                                    ]
                                },
                                "id": "SLA-TrustPoint",
                                "revocation-check": [
                                    "crl"
                                ]
                            },
                            {
                                "enrollment": {
                                    "selfsigned": [
                                        null
                                    ]
                                },
                                "id": "TP-self-signed-1088426642",
                                "revocation-check": [
                                    "none"
                                ],
                                "subject-name": "cn=IOS-Self-Signed-Certificate-1088426642"
                            }
                        ]
                    }
                },
                "hostname": "csr1",
                "interface": {
                    "GigabitEthernet": [
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "description": "MANAGEMENT_DO_NOT_CHANGE",
                            "ip": {
                                "address": {
                                    "primary": {
                                        "address": "10.0.0.15",
                                        "mask": "255.255.255.0"
                                    }
                                }
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "1"
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "2"
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "3"
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "4"
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "5"
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "6",
                            "shutdown": [
                                null
                            ]
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "7",
                            "shutdown": [
                                null
                            ]
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "8",
                            "shutdown": [
                                null
                            ]
                        },
                        {
                            "Cisco-IOS-XE-ethernet:negotiation": {
                                "auto": true
                            },
                            "mop": {
                                "enabled": false,
                                "sysid": false
                            },
                            "name": "9",
                            "shutdown": [
                                null
                            ]
                        }
                    ],
                    "Loopback": [
                        {
                            "ip": {
                                "address": {
                                    "primary": {
                                        "address": "100.2.2.4",
                                        "mask": "255.255.255.0"
                                    }
                                }
                            },
                            "name": 100
                        },
                        {
                            "ip": {
                                "address": {
                                    "primary": {
                                        "address": "20.0.0.1",
                                        "mask": "255.255.255.0"
                                    }
                                }
                            },
                            "name": 200
                        }
                    ]
                },
                "ip": {
                    "Cisco-IOS-XE-http:http": {
                        "authentication": {
                            "local": [
                                null
                            ]
                        },
                        "secure-server": true,
                        "server": true
                    },
                    "access-list": {
                        "Cisco-IOS-XE-acl:extended": [
                            {
                                "name": "meraki-fqdn-dns"
                            }
                        ]
                    },
                    "domain": {
                        "lookup": false,
                        "name": "ntc.com"
                    },
                    "forward-protocol": {
                        "protocol": "nd"
                    },
                    "pim": {
                        "Cisco-IOS-XE-multicast:autorp-container": {
                            "autorp": false
                        }
                    },
                    "scp": {
                        "server": {
                            "enable": [
                                null
                            ]
                        }
                    }
                },
                "ipv6": {
                    "Cisco-IOS-XE-mld:mld": {
                        "ssm-map": {
                            "query": {
                                "dns-leaf": false
                            }
                        }
                    }
                },
                "license": {
                    "udi": {
                        "pid": "CSR1000V",
                        "sn": "9SAGBHTUEE9"
                    }
                },
                "line": {
                    "console": [
                        {
                            "first": "0",
                            "stopbits": "1"
                        }
                    ],
                    "vty": [
                        {
                            "first": 0,
                            "last": 4,
                            "login": {
                                "local": [
                                    null
                                ]
                            },
                            "privilege": {
                                "level": {
                                    "number": 15
                                }
                            },
                            "transport": {
                                "input": {
                                    "all": [
                                        null
                                    ]
                                },
                                "preferred": {
                                    "protocol": "ssh"
                                }
                            }
                        },
                        {
                            "first": 5,
                            "last": 15,
                            "login": {
                                "local": [
                                    null
                                ]
                            },
                            "privilege": {
                                "level": {
                                    "number": 15
                                }
                            },
                            "transport": {
                                "input": {
                                    "all": [
                                        null
                                    ]
                                },
                                "preferred": {
                                    "protocol": "ssh"
                                }
                            }
                        }
                    ]
                },
                "login": {
                    "on-success": {
                        "log": {}
                    }
                },
                "memory": {
                    "free": {
                        "low-watermark": {
                            "processor": 72107
                        }
                    }
                },
                "multilink": {
                    "Cisco-IOS-XE-ppp:bundle-name": "authenticated"
                },
                "platform": {
                    "Cisco-IOS-XE-platform:console": {
                        "output": "serial"
                    },
                    "Cisco-IOS-XE-platform:punt-keepalive": {
                        "disable-kernel-core": true
                    },
                    "Cisco-IOS-XE-platform:qfp": {
                        "utilization": {
                            "monitor": {
                                "load": 80
                            }
                        }
                    }
                },
                "redundancy": {},
                "router": {
                    "Cisco-IOS-XE-rip:rip": {}
                },
                "service": {
                    "call-home": [
                        null
                    ],
                    "timestamps": {
                        "debug": {
                            "datetime": {
                                "msec": {}
                            }
                        },
                        "log": {
                            "datetime": {
                                "msec": [
                                    null
                                ]
                            }
                        }
                    }
                },
                "snmp-server": {
                    "Cisco-IOS-XE-snmp:community": [
                        {
                            "access-list-name": "ro",
                            "name": "NETMIKO_FROM_FILE"
                        },
                        {
                            "access-list-name": "ro",
                            "name": "SENT_WITH_NETMIKO"
                        },
                        {
                            "RW": [
                                null
                            ],
                            "name": "ntc-private"
                        },
                        {
                            "RO": [
                                null
                            ],
                            "name": "ntc-public"
                        }
                    ],
                    "Cisco-IOS-XE-snmp:contact": "Kevin",
                    "Cisco-IOS-XE-snmp:location": "Atlanta"
                },
                "spanning-tree": {
                    "Cisco-IOS-XE-spanning-tree:extend": {
                        "system-id": [
                            null
                        ]
                    }
                },
                "subscriber": {
                    "templating": [
                        null
                    ]
                },
                "username": [
                    {
                        "name": "ntc",
                        "password": {
                            "encryption": "0",
                            "password": "ntc123"
                        },
                        "privilege": 15
                    }
                ],
                "version": "17.1",
                "virtual-service": [
                    {
                        "name": "csr_mgmt"
                    }
                ],
                "vrf": {
                    "definition": [
                        {
                            "address-family": {
                                "ipv4": {},
                                "ipv6": {}
                            },
                            "name": "MANAGEMENT"
                        }
                    ]
                }
            }
        }
    }
}

PLAY RECAP **********************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

### Step 4

Modify the `test_module.yml` playbook to see if the data can be accessed and what keys are available.

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: localhost
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs: 
      register: result

    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result['msg']['Cisco-IOS-XE-native:native'].keys()
```

### Step 5

Execute the playbook and view the output. Each key returned contains data from the device configuration. These keys can also be used as a resource endpoint at the end of the `url` in the API call. Since the Python script has the `url` statically defined the data can only be accessed through the JSON output as a Python dictionary.

```
ntc@ntc-training:lab05$ ansible-playbook test_module.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [TEST CUSTOM MODULE WORKS] *************************************************************************************************************

TASK [GATHER IOSXE CONFIGS] *****************************************************************************************************************
ok: [localhost]

TASK [VIEW THE DATA STORED IN RESULT] *******************************************************************************************************
ok: [localhost] => {
    "result['msg']['Cisco-IOS-XE-native:native'].keys()": "dict_keys(['version', 'boot-start-marker', 'boot-end-marker', 'memory', 'call-home', 'service', 'platform', 'hostname', 'archive', 'username', 'vrf', 'ip', 'ipv6', 'cdp', 'interface', 'control-plane', 'login', 'multilink', 'redundancy', 'spanning-tree', 'subscriber', 'crypto', 'router', 'virtual-service', 'snmp-server', 'license', 'alias', 'line', 'Cisco-IOS-XE-diagnostics:diagnostic', 'Cisco-IOS-XE-lldp:lldp'])"
}

PLAY RECAP **********************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

### Step 6

Modify the playbook so it can only access the device version. Provide the needed keys to access the device `version` information. 

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: localhost
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs: 
      register: result

    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result['msg']['Cisco-IOS-XE-native:native']['version']
```

### Step 7

Execute the playbook and view the output.

```
ntc@ntc-training:lab05$ ansible-playbook test_module.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [TEST CUSTOM MODULE WORKS] *************************************************************************************************************

TASK [GATHER IOSXE CONFIGS] *****************************************************************************************************************
ok: [localhost]

TASK [VIEW THE DATA STORED IN RESULT] *******************************************************************************************************
ok: [localhost] => {
    "result['msg']['Cisco-IOS-XE-native:native']['version']": "17.1"
}

PLAY RECAP **********************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

## Task 4 Optimizing the module with parameters

This task will focus on improving the module so it can take in more dynamic data for different devices, credentials and a filter to only return specific data rather than the entire configuration. 

### Step 1

Open the `iosxe_gather_configs.py` script and create a variable called `module_args`. As a value to the `module_args` variable create a dictionary using the `dict` object.

> Note: The `dict` object is just another way to build dictionary data structures. 

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


def main():

    module_args = dict(
        host=dict(),
        user=dict(),
        password=dict()
    )
    
    module = AnsibleModule(argument_spec={})
    
    auth = HTTPBasicAuth('ntc', 'ntc123')
    
    url = 'https://csr1/restconf/data/Cisco-IOS-XE-native:native/'

    headers = {"Accept": "application/yang-data+json"}
    
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    
    module.exit_json(changed=False, msg=response.json())
  
if __name__ == '__main__':
    main()
```

### Step 2

Modify each key inside `module_args` to specify what data type to expect from the user and if the parameter is required or not. Since these parameters will be needed to communicate with the networking devices then they will need to be set as required. These dictionary keys will become the module parameters in the Ansible playbook. 

These parameters will allow the user to dynamically provide input data to the module so it does not run on the same device and use the same credentials every time without the ability to modify the script.

Modify the `auth` variable so that it can pass in the credentials that the user will provide as value in the module task. Also modify the `url` variable so the user can dynamically provide input for what devices to target.

Finally the `module` variable will need to be modified to take in the `module_args` as input into the `argument_spec` which will build the module parameters.

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


def main():

    module_args = dict(
        host=dict(type='str', required=True),
        user=dict(type='str', required=True),
        password=dict(type='str', required=True)
    )
    
    module = AnsibleModule(argument_spec=module_args)
    
    auth = HTTPBasicAuth(module.params['user'], module.params['password'])
    
    url = f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native/"

    headers = {"Accept": "application/yang-data+json"}
    
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    
    module.exit_json(changed=False, msg=response.json())
  
if __name__ == '__main__':
    main()
```

### Step 3


After making the previous changes, create an inventory file and add three `iosxe` devices.

```
ntc@ntc-training:lab05$ 
ntc@ntc-training:lab05$ touch inventory
ntc@ntc-training:lab05$ 
ntc@ntc-training:lab05$ tree
.
├── ansible.cfg
├── inventory
├── modules
│   └── iosxe_gather_configs.py
└── test_module.yml

1 directory, 4 files
ntc@ntc-training:lab05$ 
```

### Step 4

Inside the `ini` inventory file add the three `csr` devices and the credentials as `group_vars`.

```ini
[iosxe]
csr1
csr2
csr3


[iosxe:vars]
username=ntc
password=ntc123
```

### Step 5

Modify the `test_module.yml` playbook to take in all `iosxe` devices and parameterize the data that will be taken as input to the module. Also set the `connection` key as `local` and add the new parameters under the module name. The parameters are going to be the same `keys` created in `iosxe_gather_configs.py` script inside the `module_args` variable.

The values used for each parameter will be `inventory_hostname` - in turn, taking the value of every device stored in the `iosxe` group within this play. The `username` and `password` variables will be rendered from the `iosxe:vars` inside the inventory file.

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: iosxe
  connection: local
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs:
        host: "{{ inventory_hostname }}"
        user: "{{ username }}"
        password: "{{ password }}"
      register: result

    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result['msg']['Cisco-IOS-XE-native:native']['version']
```

### Step 6

After making and saving the changes execute the playbook with the inventory file to view the results. Review the output and notice that this time multiple devices have been targeted and not just the `csr1` device.

```
ntc@ntc-training:lab05$ 
ntc@ntc-training:lab05$ ansible-playbook -i inventory test_module.yml 

PLAY [TEST CUSTOM MODULE WORKS] ********************************************************************************

TASK [GATHER IOSXE CONFIGS] ************************************************************************************
ok: [csr3]
ok: [csr2]
ok: [csr1]

TASK [VIEW THE DATA STORED IN RESULT] **************************************************************************
ok: [csr1] => {
    "result['msg']['Cisco-IOS-XE-native:native']['version']": "17.1"
}
ok: [csr2] => {
    "result['msg']['Cisco-IOS-XE-native:native']['version']": "17.1"
}
ok: [csr3] => {
    "result['msg']['Cisco-IOS-XE-native:native']['version']": "17.1"
}

PLAY RECAP *****************************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
csr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
csr3                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

### Step 7

Currently the module can only return the entire device configuration. A `filter` can be created as a parameter so that the user can specify as a value to only request certain data from the API rather than the entire configuration. Modify the `iosxe_gather_configs.py` script so it can filter out the device configuration.

> Note: Choices and default are two new arguments that can be used to specify the only choices available for the user to input into the parameter and a default argument is used so that when the user does not specify a choice it will get all the device configurations. 

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()


def main():

    module_args = dict(
        host=dict(type="str", required=True),
        user=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        filter=dict(
            type="str",
            required=False,
            default="all",
            choices=[
                "all",
                "version",
                "memory",
                "platform",
                "hostname",
                "username",
                "vrf",
                "ip",
                "cdp",
                "interface",
                "login",
                "snmp-server",
                "lldp",
            ],
        ),
    )

    module = AnsibleModule(argument_spec=module_args)

    auth = HTTPBasicAuth(module.params["user"], module.params["password"])

    url = f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native/"

    headers = {"Accept": "application/yang-data+json"}

    response = requests.get(url, headers=headers, auth=auth, verify=False)

    module.exit_json(msg=response.json())


if __name__ == "__main__":
    main()
```

### Step 8

Add some logic to the Python script so that the correct `URL` endpoint is provided based on the choice from the user.

```python
#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()


def main():

    module_args = dict(
        host=dict(type="str", required=True),
        user=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        filter=dict(
            type="str",
            required=False,
            default="all",
            choices=[
                "all",
                "version",
                "memory",
                "platform",
                "hostname",
                "username",
                "vrf",
                "ip",
                "cdp",
                "interface",
                "login",
                "snmp-server",
                "lldp",
            ],
        ),
    )

    module = AnsibleModule(argument_spec=module_args)

    auth = HTTPBasicAuth(module.params["user"], module.params["password"])

    if module.params["filter"] == "all":
        url = f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native/"
    elif module.params["filter"] == "lldp":
        url = f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native/Cisco-IOS-XE-lldp:lldp"
    else:
        url = f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native/{module.params['filter']}"

    headers = {"Accept": "application/yang-data+json"}

    response = requests.get(url, headers=headers, auth=auth, verify=False)

    module.exit_json(changed=False, msg=response.json())


if __name__ == "__main__":
    main()
```

### Step 9

Modify the `test_module.yml` playbook and add the `filter` parameter and as a value choose `version`.

```yaml
---

- name: TEST CUSTOM MODULE WORKS
  hosts: iosxe
  connection: local
  gather_facts: false
  
  tasks:

    - name: GATHER IOSXE CONFIGS
      iosxe_gather_configs:
        host: "{{ inventory_hostname }}"
        user: "{{ username }}"
        password: "{{ password }}"
        filter: version
      register: result

    - name: VIEW THE DATA STORED IN RESULT
      debug: 
        var: result
```

### Step 10

After saving the playbook execute it and view the results.

```
ntc@ntc-training:lab05$ ansible-playbook -i inventory test_module.yml 

PLAY [TEST CUSTOM MODULE WORKS] *************************************************************************************************************

TASK [GATHER IOSXE CONFIGS] *****************************************************************************************************************
ok: [csr1]
ok: [csr3]
ok: [csr2]

TASK [VIEW THE DATA STORED IN RESULT] *******************************************************************************************************
ok: [csr1] => {
    "result": {
        "changed": false,
        "failed": false,
        "msg": {
            "Cisco-IOS-XE-native:version": "17.1"
        }
    }
}
ok: [csr2] => {
    "result": {
        "changed": false,
        "failed": false,
        "msg": {
            "Cisco-IOS-XE-native:version": "17.1"
        }
    }
}
ok: [csr3] => {
    "result": {
        "changed": false,
        "failed": false,
        "msg": {
            "Cisco-IOS-XE-native:version": "17.1"
        }
    }
}

PLAY RECAP **********************************************************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
csr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
csr3                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

ntc@ntc-training:lab05$ 
```

### Step 11

Try out other value of for the `filter` parameter, both valid and invalid to see what Ansible does.