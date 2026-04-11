import argparse
import os
import joblib
import pandas as pd
import numpy as np
import mlflow

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()

    df = pd.read_csv("AmesHousing.csv")
    df = df.drop_duplicates()
    df = df.dropna(subset=["SalePrice"])

    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())

    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    df["Age"] = df["Yr Sold"] - df["Year Built"]
    df = pd.get_dummies(df, drop_first=True)

    base_features = ["Gr Liv Area", "Garage Area", "Total Bsmt SF", "Age", "Overall Qual"]
    feature_columns = []
    for col in df.columns:
        normalized = col.replace("_", " ")
        if normalized in base_features:
            feature_columns.append(col)

    X = df[feature_columns]
    y = df["SalePrice"]

    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    train_preds = model.predict(X_train)
    val_preds = model.predict(X_val)
    test_preds = model.predict(X_test)

    with mlflow.start_run():
        mlflow.log_metric("train_rmse", mean_squared_error(y_train, train_preds) ** 0.5)
        mlflow.log_metric("train_mae", mean_absolute_error(y_train, train_preds))
        mlflow.log_metric("train_r2", r2_score(y_train, train_preds))

        mlflow.log_metric("val_rmse", mean_squared_error(y_val, val_preds) ** 0.5)
        mlflow.log_metric("val_mae", mean_absolute_error(y_val, val_preds))
        mlflow.log_metric("val_r2", r2_score(y_val, val_preds))

        mlflow.log_metric("test_rmse", mean_squared_error(y_test, test_preds) ** 0.5)
        mlflow.log_metric("test_mae", mean_absolute_error(y_test, test_preds))
        mlflow.log_metric("test_r2", r2_score(y_test, test_preds))

        os.makedirs(args.output, exist_ok=True)
        model_path = os.path.join(args.output, "model.pkl")
        joblib.dump({"model": model, "feature_columns": feature_columns}, model_path)
        mlflow.log_artifact(model_path)

if __name__ == "__main__":
    main()