import time
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("VSCodeSpark") \
    .master("local[*]") \
    .getOrCreate()

strings = spark.read.text("README.md")
filtered = strings.filter(strings.value.contains("Spark"))
filtered.count()

print("Spark is running! Open your browser and go to http://localhost:4040")

# Tell the script to sleep for an hour so the UI stays alive
time.sleep(3600)