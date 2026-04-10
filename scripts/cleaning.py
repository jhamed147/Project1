from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

raw_path = "abfss://raw@jana60305219.dfs.core.windows.net/AmesHousing.csv"
df = spark.read.csv(raw_path, header=True, inferSchema=True)

processed_path = "abfss://processed@jana60305219.dfs.core.windows.net/AmesHousing_cleaned"
df.write.mode("overwrite").parquet(processed_path)

