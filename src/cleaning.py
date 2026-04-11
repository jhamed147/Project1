from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean

spark = SparkSession.builder.getOrCreate()

raw_path = "abfss://raw@jana60305219.dfs.core.windows.net/AmesHousing.csv"
df = spark.read.csv(raw_path, header=True, inferSchema=True)

df = df.dropDuplicates()

df = df.dropna(subset=["SalePrice"])

numeric_cols = [field.name for field in df.schema.fields if str(field.dataType) in ["IntegerType", "DoubleType"]]

for c in numeric_cols:
    avg = df.select(mean(col(c))).collect()[0][0]
    if avg is not None:
        df = df.fillna({c: avg})

string_cols = [field.name for field in df.schema.fields if str(field.dataType) == "StringType"]

for c in string_cols:
    df = df.fillna({c: "Unknown"})

processed_path = "abfss://processed@jana60305219.dfs.core.windows.net/AmesHousing_processed"
df.write.mode("overwrite").parquet(processed_path)
