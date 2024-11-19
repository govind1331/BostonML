@echo off
REM cleanup.bat
REM Clean up resources when they're no longer needed

REM Load environment variables
for /f "tokens=1,* delims==" %%a in (.env) do set %%a=%%b

REM Confirm cleanup
set /p CONFIRM="This will delete the container image and optionally the GCS bucket. Proceed? (y/n): "

if /i "%CONFIRM%"=="y" (
    REM Delete container image
    echo Deleting container image...
    gcloud container images delete gcr.io/%PROJECT_ID%/xgboost-training:latest --quiet

    REM Ask about bucket deletion
    set /p DELETE_BUCKET="Do you want to delete the GCS bucket as well? (y/n): "
    
    if /i "%DELETE_BUCKET%"=="y" (
        echo Deleting GCS bucket...
        gsutil rm -r gs://%BUCKET_NAME%
    )

    echo Cleanup complete!
) else (
    echo Cleanup cancelled.
)
pause