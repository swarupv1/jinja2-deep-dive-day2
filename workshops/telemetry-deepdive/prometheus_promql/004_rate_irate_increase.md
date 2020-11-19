# rate(), irate(), increase()
## Goals
The goals of this lab are:
* Familiarize yourself with the rate() function.
* Familiarize yourself with the irate() function.
* Familiarize yourself with the increase() function.

## Exercises
### Task 1
Return the per-second increase of the `interface_in_octets` metric, over a 5 minute range for `interface` `GigabitEthernet0/2`.
<details>
  <summary>Reveal Answer</summary>
  
```
rate(interface_in_octets{interface="GigabitEthernet0/2"}[5m])
```
</details>


### Task 2
Return the per-second increase of the `interface_in_octets` metric, over a 5 minute range for `interface` `GigabitEthernet0/2` between the last 2 values of the time range.
<details>
  <summary>Reveal Answer</summary>
  
```
irate(interface_in_octets{interface="GigabitEthernet0/2"}[5m])
```
</details>

### Task 3
Return the total increase of the `interface_in_octets` metric, over a 5 minute range for `interface` `GigabitEthernet0/2`.
<details>
  <summary>Reveal Answer</summary>
  
```
increase(interface_in_octets{interface="GigabitEthernet0/2"}[5m])
```
</details>