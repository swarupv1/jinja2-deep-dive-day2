# Offets
## Goals
The goals of this lab are:
* Familerize yourself with offsets.

## Excercises
### Offset Query
Perform a query to return the admin status`s of the interfaces for the device `zpa_frankfurt_fr6_1` using the `interface_ifAdminStatus` metric, 48 hours ago.
<details>
  <summary>Reveal Answer</summary>
  
```
interface_ifAdminStatus{device="zpa_frankfurt_fr6_1"} offset 48h
```
</details>