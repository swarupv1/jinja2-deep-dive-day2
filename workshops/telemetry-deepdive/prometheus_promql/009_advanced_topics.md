# Advanced Topics
## Goals
The goals of this lab are:
* Familiarize yourself with the aggregation over time quantile based functions.
* Familiarize yourself with the standard deviation operator.


## Exercises
### Task 1
Calulate the top 5% `dns_query_query_time_ms` times (highest ms) for the `site`=`lessines` and the `sensor_name`=`google_public_dns_a` over a 5 minute time range.
<details>
  <summary>Reveal Answer</summary>
  
```
quantile_over_time(0.95, dns_query_query_time_ms{site="lessines",sensor_name="google_public_dns_a"}[5m])
```
</details>

### Task 2
Calculate the standard deviation of `dns_query_query_time_ms` across all devices within the site `lessines` and the sensor_name `one.one.one.one`. 
<details>
  <summary>Reveal Answer</summary>
  
```
stddev(dns_query_query_time_ms{site="lessines", sensor="one.one.one.one"})
```
</details>




stddev(dns_query_query_time_ms{site="lessines", sensor="one.one.one.one"})