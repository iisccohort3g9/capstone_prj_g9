from prometheus_client import start_http_server, Gauge
from clearml import Task
import time

# Define Prometheus metrics
metric_1 = Gauge('clearml_metric_pdf_text_extraction_time', 'PDF Text Extraction Metric-ClearML')
metric_2 = Gauge('clearml_summary_extraction_time', 'Resume Summary Extraction Metric-ClearML')
metric_3 = Gauge('clearml_jd_similarity_extraction_time', 'Resume Similarity Extraction Metric-ClearML')
metric_4 = Gauge('clearml_jd_summary_extraction_time', 'Candidate Resume Summary JD Eval Metric-ClearML')

def collect_clearml_metrics():
    # Fetch a specific ClearML Task or project metrics
    task = Task.get_task(task_id='463c0fafd1734be68f927a095ef4a74c')  # Replace with your Task ID
    metrics = task.get_last_scalar_metrics()

    # Update Prometheus gauges
    pdf_processing_time = round(float(metrics.get('PDF Processing Time', 0)), 3)
    summary_extraction_time = round(float(metrics.get('Summary Processing Time', 0)), 3)
    similarity_extraction_time = round(float(metrics.get('JD - Resume Comparison Time', 0)), 3)
    resume_jd_eval_time = round(float(metrics.get('Candidate Eval Job Time', 0)), 3)

    metric_1.set(pdf_processing_time)  # Replace 'metric_name' with your metric key
    metric_2.set(summary_extraction_time)
    metric_3.set(similarity_extraction_time)
    metric_4.set(resume_jd_eval_time)

if __name__ == "__main__":
    # Start the Prometheus metrics server on port 9091
    start_http_server(9091)
    
    while True:
        collect_clearml_metrics()
        time.sleep(10)  # Scrape interval in seconds
