# Advanced Topics
## Goals
The goals of this lab are:
* Familerize yourself with the aggregation over time quantile based functions.


## Excercises
### Task 1
Calulate the top 5% `dns_query_query_time_ms` times (highest ms) for the `site`=`lessines` and the `sensor_name`=`google_public_dns_a` over a 5 minute time range.
<details>
  <summary>Reveal Answer</summary>
  
```
quantile_over_time(0.95, dns_query_query_time_ms{site="lessines",sensor_name="google_public_dns_a"}[5m])
```
</details>