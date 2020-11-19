# Aggregation Operators
## Goals
The goals of this lab are:
* Familiarize yourself with the sum() aggregation operator.
* Familiarize yourself with the count() aggregation operator.

## Exercises
### Task 1
Calculate the total number of `asa_anyconnect_client_active` sessions across all devices within the `frankfurt` site.
<details>
  <summary>Reveal Answer</summary>
  
```
sum(asa_anyconnect_client_active{site="frankfurt"})
```
</details>


### Task 2
Calculate the total number of devices within the `frankfurt` site using the metric `asa_anyconnect_client_active`.
<details>
  <summary>Reveal Answer</summary>
  
```
count(asa_anyconnect_client_active{site="frankfurt"})
```
</details>