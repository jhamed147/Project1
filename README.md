# Project1
In this project i will build reproducible data pipeline on Azure to prepare the Amed Housing dataset for machine learning. My goal is to predict house pricing using engineered features and regression.

My pipeline is 
Start with raw data --> start ETL(cleaning, type, imputation) --> Processed Data (Parquet in the processed container) --> EDA (distribution, correlations, and outliers) --> Feature Engineering $ selection --> then finally the Features Dataset (We add the parquet to the features container that we created)

Step 1 we will do Data Ingestion:
Source: Ames Housing dataset (CSV is from Kaggle)
Storage: Uploaded to Azure Data Lake Storage Gen2 in a raw container.
Access: Configured in Databricks using spark.conf.set with account key.
Mode: Batch ingestion (static dataset).
Preservation: Raw CSV stored and versioned.

Step 2 start the ETL process:

Cleaning:
Dropped rows with missing target (SalePrice).
Imputed missing numeric values (mean/median).
Encoded categorical variables (StringIndexer + OneHotEncoder).

Type Fixes:
Converted numeric columns to float.
Standardized categorical columns to string.

Output: Saved as Parquet in processed container.

Step 3 Cataloging & Goverance:

Registered datasets in Hive Metastore:
hive_metastore.ames_schema.ames_raw
hive_metastore.ames_schema.ames_processed

Added schema documentation and column comments.

Lineage documented in README and tracked automatically in Hive Metastore.

Step 4 we start EDA
Distribution: SalePrice is right-skewed.

Correlations:
Strong positive: Gr_Liv_Area, Overall_Qual.
Moderate: Garage_Area, Total_Bsmt_SF.

Outliers: Large houses with unusually low/high prices.

Categorical Influence: Neighborhood strongly affects SalePrice.

Risks:
Skewness may require log-transform.
Multicollinearity between size-related features.

Step 5 Feature Extraction & Selection
Engineered Features:
Age = Yr_Sold - Year_Built
PricePerSqFt = SalePrice / Gr_Liv_Area

Selected Features:
Gr_Liv_Area, Garage_Area, Total_Bsmt_SF, Age, Overall_Qual, Neighborhood.

Scaling:
StandardScaler applied to numerical features.

Output: Saved engineered dataset in features container and registered as:
hive_metastore.ames_schema.ames_features

Step 6 Documentation & Version control
All notebooks synced to GitHub via Databricks Repos.
README.md explains pipeline stages and lineage.
Branching strategy: main, dev, feature/etl, feature/eda.


“Unity Catalog was not enabled in my Databricks workspace, so we registered datasets in the default Hive Metastore (hive_metastore.ames_schema). This still provides lineage and governance, but without Unity Catalog’s advanced features. If Unity Catalog were available, we would have created a dedicated catalog (housing_catalog) for this project.”
