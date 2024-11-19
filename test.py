import numpy as np
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Load the Boston Housing dataset
boston = load_boston()
X, y = boston.data, boston.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create XGBoost regressor
xgb_reg = xgb.XGBRegressor(
    objective='reg:squarederror',
    random_state=42
)

# Define hyperparameter grid with selected parameters
param_grid = {
    'n_estimators': [100, 200, 300, 400],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.7, 0.8, 0.9, 1.0]
}

# Perform Grid Search with cross-validation
grid_search = GridSearchCV(
    estimator=xgb_reg,
    param_grid=param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    verbose=1,
    n_jobs=-1
)

# Fit the model
grid_search.fit(X_train, y_train)

# Get best parameters and score
print("\nBest parameters found:")
for param, value in grid_search.best_params_.items():
    print(f"{param}: {value}")
print("\nBest cross-validation MSE: {:.4f}".format(-grid_search.best_score_))
print("Best cross-validation RMSE: {:.4f}".format(np.sqrt(-grid_search.best_score_)))

# Train model with best parameters
best_model = grid_search.best_estimator_

# Make predictions
y_pred = best_model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nTest set performance:")
print("MSE: {:.4f}".format(mse))
print("RMSE: {:.4f}".format(rmse))
print("R2 Score: {:.4f}".format(r2))

# Create learning curves for the best model
cv_results_df = pd.DataFrame(grid_search.cv_results_)

# Print top 5 best performing parameter combinations
print("\nTop 5 best performing parameter combinations:")
results_df = pd.DataFrame(grid_search.cv_results_)[
    ['params', 'mean_test_score', 'std_test_score']
].sort_values('mean_test_score', ascending=False).head()

results_df['mean_test_score'] = -results_df['mean_test_score']  # Convert back to MSE
results_df['std_test_score'] = results_df['std_test_score']
print(results_df)