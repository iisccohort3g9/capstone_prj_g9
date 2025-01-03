from prometheus_client import start_http_server, Gauge
from clearml import Task
import time

# Define Prometheus metrics
metric_1 = Gauge('clearml_metric_example', 'Example metric from ClearML')

def collect_clearml_metrics():
    # Fetch a specific ClearML Task or project metrics
    task = Task.get_task(task_id='05e080a46d254f1f8640e45f19258158')  # Replace with your Task ID
    metrics = task.get_last_scalar_metrics()

    # Update Prometheus gauges
    pdf_processing_time = round(float(metrics.get('PDF Processing Time', 0)), 3)
    metric_1.set(pdf_processing_time)  # Replace 'metric_name' with your metric key

if __name__ == "__main__":
    # Start the Prometheus metrics server on port 9091
    start_http_server(9091)
    
    while True:
        collect_clearml_metrics()
        time.sleep(10)  # Scrape interval in seconds
