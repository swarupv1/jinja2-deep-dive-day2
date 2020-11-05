# Extending Ansible - Lab 06

In this lab exercise you will create a custom module for Ansible that performs changes against the IOS-XE RESTCONF API endpoints, specifically to manage VRF configuration.

## Task 1 - Building the VRF REST Module

To start with, you will create a new module that makes changes to a specific VRF's description via the API.

### Step 1

In your terminal on the lab workstation, change into the `/home/ntc/labs/lab06` folder, creating it if it doesn't exist.

```
ntc@ntc-training:~$ mkdir -p /home/ntc/labs/lab06
ntc@ntc-training:~$ cd /home/ntc/labs/lab06
ntc@ntc-training:lab06$
```

### Step 2

Create a folder named `modules` and in it a file called `iosxe_rest_vrf.py`.

```
ntc@ntc-training:lab06$ mkdir modules
ntc@ntc-training:lab06$ touch modules/iosxe_rest_vrf.py
ntc@ntc-training:lab06$ tree
.
└── modules
    └── iosxe_rest_vrf.py

1 directory, 1 file
```

### Step 3

Open the `modules/iosxe_rest_vrf.py` file in your editor and add the following code:

```py
#!/usr/bin/env python3

DOCUMENTATION = """
"""

EXAMPLES = """
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
import requests
import json

requests.packages.urllib3.disable_warnings()

def main():
    pass

if __name__ == "__main__":
    main()
```

> This is just the scaffolding for the module and over the following steps you will build its full functionality and documentation.

### Step 4

In the `modules/iosxe_rest_vrf.py` file, change the EXAMPLES string to the following value.

```py
EXAMPLES = """
# Collect Device Version
- name: UPDATE VRF DESCRIPTION
  iosxe_rest_vrf:
    host: "{{ inventory_hostname }}"
    user: "{{ username }}"
    password: "{{ password }}"
    name: CORP
    description: VRF FOR CORPORATE USERS
"""
```

You can use this to build a visual representation of how the module would be used - it helps to work out what parameters it needs when called from a playbook.

Since the module will be sending REST calls to an authenticated API, you need the device's IP or hostname (the `host` parameter), and the `user` and `password`.

As for the other parameters, the goal here is to provide an abstracted interface to make changes to a VRF's description. So you need to provide a VRF `name` and a VRF `description`.

### Step 5

In the `modules/iosxe_rest_vrf.py` file, change the DOCUMENTATION string to the following value.

```py
DOCUMENTATION = """
---
module: iosxe_rest_vrf
short_description: This module updates VRF configuration via the IOSXE REST API.
version_added: "1.0.0"
description: This module uses the requests Python library to make API calls against the IOSXE device.
options:
    host:
        description: Enter the IP or hostname of the IOSXE device
        required: true
        type: str
    user:
        description: Enter the device username
        required: true
        type: str
    password:
        description: Enter the device password
        required: true
        type: str
    verify:
        description: Enable or disable SSL verification, it will disabled by default
        required: false
        type: bool
    name:
        description: The VRF's name you want to manage
        required: true
        type: str
    description:
        description: The VRF's description (optional)
        required: false
        type: str

author:
    - NetworkToCode (@networktocode)
"""
```

This is what `ansible-doc` will use to generate the documentation page for the custom module and is a more programmatic way of defining each parameter you sketched out in the previous step's EXAMPLES.

Take special notice of each parameter's metadata - i.e. `required`, `type`, and `description`.

### Step 6

Continue editing the file and replace the `pass` statement (which does nothing) in the `main()` function as shown below.

```py
def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        host=dict(type="str", required=True),
        user=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        verify=dict(type="bool", default=False),
        name=dict(type="str", required=True),
        description=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # prepare the standard return object
    result = dict(changed=False)
```

The `module_args` dictionary holds the **argument spec** or the actual code that specifies the module parameters as detailed in the `DOCUMENTATION` string earlier. This is used by the Ansible engine during execution.

