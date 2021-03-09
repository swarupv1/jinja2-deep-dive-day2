# Challenge - Introduction to HTTP APIs

The goal of this exercise is to learn about HTTP APIs. You will learn how to recognise different types of HTTP APIs and how to interact with them using cURL and Postman.

## Exercise Overview

### Prerequisites

- You need to have `cURL` utility installed on your machine.
  - If you don't have `cURL` you should use your package manager to install it. E.g. for Ubuntu you would use `sudo apt install curl`.

- You need to have the `Postman` program installed. You can download it from [Postman website](https://www.postman.com/downloads/).

### Tasks

Submitting your solution for this challenge is optional - feel free to ask for help via email, chat, or at the open office hours if you get stuck!


#### Task 1 - HTTP methods

REST APIs reuse existing HTTP methods to perform CRUD (create, retrieve, update, delete) operations.

You are asked to:

1. Write down next to each of the methods what it is used for.

2. Give an example of how each method could perform an operation against the API of NetBox or a network device.

3. Explain the difference between PATCH and PUT methods.

HTTP methods:

- GET
- POST
- PATCH
- PUT
- DELETE


#### Task 2 - HTTP headers

HTTP headers carry metadata about a request and are very important when talking to APIs.

Below are the names of a few HTTP headers. Can you explain what each of them is used for?

1. Accept

2. Authorization

3. Content-Type


#### Task 3 - HTTP headers - content types

When communicating with APIs you will often need to specify the type of data you want to receive or send.

For this task, you are asked to write down the header name, and the value the header should have. Do it for each of the below cases:

1. You are talking to the REST API and you want to receive `json` data.

2. You are creating a new resource with POST request, using `json` data, sent to REST API .

3. You want a device running RESTCONF to return interface data in `xml` format.

4. You want to create a new VLAN on your device using RESTCONF API and `json` data.

> Hint: Pay attention to API types when choosing data type.

#### Task 4 - REST and non-REST APIs

RESTful APIs tend to behave in a similar way, once you learned one it's easier to get started with another. Non-REST API usually requires more effort to get started. By looking at methods and URL format used by the API we might be able to tell if an API is RESTful or not.

Below you're given some information on several APIs. Answer how likely it is that the API is RESTful for each of them. Provide a short explanation for each of your answers.

1. This system has an API that uses POST method to retrieve information on the objects.

2. Network device with API using GET, POST, PATCH, PUT, DELETE. Different resources use different URL paths.

3. Network device with API that requires CLI commands to be sent in the data payload.

> Hint: Think about REST principles and how HTTP methods map to CRUD operations in RESTful APIs.

#### TASK 5 - NetBox API - getting data

In this task you are asked to retrieve some data from NetBox via API.

For this task use the below freely available online instance of NetBox:

- URL: https://netboxdemo.com/
- API token: 72830d67beff4ae178b94d8f781842408df8069d

1. Using `Postman` get data on existing VLANs. Take a screenshot showing request details and response.

2. Using `Postman` get data on an individual VLAN. Take a screenshot showing request details and response.

3. Using `cURL` get data on device manufacturers. Copy the command you used and the output.

4. Using `cURL` get data on a single device manufacturer. Copy the command you used and the output.

> Hints:
>   - Don't forget to submit authorization details.
>   - API documentation is available at: https://netboxdemo.com/api/docs/
>   - NetBox documentation is available at: https://netbox.readthedocs.io/en/stable/
>   - With cURL, you can prettify output from NetBox API by adding `; indent=4` characters right after the value of the content type you want to get back.

#### TASK 6 - NetBox API - modifying data

In this task you are asked to create and modify resources stored in NetBox using its API. 

For this task use the below freely available online instance of NetBox:

- URL: https://netboxdemo.com/
- API token: 72830d67beff4ae178b94d8f781842408df8069d

1. Using `Postman` create a new VLAN. Use VLAN ID that's not currently in use. You can give a description to your VLAN. Take a screenshot showing request details and response.

2. Using `Postman` update the VLAN you just created. You need to change its description to `BACKUP_VLAN_{VID}`, where `{VID}` is VLAN ID of your VLAN, e.g. `BACKUP_VLAN_911`.

    Data you send to an API should contain only one key-value pair. Take a screenshot showing request details and response.

3. Using `cURL` delete the VLAN object you created in step 1. Use the `-i` option to see headers in the response. This will show you response code among other things. Copy the command you used and the output.

> Hints:
>   - When performing merge and delete operations you need to specify the URL object you're modifying.
>   - Don't forget to provide authentication details when using cURL.
>   - Some REST API responses contain no data but all should have HTTP response code.


#### Task 7 - IOS-XE RESTCONF - getting data
 
In this task you are asked to use API to retrieve configuration items from a Cisco device running IOS-XE.

For this task use the below Cisco always-on sandbox device:

- URL: https://ios-xe-mgmt.cisco.com:9443
- username: developer
- password: C1sco12345

1. Using `Postman` retrieve interfaces configured on this device. Use the `Cisco-IOS-XE-native` YANG model for this task. Take a screenshot showing request details and response.

2. Using `Postman` retrieve description of interface `GigabitEthernet1`. Use the `Cisco-IOS-XE-native` YANG model for this task. Take a screenshot showing request details and response.

3. Using `cURL` retrieve route maps configured on this device. Use the `Cisco-IOS-XE-native` YANG model for this task. Copy the command you used and the output.

> Hints:
>  - Base URL for RESTCONF API on IOS-XE is `https://ios-xe-mgmt.cisco.com:9443/restconf/data/`.
>  - To navigate nested data structure in RESTCONF place name of the key after `/` character. For lists use `=` notation after the name of the resource to get a specific item. E.g. `../FastEthernet=1/` would return data on interface `FastEthernet1` with `FastEthernet` being a list container.


#### Task 8 - Bonus (Intermediate) - IOS-XE RESTCONF - creating resource

In this task you are asked to use API to create a new resource on a Cisco device running IOS-XE.

For this task use the below Cisco always-on sandbox device:

- URL: https://ios-xe-mgmt.cisco.com:9443
- username: developer
- password: C1sco12345

1. Using `Postman` create a new Loopback interface on this device. Use the first available interface number in range 100 - 999. Your interface MUST have description and IP address. Use the `Cisco-IOS-XE-native` YANG model for this task. Take a screenshot showing request details and response.

> Hint: To build data needed to create interface you can reuse data returned by GET method.


#### Task 9 - Bonus (Advanced) - IOS-XE RESTCONF - modifying resource

In this task you are asked to use API to modify an existing resource on a Cisco device running IOS-XE.

For this task use the below Cisco always-on sandbox device:

- URL: https://ios-xe-mgmt.cisco.com:9443
- username: developer
- password: C1sco12345

1. Using `Postman` change description of the Loopback interface you created in Task 8. New description should be created by appending string `-fixme` to existing description. Use the merge operation and `Cisco-IOS-XE-native` YANG model for this task. Take a screenshot showing request details and response.

> Hint: To update resource you can specify the type and name of the target interface in your data or in the resource URL.

#### Task 10 - Bonus (Advanced) - IOS-XE RESTCONF - deleting resource

In this task you are asked to use API to delete an existing resource on a Cisco device running IOS-XE.

For this task use the below Cisco always-on sandbox device:

- URL: https://ios-xe-mgmt.cisco.com:9443
- username: developer
- password: C1sco12345

1. Using `cURL` delete the Loopback interface you created in Task 8. Use URL to specify the interface to be deleted. Use the `Cisco-IOS-XE-native` YANG model for this task. Provide a copy of the command you used and the output.

2. Using `cURL` confirm the Loopback interface is gone from the device. Use URL to specify the interface you want to check. Use the `Cisco-IOS-XE-native` YANG model for this task. Provide a copy of the command you used and the output.

> Hints:
> - You need to refer to cURL docs to find out which option is used for authentication.
> - You need to allow a  self-signed certificate in this task. Find in the cURL docs option that does that.
> - Key name can be used in URL after the name of the resource using `=` character.

### Reference Enablement Material
 
- Introduction to Data Structures
- Introduction to REST APIs
- Network Programming and Automation course
 
> Note: Recordings of the relevant sessions can be found online at: https://training.networktocode.com/ 

### External references

- Official NetBox docs, section on API: https://netbox.readthedocs.io/en/stable/rest-api/overview/
- NetBox Demo built-in API docs: https://netboxdemo.com/api/docs/
- cURL Documentation: https://curl.se/docs/tooldocs.html
- RFC8040 - RESTCONF Protocol. Very detailed and technical but still one of the best resources for learning RESTCONF: https://tools.ietf.org/html/rfc8040
- Wikipedia article on REST. Good overview and some history of REST architecture. https://en.wikipedia.org/wiki/Representational_state_transfer
- YANG catalog. Tools for working with and exploring YANG models. https://yangcatalog.org/
  - See for example `yang-search` results for `Cisco-IOS-XE-native` YANG model: https://yangcatalog.org/yang-search/yang_tree/Cisco-IOS-XE-native@2019-11-01
