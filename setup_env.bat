@echo off
REM setup_env.bat
REM Set up the environment and enable required APIs

set /p PROJECT_ID="Please enter your Google Cloud Project ID: "
set /p BUCKET_NAME="Please enter your desired GCS bucket name: "
set /p REGION="Please enter your desired region (default: us-central1): "

if "%REGION%"=="" set REGION=australia-east-a

REM Store configuration
echo PROJECT_ID=%PROJECT_ID%> .env
echo BUCKET_NAME=%BUCKET_NAME%>> .env
echo REGION=%REGION%>> .env

REM Initialize gcloud
echo Initializing Google Cloud...
gcloud init --project=%PROJECT_ID%

REM Enable required APIs
echo Enabling required APIs...
gcloud services enable ^
    compute.googleapis.com ^
    containerregistry.googleapis.com ^
    aiplatform.googleapis.com ^
    cloudbuild.googleapis.com ^
    storage-component.googleapis.com

REM Create GCS bucket
echo Creating GCS bucket...
@REM gsutil mb -l %REGION% gs://%BUCKET_NAME%
gcloud storage buckets create gs://%REGION%cket --location=%BUCKET_NAME%

REM Set up Python environment
echo Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo Environment setup complete!
pause