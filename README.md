# Ames Housing Price Prediction – Phase 1

## Project Overview

This project builds a reproducible data pipeline on Azure for the Ames Housing dataset to prepare it for machine learning. The overall objective is to support house price prediction using engineered features and regression models.

The pipeline follows this flow:

Raw Data → ETL → Processed Data → EDA → Feature Engineering → Feature Dataset

## 1. Data Ingestion

The source dataset is the Ames Housing Dataset from Kaggle, stored as a CSV file. The data was uploaded to Azure Data Lake Storage Gen2 in the `raw` container. The ingestion mode is batch because the dataset is static and not streamed. The raw CSV is preserved in its original format to support reproducibility and traceability.

## 2. ETL Process

The ETL stage was implemented in Databricks using PySpark.

The main cleaning and transformation steps include:

* reading the raw CSV from the `raw` container
* removing duplicate rows
* dropping rows with missing target values in `SalePrice`
* imputing missing numerical values using the column mean
* filling missing categorical values with `"Unknown"`
* preserving schema consistency during transformation
* writing the cleaned dataset in Parquet format to the `processed` container

Validation checks were also performed after cleaning:

* null-value inspection across all columns
* total row count verification
* duplicate-check verification using unique row counts

This ensures that the processed dataset is clean, consistent, and ready for downstream analysis.

## 3. Cataloging and Governance

The datasets were registered in Databricks Hive Metastore under `hive_metastore.ames_schema`.

Registered tables include:

* `ames_raw`
* `ames_processed`
* `ames_features`

The schema, storage locations, and pipeline stages were documented to provide basic governance and lineage. Unity Catalog was not enabled in the workspace, so Hive Metastore was used as the available metadata solution.

## 4. Exploratory Data Analysis

A concise exploratory data analysis was carried out to assess data readiness for modeling.

Main findings:

* `SalePrice` is right-skewed
* strong positive relationships were observed with `Gr_Liv_Area` and `Overall_Qual`
* moderate relationships were observed with `Garage_Area` and `Total_Bsmt_SF`
* outliers were visible in some large houses with unusual prices
* neighborhood appears to have a strong effect on pricing

Potential risks identified:

* skewness in the target variable
* possible multicollinearity among size-related variables

These findings helped guide feature selection and preparation for modeling.

## 5. Feature Engineering and Selection

Feature engineering was performed on the processed dataset to create a machine-learning-ready feature set.

Engineered feature:

* `Age = Yr_Sold - Year_Built`

Selected core features:

* `Gr_Liv_Area`
* `Garage_Area`
* `Total_Bsmt_SF`
* `Age`
* `Overall_Qual`

The numerical features were assembled into a feature vector and scaled using `StandardScaler`. The resulting engineered dataset was saved in Parquet format to the `features` container and registered as `hive_metastore.ames_schema.ames_features`.

## 6. Reproducibility and Version Control

The project was implemented in Databricks and documented in GitHub. The repository includes:

* the notebook used for implementation
* pipeline definition files
* modular Python scripts for cleaning and feature engineering
* project documentation in `README.md`

This structure supports reproducibility, code organization, and version control for the data pipeline.

## 7. Storage Layout

The Azure Data Lake Storage layout is organized into separate zones:

* `raw` for original source data
* `processed` for cleaned ETL outputs
* `features` for engineered machine learning features

This separation improves traceability and aligns with good data engineering practice.

## Conclusion

Phase 1 establishes the data foundation for the AI system. The dataset was ingested, cleaned, validated, analyzed, cataloged, and transformed into a feature-ready format for machine learning. This provides a reproducible base for Phase 2, which focuses on model development, validation, versioning, and deployment.