Since this module does not yet support `check mode`, we set that when instantiating the AnsibleModule class. Finally, `result` is a dictionary that holds the data you wish the module to return to the Ansible engine once it finishes execution.

> The `module_args` and the `DOCUMENTATION` string should be kept in sync! Any discrepancies will only cause confusion to users of your module.

### Step 7

Update the `RETURN` string with the following code:

```py
RETURN = """
# These are examples of possible return values, and in general should use other names for return values.
sent_payload:
    description: The VRF data that will be sent to the API via the PATCH request
    type: str
    returned: always
    sample: '{"Cisco-IOS-XE-native:definition": {"description": "VRF FOR CORPORATE USERS", "name": "CORP"}}}'
msg:
    description: A status message including the HTTP response code.
    type: str
    returned: always
    sample: 'OK 204'
"""
```

This is used by documentation to explain what additional data the module is returning - here the plan is to return `sent_payload` (the JSON API payload built for the request) and `msg` which is a custom message that includes the HTTP response code (e.g. 204 or 404).

### Step 8

In the `/home/ntc/labs/lab06` folder, create a new file called `ansible.cfg` with the content below. You need to tell Ansible where to find your custom module - in this case you're telling it to search in the current path for a folder called `modules`.

```
[defaults]

# Disable automatic facts gathering.
gathering = explicit

# Instruct Ansible to look locally for modules
library = modules
```

### Step 9

Verify that your folder structure looks like the output below.

```
ntc@ntc-training:lab06$ tree
.
├── ansible.cfg
└── modules
    └── iosxe_rest_vrf.py

1 directory, 2 files
```

### Step 10

Verify where Ansible looks for modules, also called the library or module search path.

```
ntc@ntc-training:lab06$ ansible --version
ansible 2.9.9
  config file = /home/ntc/labs/lab06/ansible.cfg
  configured module search path = ['/home/ntc/labs/lab06/modules']
  ansible python module location = /usr/local/lib/python3.6/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.6.8 (default, Jun 11 2019, 01:16:11) [GCC 6.3.0 20170516]
```

### Step 11

Since the module's documentation is fully defined, you can already inspect it using the `ansible-doc` command. Notice that the output is built from the information you defined in the `DOCUMENTATION`, `EXAMPLES`, and `RETURN` strings inside of your custom module file.

```
ntc@ntc-training:lab06$ ansible-doc iosxe_rest_vrf
> IOSXE_REST_VRF    (/home/ntc/labs/lab06/modules/iosxe_rest_vrf.py)

        This module uses the requests Python library to make API calls against the IOSXE device.

  * This module is maintained by The Ansible Community
OPTIONS (= is mandatory):

- description
        The VRF's description (optional)
        [Default: (null)]
        type: str

= host
        Enter the IP or hostname of the IOSXE device

        type: str

= name
        The VRF's name you want to manage

        type: str

= password
        Enter the device password

        type: str

= user
        Enter the device username

        type: str

- verify
        Enable or disable SSL verification, it will disabled by default
        [Default: (null)]
        type: bool


AUTHOR: NetworkToCode (@networktocode)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:

# Collect Device Version
- name: UPDATE VRF DESCRIPTION
  iosxe_rest_vrf:
    host: "{{ inventory_hostname }}"
    user: "{{ username }}"
    password: "{{ password }}"
    name: CORP
    description: VRF FOR CORPORATE USERS


RETURN VALUES:

# These are examples of possible return values, and in general should use other names for return values.
sent_payload:
    description: The VRF data that will be sent to the API via the PATCH request
    type: str
    returned: always
    sample: '{"Cisco-IOS-XE-native:definition": {"description": "VRF FOR CORPORATE USERS", "name": "CORP"}}}'
msg:
    description: A status message including the HTTP response code.
    type: str
    returned: always
    sample: 'OK 204'
```

### Step 12

Time to build the actual REST API call! Edit the `iosxe_rest_vrf.py` file and add the following code to the end of the `main()` function definition.

