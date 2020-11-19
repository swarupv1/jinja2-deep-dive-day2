# Aggregation over Time
## Goals
The goals of this lab are:
* Familiarize yourself with the aggregation over time based functions.


## Exercises
### Task 1
Calculate the maximum number of `asa_anyconnect_client_active` over a 24 hour time period, for all sites.
<details>
  <summary>Reveal Answer</summary>
  
```
max_over_time(asa_anyconnect_client_active{}[24h])
```
</details>

### Task 2
Calculate the average `dns_query_query_time_ms` over a 5 minute time range for the `site`=`lessines` and the `sensor_name`=`google-public-dns-a.google.com`.
<details>
  <summary>Reveal Answer</summary>
  
```
avg_over_time(dns_query_query_time_ms{site="lessines", sensor="google-public-dns-a.google.com"}[5m])
```
</details>