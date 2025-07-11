import sys

from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # python mnmcount.py 2> error.log
        print("Usage: mnmcount.py <file>", file=sys.stderr)
        sys.exit(-1)


    # Build a SparkSession using the SparkSession APIs.
    # If one does not exist, then create an instance.
    # There can only be one SparkSession per JVM
    spark = (SparkSession.builder.appName("PythonMnMCount").getOrCreate())

    # Get the M&M data set filename from the command-line arguments
    mnm_file = sys.argv[1]

    # Read the file into a Spark DataFrame using the CSV
    # format by inferring the schema and specifying that the
    # file contains a header, which provides column names for comma-
    # separated fields.
    mnm_df = (spark.read.format("csv")).option("header", "true").option("inferSchema", "true").load(mnm_file)

    # We use the DataFrame high-level APIs. Note
    # that we don't use RDDs at all. Because some of Spark's
    # functions return the same object, we can chain function calls.
    # 1. Select from the DataFrame the fields "State", "Color", and "Count"
    # 2. Since we want to group each state and its M&M color count,
    # we use groupBy()
    # 3. Aggregate counts of all colors and groupBy() State and Color
    # 4 orderBy() in descending order

    count_mnm_df = (mnm_df.select("State", "Color", "Count").groupBy("State", "Color").sum("Count").orderBy("sum(Count)", ascending=False))

    # Show the resulting aggregations for all the states and colors;
    # a total count of each color per state.
    # Note show() is an action, which will trigger the above query to be executed.
    count_mnm_df.show(n=60, truncate=False)
    print(f"Total Rows={count_mnm_df.count()}")

    # While the above code aggregated and counted for all
    # the states, what if we just want to see the data for 
    # a single state, e.g., CA?
    # 1. Select from all rows in the DataFrame
    # 2. Filter only CA state
    # 3. groupBy() State and Color as we did above
    # 4. Aggregate the counts for each color
    # 5. orderBy() in descending order
    # Find the aggregate count for California by filtering

    ca_count_mnm_df = (mnm_df.select("State", "Color", "Count").where(mnm_df.State=="CA").groupBy("State", "Color").sum("Count").orderBy("sum(Count)", ascending=False))

    # Show the resulting aggregation for California.
    # As above, show() is an action that will trigger the execution of the
    # entire computation

    ca_count_mnm_df.show(n=10, truncate=False)

    #Stop the SparkSession
    spark.stop()













