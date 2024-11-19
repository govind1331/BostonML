@echo off
REM build_and_push.bat
REM Build and push Docker container to Google Container Registry

REM Load environment variables
for /f "tokens=1,* delims==" %%a in (.env) do set %%a=%%b

REM Configure Docker to use gcloud credentials
echo Configuring Docker authentication...
gcloud auth configure-docker

REM Build the Docker image
echo Building Docker image...
docker build -t gcr.io/%PROJECT_ID%/xgboost-training:latest .

REM Push to Container Registry
echo Pushing image to Container Registry...
docker push gcr.io/%PROJECT_ID%/xgboost-training:latest

echo Container build and push complete!
pause