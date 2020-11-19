# Operator Clauses
## Goals
The goals of this lab are:
* Familiarize yourself with the by() and without() operator clauses.


## Exercises
### Task 1
Calculate the average `dns_query_query_time_ms` by including the tags `host` and `server`.
<details>
  <summary>Reveal Answer</summary>
  
```
avg by (host, server) (dns_query_query_time_ms)
```
</details>

### Task 2
Calculate the maximum `dns_query_query_time_ms` by excluding the tags `db` and `environment`.
<details>
  <summary>Reveal Answer</summary>
  
```
avg without (db, environment) (dns_query_query_time_ms)
```
</details>