```py
# set up the API request parameters
    auth = requests.auth.HTTPBasicAuth(module.params["user"], module.params["password"])
    # this module supports only json
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }
    # this module supports only the Cisco-IOS-XE-native data model
    base_url = (
        f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native"
    )
    # manages vrf by name
    url = f"{base_url}/Cisco-IOS-XE-native:vrf/definition={module.params['name']}"

    # build PATCH request payload
    payload = {"Cisco-IOS-XE-native:definition": {"name": f"{module.params['name']}"}}

    # only set if it's defined since an empty description is not acceptable by the API
    if module.params["description"]:
        payload["Cisco-IOS-XE-native:definition"][
            "description"
        ] = f"{module.params['description']}"

    # add this to the module output for easier troubleshooting
    result["sent_payload"] = payload
```

This code builds the necessary variables needed to send an HTTP API call (URL, data, headers, authentication) from both hard-coded values (e.g. we only support JSON data) and dynamic module parameters (e.g. VRF name, description, hostname, user, password).

### Step 13

The URL and payload are built by referencing an example output from the IOS-XE API for the VRF object. Take some time to compare the structure below to the code added in the previous step.

```json
{
  "Cisco-IOS-XE-native:vrf": {
    "definition": [
      {
        "name": "CORP",
        "description": "VRF for Corporate Users"
      },
      {
        "name": "MANAGEMENT",
        "address-family": {
          "ipv4": {
          },
          "ipv6": {
          }
        }
      }
    ]
  }
}
```

### Step 14

Finally, add this block of code at the end of the `main()` function. This actually sends the request to the API and handles the results accordingly.

```py
    # send the API request to the device (PATCH)
    response = requests.patch(
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=auth,
        verify=module.params["verify"],
    )

    # return the json response from the API if it exists
    if response.text:
        result["json"] = response.json()

    # since it's a blind PATCH request, always assume a change was made
    if response.ok:
        result["changed"] = True
        result["msg"] = f"OK {response.status_code}"
    # the request failed so the module should fail as well
    else:
        result["msg"] = f"API request failed with code {response.status_code}"
        module.fail_json(**result)

    # return successfully and pass the results to ansible
    module.exit_json(**result)
```

If the API request is successful (`response.ok` is True), then inform Ansible that the modules has performed a change.

In case of a failure (API is unavailable, authentication fails, resource does not exist etc.), you must also inform Ansible that the module has failed and provide an error message.

### Step 15

The full `iosxe_rest_vrf.py` file is included below for reference - compare it with your own before going further!

