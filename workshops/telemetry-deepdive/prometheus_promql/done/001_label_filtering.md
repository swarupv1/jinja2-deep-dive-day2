# Label Filtering
## Goals
The goals of this lab are:
* Familerize yourself with the Thanos UI.
* Perform basic label filtering to return the active ASA VPN clients.

## Excercises
### Basic Query
Run the query: `asa_anyconnect_client_active` and view the results within the `Console`.
### Query with Label Selection (Equal)
Perform a query to return all active ASA VPN clients (`asa_anyconnect_client_active`) for `frankfurt`.
<details>
  <summary>Reveal Answer</summary>
  
```
asa_anyconnect_client_active{site="frankfurt"}
```
</details>


### Query with Label Selection (Not Equal)
Perform a query to return all active ASA VPN clients (`asa_anyconnect_client_active`) for all sites excluding `frankfurt`.
<details>
  <summary>Reveal Answer</summary>
  
```
asa_anyconnect_client_active{site!="frankfurt"}
```
</details>



### Query with Label Selection (Regex Match)
Perform a query to return all active ASA VPN clients (`asa_anyconnect_client_active`) for all sites ending in the numbers `2` or `3`.
<details>
  <summary>Reveal Answer</summary>
  
```
asa_anyconnect_client_active{device=~".*[2-3]"}
```
</details>

