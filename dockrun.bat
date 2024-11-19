@echo off
REM docker_build_test.bat
REM Build and test Docker container locally

REM Load environment variables
for /f "tokens=1,* delims==" %%a in (.env) do set %%a=%%b

REM Build the Docker image
echo Building Docker image...
docker build -t xgboost-training:local .

REM Test the container locally
echo Testing container...
docker run --rm xgboost-training:local --help

REM Build for Google Container Registry
echo Building for GCR...
docker build -t gcr.io/%PROJECT_ID%/xgboost-training:latest .

echo Docker build and test complete!
pause