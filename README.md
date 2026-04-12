# Ames Housing Price Prediction – End-to-End MLOps Pipeline

## Project Overview

This project implements a complete end-to-end data and machine learning pipeline for predicting house prices using the Ames Housing dataset.

The project is divided into two phases:

- **Phase 1:** Data engineering pipeline (ingestion, ETL, EDA, feature engineering)
- **Phase 2:** Machine learning and MLOps pipeline (model training, validation, deployment, automation)

The overall workflow is:

Raw Data → ETL → Processed Data → EDA → Feature Engineering → Model Training → Evaluation → Model Registration → Deployment → DevOps Automation

---

## Phase 1 – Data Engineering Pipeline

### 1. Data Ingestion

The Ames Housing dataset was obtained from Kaggle and uploaded as a CSV file to Azure Data Lake Storage Gen2.

- Storage container: `raw`
- Ingestion mode: batch
- The raw dataset is preserved in its original format to ensure reproducibility and traceability.

---

### 2. ETL Process

The ETL pipeline was implemented in Databricks using PySpark.

Main steps:

- reading the raw CSV file from the `raw` container  
- removing duplicate records  
- dropping rows with missing target values (`SalePrice`)  
- imputing missing numerical values using the column mean  
- filling missing categorical values with `"Unknown"`  
- ensuring schema consistency  
- saving the cleaned dataset in Parquet format to the `processed` container  

Validation checks performed:

- null value inspection across all columns  
- row count verification  
- duplicate validation  

---

### 3. Cataloging and Governance

Datasets were registered in Databricks Hive Metastore:

- `hive_metastore.ames_schema.ames_raw`
- `hive_metastore.ames_schema.ames_processed`
- `hive_metastore.ames_schema.ames_features`

This provides:

- basic data lineage  
- metadata tracking  
- structured access to datasets  

---

### 4. Exploratory Data Analysis

EDA was performed to understand relationships between features and the target variable.

Key findings:

- `SalePrice` is right-skewed  
- strong positive correlation with:
  - `Gr_Liv_Area`
  - `Overall_Qual`  
- moderate correlation with:
  - `Garage_Area`
  - `Total_Bsmt_SF`  
- presence of outliers in large properties  
- neighborhood has a strong impact on price  

Risks identified:

- skewed target distribution  
- potential multicollinearity among size-related variables  

---

### 5. Feature Engineering and Selection

Feature engineering was applied to prepare data for modeling.

Engineered feature:

- `Age = Yr_Sold - Year_Built`

Selected features:

- `Gr_Liv_Area`
- `Garage_Area`
- `Total_Bsmt_SF`
- `Age`
- `Overall_Qual`

Features were assembled and scaled, and the final dataset was stored in the `features` container.

---

### 6. Storage Architecture

The data lake was organized into three layers:

- `raw` → original data  
- `processed` → cleaned data  
- `features` → machine learning-ready dataset  

This structure improves traceability and aligns with data engineering best practices.

---

## Phase 2 – Machine Learning and MLOps Pipeline

### 7. Model Development

A regression model was developed to predict house prices.

Selected model:

- Random Forest Regressor  

Reason for selection:

- strong performance on structured data  
- ability to model nonlinear relationships  
- robustness to noise  

---

### 8. Training and Validation

The dataset was split into:

- training set  
- validation set  
- test set  

Training workflow:

- model trained on training data  
- validated using validation set  
- final evaluation performed on test set  

---

### 9. Evaluation Metrics

The model was evaluated using:

- RMSE (Root Mean Squared Error)  
- MAE (Mean Absolute Error)  
- R² Score  

Results:

- the model outperformed the baseline  
- prediction errors were significantly reduced  
- relationships between features and price were captured effectively  

---

### 10. Model Saving and Registration

The trained model was saved as:

- `model.pkl`

The model was registered in Azure ML:

- Model Name: `ames-model`

This enables:

- version control  
- reproducibility  
- centralized model management  

---

### 11. Deployment

The model was deployed using Azure ML Managed Online Endpoint.

Deployment details:

- Endpoint Name: `ames-endpoint-03`  
- Deployment Name: `blue`  
- Compute Type: Standard_DS2_v2  

A scoring script was implemented to:

- load the model at runtime  
- process incoming JSON requests  
- generate predictions  
- return results as JSON  

---

### 12. Endpoint Inference

The endpoint was tested successfully.

Sample input:

```json
{
  "data": [
    {
      "Gr_Liv_Area": 1500,
      "Garage_Area": 400,
      "Total_Bsmt_SF": 800,
      "Age": 20,
      "Overall_Qual": 6
    }
  ]
}
