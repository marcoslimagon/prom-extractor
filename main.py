"""
Author: Marcos Lima assisted by ChatGPT 3.5
"""

import os
import requests
import yaml
import datetime
import argparse

def fetch_prometheus_metrics(endpoint, start, end, evaluation_timeout, step, metrics, output_folder):
    """
    Fetches Prometheus metrics for a given list of metric names from the specified endpoint
    within the specified time range, with the specified step interval, and with the specified evaluation timeout.
    Saves each metric in a separate file in the specified output folder.

    Args:
    - endpoint (str): The URL of the Prometheus endpoint.
    - start (int): The start time of the time range for the query as a Unix timestamp.
    - end (int): The end time of the time range for the query as a Unix timestamp.
    - evaluation_timeout (str): The evaluation timeout for each query.
    - step (str): The step interval for data points in the response.
    - metrics (list): A list of dictionaries containing 'name' and 'query' attributes for each metric.
    - output_folder (str): The folder path where the metrics will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for metric in metrics:
        name = metric["name"]
        query = metric["query"]
        params = {'query': query, 'start': start, 'end': end, 'step': step, 'timeout': evaluation_timeout}
        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            filename = os.path.join(output_folder, f"{name}.json")
            with open(filename, "w") as f:
                f.write(str(data))
            print(f"Metrics for '{name}' saved to '{filename}'")
        else:
            print(f"Failed to fetch metrics for '{name}'. Status code: {response.status_code}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch Prometheus metrics")
    parser.add_argument("--days", type=int, default=7, help="Number of days for the time range")
    parser.add_argument("--step", type=str, default="5m", help="Step interval for data points in the response")
    args = parser.parse_args()

    # Calculate start and end times as Unix timestamps
    end_time = datetime.datetime.now()
    end_unix_timestamp = int(end_time.timestamp())
    start_time = end_time - datetime.timedelta(days=args.days)
    start_unix_timestamp = int(start_time.timestamp())

    # Load metrics from YAML file
    with open("metrics.yaml", "r") as yaml_file:
        metrics_config = yaml.safe_load(yaml_file)

    # Extract configuration parameters
    prometheus_endpoint = metrics_config.get("prometheus_endpoint")
    evaluation_timeout = metrics_config.get("evaluation_timeout")
    metric_configs = metrics_config.get("metrics")
    output_folder = metrics_config.get("output_folder")
    
    fetch_prometheus_metrics(prometheus_endpoint, start_unix_timestamp, end_unix_timestamp, evaluation_timeout, args.step, metric_configs, output_folder)

if __name__ == "__main__":
    main()