```py
#!/usr/bin/env python3

DOCUMENTATION = """
---
module: iosxe_rest_vrf
short_description: This module updates VRF configuration via the IOSXE REST API.
version_added: "1.0.0"
description: This module uses the requests Python library to make API calls against the IOSXE device.
options:
    host:
        description: Enter the IP or hostname of the IOSXE device
        required: true
        type: str
    user:
        description: Enter the device username
        required: true
        type: str
    password:
        description: Enter the device password
        required: true
        type: str
    verify:
        description: Enable or disable SSL verification, it will disabled by default
        required: false
        type: bool
    name:
        description: The VRF's name you want to manage
        required: true
        type: str
    description:
        description: The VRF's description (optional)
        required: false
        type: str

author:
    - NetworkToCode (@networktocode)
"""

EXAMPLES = """
# Collect Device Version
- name: UPDATE VRF DESCRIPTION
  iosxe_rest_vrf:
    host: "{{ inventory_hostname }}"
    user: "{{ username }}"
    password: "{{ password }}"
    name: CORP
    description: VRF FOR CORPORATE USERS
"""

RETURN = """
# These are examples of possible return values, and in general should use other names for return values.
sent_payload:
    description: The VRF data that will be sent to the API via the PATCH request
    type: str
    returned: always
    sample: '{"Cisco-IOS-XE-native:definition": {"description": "VRF FOR CORPORATE USERS", "name": "CORP"}}}'
msg:
    description: A status message including the HTTP response code.
    type: str
    returned: always
    sample: 'OK 204'
"""

from ansible.module_utils.basic import AnsibleModule
import requests
import json

requests.packages.urllib3.disable_warnings()


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        host=dict(type="str", required=True),
        user=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        verify=dict(type="bool", default=False),
        name=dict(type="str", required=True),
        description=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # prepare the standard return object
    result = dict(changed=False)

    # set up the API request parameters
    auth = requests.auth.HTTPBasicAuth(module.params["user"], module.params["password"])
    # this module supports only json
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }
    # this module supports only the Cisco-IOS-XE-native data model
    base_url = (
        f"https://{module.params['host']}/restconf/data/Cisco-IOS-XE-native:native"
    )
    # manages vrf by name
    url = f"{base_url}/Cisco-IOS-XE-native:vrf/definition={module.params['name']}"

    # build PATCH request payload
    payload = {"Cisco-IOS-XE-native:definition": {"name": f"{module.params['name']}"}}

    # only set if it's defined since an empty description is not acceptable by the API
    if module.params["description"]:
        payload["Cisco-IOS-XE-native:definition"][
            "description"
        ] = f"{module.params['description']}"

    # add this to the module output for easier troubleshooting
    result["sent_payload"] = payload

    # send the API request to the device (PATCH)
    response = requests.patch(
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=auth,
        verify=module.params["verify"],
    )

    # return the json response from the API if it exists
    if response.text:
        result["json"] = response.json()

    # since it's a blind PATCH request, always assume a change was made
    if response.ok:
        result["changed"] = True
        result["msg"] = f"OK {response.status_code}"
    # the request failed so the module should fail as well
    else:
        result["msg"] = f"API request failed with code {response.status_code}"
        module.fail_json(**result)

    # return successfully and pass the results to ansible
    module.exit_json(**result)


if __name__ == "__main__":
    main()
```

## Task 2 - Using the VRF Module

Here you will start using the basic VRF module you created to make some changes to a CSR's configuration.

### Step 1

In the `/home/ntc/labs/lab06` folder, create a new file called `pb_vrf.yml` with the content below.

```yml
---

- name: TESTING THE IOSXE_REST_VRF MODULE
  hosts: localhost
  gather_facts: false

  tasks:
    - name: UPDATE DESCRIPTION FOR CORP VRF
      iosxe_rest_vrf:
        host: csr1
        user: ntc
        password: ntc123
        name: CORP
        description: VRF FOR CORPORATE USERS
```

> Note: All the necessary data is embedded into the playbook, since this is early testing!

### Step 2

Run the playbook `pb_vrf.yml`. It will fail.

```
ntc@ntc-training:lab06$ ansible-playbook pb_vrf.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match
'all'

PLAY [TESTING THE IOSXE_REST_VRF MODULE] *********************************************************************************

TASK [UPDATE DESCRIPTION FOR CORP VRF] ***********************************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "json": {"errors": {"error": [{"error-message": "patch to a nonexistent resource", "error-path": "/Cisco-IOS-XE-native:native/vrf/definition=CORP", "error-tag": "invalid-value", "error-type": "application"}]}}, "msg": "API request failed with code 404", "sent_payload": {"Cisco-IOS-XE-native:definition": {"description": "VRF FOR CORPORATE USERS", "name": "CORP"}}}

PLAY RECAP ***************************************************************************************************************
localhost                  : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

Why did it fail? Well, the PATCH request needs to modify an existing VRF. Since the `CORP` VRF doesn't actually exist on the `csr1` device, the API call fails. Inspect the error message, do you see the "patch to a nonexistent resource" text in there?

Look at the rest of the information provided, it is coming from your code! There's `sent_payload` in there showing you the request data, and there's `msg` showing the error code 404. The `json` field actually contains the full response given by the API.

### Step 3

In a separate terminal on the lab workstation, open an SSH connection to the `csr1` device. Verify the configuration (there's no VRF CORP yet!) and manually add the `CORP` VRF into the configuration.

```
ntc@ntc-training:lab06$ ssh csr1
Warning: Permanently added 'csr1,172.18.0.6' (RSA) to the list of known hosts.
Password:


