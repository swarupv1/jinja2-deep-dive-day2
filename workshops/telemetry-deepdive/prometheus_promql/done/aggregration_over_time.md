# Aggregation over Time
## Goals
The goals of this lab are:
* Familerize yourself with the aggregation over time based functions.


## Excercises
### Task 1
Calculate the maximum number of `asa_anyconnect_client_active` over a 24 hour time period, for all sites.
<details>
  <summary>Reveal Answer</summary>
  
```
max_over_time(asa_anyconnect_client_active{}[24h])
```
</details>

### Task 2
Calulate the top 5% `dns_query_query_time_ms` times (highest ms) for the `site`=`lessines` and the `sensor_name`=`google_public_dns_a` over a 5 minute time range.
<details>
  <summary>Reveal Answer</summary>
  
```
quantile_over_time(0.95, dns_query_query_time_ms{site="lessines",sensor_name="google_public_dns_a"}[5m])
```
</details>