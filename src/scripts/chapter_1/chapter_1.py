from pyspark.sql import SparkSession

# 1. Initialize
spark = SparkSession.builder \
    .appName("VSCodeSpark") \
    .master("local[*]") \
    .getOrCreate()

# 2. Define the logic (Transformation - nothing happens yet)
log_df = spark.read.text("data/raw/chapter_2/mnm_dataset.csv").repartition(8)

# 3. Check partitions (Returns plan info)
print(f"Plan says we have {log_df.rdd.getNumPartitions()} partitions.")

# 4. TRIGGER THE WORK (Action - this will finally run the code)
print("Starting the actual data processing...")
print(f"Total rows in file: {log_df.count()}") 

# 5. See the data
log_df.show(5)

# And this code will create a DataFrame of 10,000 integers distributed over eight partitions in memory:
df = spark.range(0, 10000, 1, 8)
print(df.rdd.getNumPartitions())