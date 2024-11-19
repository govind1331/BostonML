@echo off
REM run_tuning_job.bat
REM Run the hyperparameter tuning job on Vertex AI

REM Load environment variables
for /f "tokens=1,* delims==" %%a in (.env) do set %%a=%%b

REM Create service account
set SA_NAME=vertex-ai-tuning
echo Setting up service account...
gcloud iam service-accounts create %SA_NAME% --display-name="Vertex AI Tuning Service Account"

REM Grant necessary permissions
echo Granting IAM permissions...
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SA_NAME%@%PROJECT_ID%.iam.gserviceaccount.com" ^
    --role="roles/storage.objectViewer"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the tuning job
echo Starting hyperparameter tuning job...
python job_config.py ^
    --project-id=%PROJECT_ID% ^
    --bucket-name=%BUCKET_NAME% ^
    --region=%REGION%

echo Tuning job submitted successfully!
pause