csr1#sh run vrf
Building configuration...

Current configuration : 127 bytes
vrf definition MANAGEMENT
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
!
!
end

csr1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
csr1(config)#vrf definition CORP
csr1(config-vrf)#end
csr1#

csr1#sh run vrf CORP
Building configuration...

Current configuration : 27 bytes
vrf definition CORP
!
end
csr1#
```

### Step 4

Run the playbook `pb_vrf.yml` again. It will succeed since the CORP VRF now exists. It has also made a change to the VRF's description as per the module parameters!

```
ntc@ntc-training:lab06$ ansible-playbook pb_vrf.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match
'all'

PLAY [TESTING THE IOSXE_REST_VRF MODULE] *********************************************************************************

TASK [UPDATE DESCRIPTION FOR CORP VRF] ***********************************************************************************
changed: [localhost]

PLAY RECAP ***************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Step 5

Back on the `csr1` CLI, check what's the running-config looking like now. As you can see, the description was successfully added.

```
csr1#sh run vrf CORP
Building configuration...

Current configuration : 64 bytes
vrf definition CORP
 description VRF FOR CORPORATE USERS
!
end

csr1#
```

### Step 6

Let's make the playbook more dynamic and use an inventory with multiple devices.

Create an `inventory` file with the following content:

```
[iosxe]
csr[1:3]

[iosxe:vars]
ansible_user=ntc
ansible_password=ntc123
```

### Step 7

Create a new playbook `pb_vrf_descriptions.yml` with the following content:

```yml
---

- name: TESTING THE IOSXE_REST_VRF MODULE
  hosts: iosxe
  gather_facts: false

  tasks:
    - name: UPDATE DESCRIPTION FOR CORP VRF
      iosxe_rest_vrf:
        host: "{{ inventory_hostname }}"
        user: "{{ ansible_user }}"
        password: "{{ ansible_password }}"
        name: CORP
        description: VRF FOR CORPORATE USERS
      delegate_to: localhost
```

> Important to note that `delegate_to: localhost` instructs Ansible to run the module locally as otherwise it would attempt to open an SSH connection an execute it remotely on the managed device (the default behavior).

### Step 8

Run the playbook `pb_vrf_descriptions.yml`. It's failing as expected on csr2 and csr3 since they are missing the `CORP` VRF. But you are now using your inventory data instead of hardcoding connection details inside of the playbook.

```
ntc@ntc-training:lab06$ ansible-playbook -i inventory pb_vrf_descriptions.yml

PLAY [TESTING THE IOSXE_REST_VRF MODULE] *********************************************************************************

TASK [UPDATE DESCRIPTION FOR CORP VRF] ***********************************************************************************
fatal: [csr2 -> localhost]: FAILED! => {"changed": false, "json": {"errors": {"error": [{"error-message": "patch to a nonexistent resource", "error-path": "/Cisco-IOS-XE-native:native/vrf/definition=CORP", "error-tag": "invalid-value", "error-type": "application"}]}}, "msg": "API request failed with code 404", "sent_payload": {"Cisco-IOS-XE-native:definition": {"description": "VRF FOR CORPORATE USERS", "name": "CORP"}}}
changed: [csr1 -> localhost]
fatal: [csr3 -> localhost]: FAILED! => {"changed": false, "json": {"errors": {"error": [{"error-message": "patch to a nonexistent resource", "error-path": "/Cisco-IOS-XE-native:native/vrf/definition=CORP", "error-tag": "invalid-value", "error-type": "application"}]}}, "msg": "API request failed with code 404", "sent_payload": {"Cisco-IOS-XE-native:definition": {"description": "VRF FOR CORPORATE USERS", "name": "CORP"}}}

PLAY RECAP ***************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
csr2                       : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
csr3                       : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

### Step 9

Feel free to experiment at this stage with different descriptions and add the VRF to the other CSRs so the playbook succeeds!
