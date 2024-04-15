# prom-extractor
A simple python-based script that exports a list of queries into txt and zip

## How it works
Given a list of metrics, it will execute the query against `prometheus` server, save in the output folder.

This can be used to export for other sources


## Getting started (from source code)

### (optional) Start prometheus server
We created a basic `docker-compose.yml` file to make easier the development and test.

You can start the `prometheus` and `node-exporter`

```bash
docker-compose up -d
```

### (optional) Create a virtual env
We strongly recommend the usage of a virtual env.


```bash
python3 -m venv .venv
source .venv/bin/activate 
```

### Install Required Dependencies

Install the required dependencies using pip and the requirements.txt file:

```bash
pip install -r requirements.txt 
```

### Prepare YAML Configuration File
Prepare a YAML configuration file named metrics.yaml with the following structure:

```yaml
prometheus_endpoint: "http://localhost:9090/api/v1/query_range"
evaluation_timeout: "10s"  # Example timeout value, adjust as needed
metrics:
  - name: up
    query: "up{}"
  - name: http_requests_total
    query: "sum(rate(prometheus_http_request_duration_seconds_bucket{}[1m]))"
output_folder: "output"
```

Where:

*   `prometheus_endpoint`: The URL of the Prometheus endpoint.
*   `evaluation_timeout`: The evaluation timeout for each query (e.g., "10s").
*   `metrics`: A list of dictionaries containing the metric name and query.
    *  `name`: Name of the query, it will be the name of the output file.
    *  `query`: PromQL query to be executed
*   `output_folder`: The folder path where the metrics will be saved.


### Execute the Script

Execute the script with the desired options:

```bash   
python main.py --days 7 --step 5m
```

Where:

* `--days`: Number of days for the time range (default is 7 days).
* `--step`: Step interval for data points in the response (default is 5 minutes).

This will fetch the Prometheus metrics according to the specified options and save them as separate JSON files in the output folder.


## Getting started (from docker)

In order to make it easier to use, it was generated a Dockerfile.

You can map the metrics

```bash
docker run -it  -v ./metrics.yaml:/app/metrics.yaml -v ./output:/app/output --network=prom-extractor_localprom marcoslimagon/prom-extractor 
```

* `./metrics.yaml`: YAML following the step: Prepare YAML Configuration File
* `--network=prom-extractor_localprom`: (optional) if you are using the `docker-compose.yaml` file of this project you need to connect into the same network. In this case, you also need to update the `prometheus_endpoint` using the internal IP address of the container.
