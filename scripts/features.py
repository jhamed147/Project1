from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler

spark = SparkSession.builder.getOrCreate()

processed_path = "abfss://processed@jana60305219.dfs.core.windows.net/AmesHousing_cleaned"
df = spark.read.parquet(processed_path)

assembler = VectorAssembler(
    inputCols=["Gr_Liv_Area", "Garage_Area", "Total_Bsmt_SF", "Year_Built"],
    outputCol="numerical_features"
)
df_num = assembler.transform(df)

scaler = StandardScaler(inputCol="numerical_features", outputCol="numerical_scaled")
df_scaled = scaler.fit(df_num).transform(df_num)

features_path = "abfss://features@jana60305219.dfs.core.windows.net/AmesHousing_features"
df_scaled.write.mode("overwrite").parquet(features_path)
