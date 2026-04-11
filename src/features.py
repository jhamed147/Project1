from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StandardScaler

spark = SparkSession.builder.getOrCreate()

processed_path = "abfss://processed@jana60305219.dfs.core.windows.net/AmesHousing_processed"
df = spark.read.parquet(processed_path)

df = df.withColumn("Age", col("Yr_Sold") - col("Year_Built"))

feature_cols = ["Gr_Liv_Area", "Garage_Area", "Total_Bsmt_SF", "Age", "Overall_Qual"]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="numerical_features")
df = assembler.transform(df)

scaler = StandardScaler(inputCol="numerical_features", outputCol="features")
df = scaler.fit(df).transform(df)

features_path = "abfss://features@jana60305219.dfs.core.windows.net/AmesHousing_features"
df.write.mode("overwrite").parquet(features_path)
