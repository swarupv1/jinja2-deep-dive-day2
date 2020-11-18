# Instant vs Range Vectors
## Goals
The goals of this lab are:
* Familiarize yourself with querying and returning instant vectors.
* Familiarize yourself with querying and returning range vectors.

## Excercises
### Instant Vector
Perform a query to return an instant vector for the metric `interface_in_octets` for `hostname=rAWPLblo02` and `interface="GigabitEthernet0/2"`.
<details>
  <summary>Reveal Answer</summary>
  
```
interface_in_octets{hostname="rAWPLblo02",interface="GigabitEthernet0/2"}
```
</details>

### Range Vector
Perform a query to return the range vector for the metric `interface_in_octets` for `hostname=rAWPLblo02` and `interface="GigabitEthernet0/2"` over 5 mins.
<details>
  <summary>Reveal Answer</summary>
  
```
interface_in_octets{hostname="rAWPLblo02",interface="GigabitEthernet0/2"}[5m]
```
</details>

