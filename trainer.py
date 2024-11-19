
 # trainer.py
import os
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import hypertune
import argparse
from google.cloud import storage
import argparse
import pandas as pd

def upload_model_artifacts(bucket_name, model_path, metrics):
    """Upload model and metrics to GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Upload model file
    model_blob = bucket.blob(f'models/{os.path.basename(model_path)}')
    model_blob.upload_from_filename(model_path)
    
    # Upload metrics
    metrics_blob = bucket.blob(f'metrics/{os.path.basename(model_path)}_metrics.txt')
    metrics_blob.upload_from_string(str(metrics))

def train_evaluate(args):
    # Load dataset
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
    data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    target = raw_df.values[1::2, 2]
    X, y = data, target
    
    # Split into train, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Create and train model with hyperparameters
    model = xgb.XGBRegressor(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        subsample=args.subsample,
        objective='reg:squarederror',
        random_state=42
    )

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate on validation set
    val_pred = model.predict(X_val)
    val_mse = mean_squared_error(y_val, val_pred)
    val_r2 = r2_score(y_val, val_pred)

    # Evaluate on test set
    test_pred = model.predict(X_test)
    test_mse = mean_squared_error(y_test, test_pred)
    test_r2 = r2_score(y_test, test_pred)

    # Create metrics dictionary
    metrics = {
        'validation_mse': val_mse,
        'validation_r2': val_r2,
        'test_mse': test_mse,
        'test_r2': test_r2,
        'hyperparameters': {
            'n_estimators': args.n_estimators,
            'max_depth': args.max_depth,
            'learning_rate': args.learning_rate,
            'subsample': args.subsample
        }
    }

    # Report metric to Vertex AI
    hpt = hypertune.HyperTune()
    hpt.report_hyperparameter_tuning_metric(
        hyperparameter_metric_tag='validation_mse',
        metric_value=val_mse
    )

    # Save model locally
    model_path = os.path.join(args.model_dir, 'model.bst')
    model.save_model(model_path)
    
    # Upload artifacts to GCS
    upload_model_artifacts(args.bucket_name, model_path, metrics)
    
    return val_mse

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--n_estimators',
        type=int,
        default=100
    )
    parser.add_argument(
        '--max_depth',
        type=int,
        default=3
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.1
    )
    parser.add_argument(
        '--subsample',
        type=float,
        default=1.0
    )
    parser.add_argument(
        '--model-dir',
        type=str,
        default=os.getenv('AIP_MODEL_DIR', 'models')
    )
    parser.add_argument(
        '--bucket-name',
        type=str,
        required=True,
        help='GCS bucket for storing artifacts'
    )
    
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    train_evaluate(args)