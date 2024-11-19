# job_config.py
from google.cloud import aiplatform
from google.cloud.aiplatform import hyperparameter_tuning as hpt

def create_job_config(project_id, bucket_name):
    # Using a smaller instance type to manage costs
    worker_pool_specs = [
        {
            "machine_spec": {
                "machine_type": "n1-standard-2",  # Smaller instance
                "accelerator_type": "NVIDIA_TESLA_T4",
                "accelerator_count": 1,
            },
            "replica_count": 1,
            "container_spec": {
                "image_uri": f"gcr.io/{project_id}/xgboost-training:latest",
                "args": [
                    f"--bucket-name={bucket_name}"
                ],
            },
        }
    ]

    # Define a smaller parameter search space
    parameters = [
        hpt.IntegerParameterSpec(
            parameter_id="n_estimators",
            min_value=50,    # Reduced range
            max_value=200,   # Reduced range
            scale="linear"
        ),
        hpt.IntegerParameterSpec(
            parameter_id="max_depth",
            min_value=3,
            max_value=6,
            scale="linear"
        ),
        hpt.DoubleParameterSpec(
            parameter_id="learning_rate",
            min_value=0.01,
            max_value=0.1,
            scale="log"
        ),
        hpt.DoubleParameterSpec(
            parameter_id="subsample",
            min_value=0.7,
            max_value=1.0,
            scale="linear"
        ),
    ]

    metric_spec = hpt.MetricSpec(
        metric_id="validation_mse",
        goal=hpt.MetricSpec.GoalType.MINIMIZE,
    )

    # Create the hyperparameter tuning job with fewer trials
    job = aiplatform.HyperparameterTuningJob(
        display_name="xgboost_tuning_job",
        worker_pool_specs=worker_pool_specs,
        parameter_spec=parameters,
        metric_spec=metric_spec,
        max_trial_count=10,  # Reduced number of trials
        parallel_trial_count=3,  # Reduced parallel trials
        optimization_algorithm="GAUSSIAN_PROCESS_BANDIT",
    )
    
    return job

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id', required=True, help='GCP Project ID')
    parser.add_argument('--bucket-name', required=True, help='GCS bucket for artifacts')
    parser.add_argument('--region', default='us-central1', help='GCP region')
    args = parser.parse_args()

    # Initialize Vertex AI
    aiplatform.init(
        project=args.project_id,
        location=args.region
    )
    
    # Create and run the job
    job = create_job_config(args.project_id, args.bucket_name)
    job.run()
    
    print("Job submitted successfully. Monitor progress in the Vertex AI console.")