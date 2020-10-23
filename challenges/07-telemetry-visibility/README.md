# Challenge - Using Telegraf for Telemetry and Visibility

The goal of this exercise is to interact with the different components of a TPG stack (Telegraf, Prometheus, Grafana), from a network monitoring perspective.

## Exercise Overview

This exercise requires you to configure 2 **Telegraf** containers that are going to query **external endpoints**. The first instance will send HTTP probes request to get the status, HTTP status code and general response from the endpoint. The second instance will perform a DNS query to an external DNS server and get its general stats.

- The **HTTP telegraf container** (`http-telegraf-01`) will use the [HTTP Response input plugin](https://docs.influxdata.com/telegraf/v1.15/plugins/#http_response) that will gather metrics from HTTP responses.
- The **DNS telegraf container** (`dns-telegraf-01`) will use the [DNS Query input plugin](https://docs.influxdata.com/telegraf/v1.15/plugins/#dns_query) that will gather DNS query times.

### Prerequisites

- Have installed `docker` and `docker-compose`
- Internet connectivity to reach the endpoints.
- Navigate to `lab/` folder to setup and run the lab.

### Setup

To perform the challenge tasks you build/start the containers.

- To bring up the lab run the command

```shell
docker-compose up -d
```

- To bring down the lab run the command

```shell
docker-compose down
```

You need to also configure the **Grafana** instance to see the data stored in Prometheus:

- On your browser navigate to http://localhost:3000
  - Username: `admin`
  - Password: `admin`

- You are good to go!

### Task 1 - Probes Configuration

#### HTTP Probe container

Create input telegraf configuration for `http-telegraf-01`:

- As stated above you need to configure it with the `http_response` input plugin.
- Requirements for the configuration:
  - **URL** is https://www.cloudflarestatus.com/ (Be sure to set it under the `urls` field)
  - Set the response timeout to 5 seconds.
  - Set the HTTP request method to **GET**.
  - Finally make the **response match this substring** to validate its returned data: `All Systems Operational`

#### DNS Query container

Create input telegraf configuration for `dns-telegraf-01`:

- As stated above you need to configure it with the `dns_query` input plugin.
- Requirements for the configuration:
  - Set the DNS server to query: `1.1.1.1`
  - Set queries for the domains: `github.com, gitlab.com, networktocode.com`

You should save a snippet of the metrics gathered on the solution to be submitted.

- **HINT**: The metrics being collected should be visible under http://localhost:9012/metrics and http://localhost:9013/metrics.
- **HINT**: You can use Docker logs (i.e. docker logs -f `http-telegraf-01`) to verify the status of the telegraf instances and spot any errors on the configurations.

### Task 2 - Data manipulation and Visualization

Go to Grafana http://localhost:3000

- Go to **Explore** and validate that you are receiving `http_response_response_time` and the `dns_query_query_time_ms` metrics. You should save some screenshot snippets to be sent on the final report.

- Under a new **Dashboard** you will create the following panels:
  - A time series visualization of the `http_response_response_time` metric
    - Set the Axes Left Y to show the values as `seconds (s)`
    - Format the legend of the time series so it shows the **`server`** and the **`status_code`** of the query.
  - A time series of the `dns_query_query_time_ms`
    - Axes similar setup as the `http_response`
    - Filter based on `server` value: `1.1.1.1`
    - Legend formatted to show the **`domain`** queried and **`result`** in a table format.

## Useful Links

- [Telegraf input plugins](https://docs.influxdata.com/telegraf/v1.15/plugins/)
  - [HTTP Response input plugin](https://docs.influxdata.com/telegraf/v1.15/plugins/#http_response)
  - [DNS Query input plugin](https://docs.influxdata.com/telegraf/v1.15/plugins/#dns_query)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [Grafana Panels](https://grafana.com/docs/grafana/latest/panels/panels-overview/)
