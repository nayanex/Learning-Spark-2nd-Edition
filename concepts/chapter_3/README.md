# Apache Spark’s Structured APIs

* What are Spark's high-level APIs? (Dataframes and Datasets)

DataFrames are a sucessor to SchemaRDDs.

 
Spark SQL introduced high-level expressive operational functions, mimicking SQL-like syntax, and DataFrames, which laid the foundation for more structure in subsequent releases, paved the path to performant operations in Spark’s computational queries.

Before we talk about the newer Structured APIs, let’s get a brief glimpse of what it’s like to not have structure in Spark by taking a peek at the simple RDD programming API model.

## Spark: What’s Underneath an RDD (Resilient Distributed Datasets)?

While RDDs are the "soul" of Spark, modern developers usually use DataFrames. Think of a DataFrame as an RDD that has been given a Schema (like an Excel table). It’s the same abstraction, just with more "Concrete" structure to make it even faster!

There are three vital characteristics associated with an RDD:

* Dependencies

* Partitions (with some locality information)

* Compute function: Partition => `Iterator[T]`

The compute function (or computation) is opaque to Spark. That is, Spark does not know what you are doing in the compute function. Whether you are performing a join, filter, select, or aggregation, Spark only sees it as a lambda expression. Another problem is that the `Iterator[T]` data type is also opaque for Python RDDs; Spark only knows that it’s a generic object in Python.

Furthermore, because it’s unable to inspect the computation or expression in the function, Spark has no way to optimize the expression—it has no comprehension of its intention. And finally, Spark has no knowledge of the specific data type in `T`. To Spark it’s an opaque object; it has no idea if you are accessing a column of a certain type within an object. Therefore, all Spark can do is serialize the opaque object as a series of bytes, without using any data compression techniques.

This opacity clearly hampers Spark’s ability to rearrange your computation into an efficient query plan. So what’s the solution?

Instead of thinking of an RDD as a **bucket of data**, think of it as a **Blueprint for a Building**. 

* The **Blueprint** (RDD) knows how many **Rooms** (Partitions) there are. 
* It has the **Construction Plan** (Compute Function) for each room. 
* It knows which **Previous Blueprints** (Dependencies) it was based on. 
* If a storm knocks down one room (Node Failure), you don't need a backup of the whole building. You just look at the **Blueprint** and the **DNA** to rebuild that specific room exactly where it was supposed to be (**Preferred Locations**).

---

### Strategy for Mastery

To train your brain to "see" this anatomy while coding, ask yourself these three questions every time you write a Spark transformation:
1. **"Is this changing the partitions?"** (e.g., `repartition` vs `map`)
2. **"Is this creating a Wide or Narrow dependency?"** (e.g., `join` vs `filter`)
3. **"Where is the data likely sitting?"** (e.g., is it coming from S3 or local HDFS?)

## Structuring Spark

Let's first try to understand the power of DSLs.

To make **DSL (Domain-Specific Language)** stick in your brain, we need to stop thinking of it as "code" and start thinking of it as a **"Specialized Tool for a Specific Context."**

---

### The First Principle: Efficiency vs. Expressiveness
A language is just a way to map human intent to machine action.
* **General Purpose Language (GPL):** Languages like Python, Java, or C++. They are like a **Dictionary**. You can use them to write a poem, a scientific paper, or a grocery list. They can do *anything*, but they are often verbose because you have to explain every detail.
* **Domain-Specific Language (DSL):** A language like SQL, HTML, or CSS. It is like a **Restaurant Menu**. You can't use a pizza menu to order a car or write a poem. But inside the "Pizza Domain," it is incredibly efficient. You just say "Pepperoni," and the kitchen knows exactly what to do.

---

### Why do we keep using them?
To train your brain to remember the "Why," look at this **Inversion**:
> If we *didn't* have the DSL "HTML," you would have to write thousands of lines of C++ code just to tell the computer how to draw a blue rectangle on a screen. With the DSL, you just write `<div style="color: blue">`. 

**A DSL trades "Breadth" (doing many things) for "Depth" (doing one thing perfectly).**

---

### Exercise: "The Everyday DSL"
Identify the DSLs in your non-digital life to cement the abstraction:
1.  **Sheet Music:** A DSL for the domain of "Music Performance." (Try explaining a symphony using only the English dictionary—it would be 10,000 pages).
2.  **Chess Notation:** `Nf3` (Knight to f3). A DSL for the domain of "Chess Moves."
3.  **A Recipe:** "Saute until translucent." "Saute" is a domain-specific term for cooking.

---

Do you see how the **Spark SQL/DataFrame API** is a DSL built on top of the RDD abstraction to make it easier to use?

Spark 2.x introduced a few key schemes for structuring Spark. One is to express computations by using common patterns found in data analysis. These patterns are expressed as high-level operations such as filtering, selecting, counting, aggregating, averaging, and grouping. This provides added clarity and simplicity.

This specificity is further narrowed through the use of a set of common operators in a DSL. Through a set of operations in DSL, available as APIs in Spark’s supported languages (Java, Python, Spark, R, and SQL), these operators let you tell Spark what you wish to compute with your data, and as a result, it can construct an efficient query plan for execution.

And the final scheme of order and structure is to allow you to arrange your data in a tabular format, like a SQL table or spreadsheet, with supported structured data types.

But what’s all this structure good for?

## Key Merits and Benefits

Structure yields a number of benefits, including better performance and space efficiency across Spark components.

`expressivity, simplicity, composability, and uniformity`

Let’s demonstrate **expressivity** and **composability** first. In the following example, we want to aggregate all the ages for each name, group by name, and then average the ages—a common pattern in data analysis and discovery. If we were to use the low-level RDD API for this, the code would look as follows:

```python
# In Python
# Create an RDD of tuples (name, age)
dataRDD = sc.parallelize([("Brooke", 20), ("Denny", 31), ("Jules", 30), 
  ("TD", 35), ("Brooke", 25)])
# Use map and reduceByKey transformations with their lambda 
# expressions to aggregate and then compute average

agesRDD = (dataRDD
  .map(lambda x: (x[0], (x[1], 1)))
  .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
  .map(lambda x: (x[0], x[1][0]/x[1][1])))
```

This code, which tells Spark **how to** aggregate keys and compute averages with a string of lambda functions, is cryptic and hard to read. In other words, the code is instructing Spark how to compute the query. It’s completely opaque to Spark, because it doesn’t communicate the intention. Furthermore, the equivalent RDD code in Scala would look very different from the Python code shown here.

By contrast, what if we were to express the same query with high-level DSL operators and the DataFrame API, thereby instructing Spark **what to do**? Have a look:

```python
# In Python 
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg
# Create a DataFrame using SparkSession
spark = (SparkSession
  .builder
  .appName("AuthorsAges")
  .getOrCreate())
# Create a DataFrame 
data_df = spark.createDataFrame([("Brooke", 20), ("Denny", 31), ("Jules", 30), 
  ("TD", 35), ("Brooke", 25)], ["name", "age"])
# Group the same names together, aggregate their ages, and compute an average
avg_df = data_df.groupBy("name").agg(avg("age"))
# Show the results of the final execution
avg_df.show()

+------+--------+
|  name|avg(age)|
+------+--------+
|Brooke|    22.5|
| Jules|    30.0|
|    TD|    35.0|
| Denny|    31.0|
+------+--------+
```

This version of the code is far more expressive as well as simpler than the earlier version, because we are using high-level DSL operators and APIs to tell Spark **what to do**. In effect, we have employed these operators to compose our query. And because Spark can inspect or parse this query and understand our intention, it can optimize or arrange the operations for efficient execution. Spark knows exactly what we wish to do: group people by their names, aggregate their ages, and then compute the average age of all people with the same name. We’ve composed an entire computation using high-level operators as a single simple query.

Some would contend that by using only high-level, expressive DSL operators mapped to common or recurring data analysis patterns to introduce order and structure, we are limiting the scope of the developers’ ability to instruct the compiler or control how their queries should be computed. Rest assured that you are not confined to these structured patterns; you can switch back at any time to the unstructured low-level RDD API, although we hardly ever find a need to do so.

As well as being simpler to read, the structure of Spark’s high-level APIs also introduces **uniformity** across its components and languages. For example, the Scala code shown here does the same thing as the previous Python code—and the API looks nearly identical:

```
// In Scala
import org.apache.spark.sql.functions.avg
import org.apache.spark.sql.SparkSession
// Create a DataFrame using SparkSession
val spark = SparkSession
  .builder
  .appName("AuthorsAges")
  .getOrCreate()
// Create a DataFrame of names and ages
val dataDF = spark.createDataFrame(Seq(("Brooke", 20), ("Brooke", 25), 
  ("Denny", 31), ("Jules", 30), ("TD", 35))).toDF("name", "age")
// Group the same names together, aggregate their ages, and compute an average
val avgDF = dataDF.groupBy("name").agg(avg("age"))
// Show the results of the final execution
avgDF.show()

+------+--------+
|  name|avg(age)|
+------+--------+
|Brooke|    22.5|
| Jules|    30.0|
|    TD|    35.0|
| Denny|    31.0|
+------+--------+
```

All of this simplicity and expressivity that we developers cherish is possible because of the Spark SQL engine upon which the high-level Structured APIs are built. It is because of this engine, which underpins all the Spark components, that we get uniform APIs. Whether you express a query against a DataFrame in Structured Streaming or MLlib, you are always transforming and operating on DataFrames as structured data.

## The DataFrame API

Inspired by [Pandas DataFrames](https://oreil.ly/z93hD) in structure, format, and a few specific operations, Spark DataFrames are like distributed in-memory tables with named columns and schemas, where each column has a specific data type: integer, string, array, map, real, date, timestamp, etc. To a human’s eye, a Spark DataFrame is like a table. 


### DataFrame Content Overview

| Id (Int) | First (String) | Last (String) | Url (String) | Published (Date) | Hits (Int) | Campaigns (List[Strings]) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Jules | Damji | https://tinyurl.1 | 1/4/2016 | 4,535 | [twitter, LinkedIn] |
| **2** | Brooke | Wenig | https://tinyurl.2 | 5/5/2018 | 8,908 | [twitter, LinkedIn] |
| **3** | Denny | Lee | https://tinyurl.3 | 6/7/2019 | 7,659 | [web, twitter, FB, LinkedIn] |
| **4** | Tathagata | Das | https://tinyurl.4 | 5/12/2018 | 10,568 | [twitter, FB] |
| **5** | Matei | Zaharia | https://tinyurl.5 | 5/14/2014 | 40,578 | [web, twitter, FB, LinkedIn] |
| **6** | Reynold | Xin | https://tinyurl.6 | 3/2/2015 | 25,568 | [twitter, LinkedIn] |


When data is visualized as a structured table, it’s not only easy to digest but also easy to work with when it comes to common operations you might want to execute on rows and columns. 

DataFrames are immutable and Spark keeps a lineage of all transformations. You can add or change the names and data types of the columns, creating new DataFrames while the previous versions are preserved. A named column in a DataFrame and its associated Spark data type can be declared in the schema.


### Transformations & Immutability (The "Save-As")

Watch what happens when we want to change a column name. We don't modify `df1`; we create `df2`.

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# We define the 'Shape' of the table before we even have the data
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("city", StringType(), True)
])

data = [("Alice", 28, "New York"), ("Bob", 35, "Amsterdam"), ("Charlie", 22, "London")]

# df1 is our 'Original' version
df1 = spark.createDataFrame(data, schema)

df1.show()

# df1 is NOT changed. We derive df2 from it.
df2 = df1.withColumnRenamed("name", "user_name").filter("age > 25")

# df1 still has the 'name' column and all 3 rows.
# df2 has 'user_name' and only 2 rows.
df2.show()
```


### Seeing the Lineage (The "Paper Trail")
The most powerful tool to see the "Anatomy" of what Spark is doing is the `.explain()` method. This shows you the **Logical Plan** (your intent) and the **Physical Plan** (how the RDDs will actually move).

```python
df2.explain(True)
```

**The output will look something like this (Abbreviated):**
1.  **Parsed Logical Plan:** `Filter (age > 25) -> Project [name AS user_name...]`
2.  **Analyzed Logical Plan:** (Verifies the names against the Schema)
3.  **Optimized Logical Plan:** (Spark might reorder steps for speed)
4.  **Physical Plan:** `*(1) Filter (age > 25) -> *(1) Scan ExistingRDD`

## Spark’s Basic Data Types

Matching its supported programming languages, Spark supports basic internal data types. These data types can be declared in your Spark application or defined in your schema.

**Basic** [Python data types](https://oreil.ly/HuREJ) in Spark:


| Data type | Value assigned in Python | API to instantiate |
| :--- | :--- | :--- |
| `ByteType` | `int` | `DataTypes.ByteType` |
| `ShortType` | `int` | `DataTypes.ShortType` |
| `IntegerType` | `int` | `DataTypes.IntegerType` |
| `LongType` | `int` | `DataTypes.LongType` |
| `FloatType` | `float` | `DataTypes.FloatType` |
| `DoubleType` | `float` | `DataTypes.DoubleType` |
| `StringType` | `str` | `DataTypes.StringType` |
| `BooleanType` | `bool` | `DataTypes.BooleanType` |
| `DecimalType` | `decimal.Decimal` | `DecimalType` |

## Spark’s Structured and Complex Data Types

For complex data analytics, you won’t deal only with simple or basic data types. Your data will be complex, often structured or nested, and you’ll need Spark to handle these complex data types. They come in many forms: maps, arrays, structs, dates, timestamps, fields, etc.

The **structured** data types in Python that Spark supports are enumerated in:

| Data type | Value assigned in Python | API to instantiate |
| :--- | :--- | :--- |
| `BinaryType` | `bytearray` | `BinaryType()` |
| `TimestampType` | `datetime.datetime` | `TimestampType()` |
| `DateType` | `datetime.date` | `DateType()` |
| `ArrayType` | `List, tuple, or array` | `ArrayType(dataType, [nullable])` |
| `MapType` | `dict` | `MapType(keyType, valueType, [nullable])` |
| `StructType` | `List or tuple` | `StructType([fields])` |
| `StructField` | A value type corresponding to the type of this field | `StructField(name, dataType, [nullable])` |

## Schemas and Creating DataFrames

A **schema** in Spark defines the column names and associated data types for a DataFrame. Most often, schemas come into play when you are reading structured data from an external data source. Defining a schema up front as opposed to taking a schema-on-read approach offers three benefits:

* You relieve Spark from the onus of inferring data types.

* You prevent Spark from creating a separate job just to read a large portion of your file to ascertain the schema, which for a large data file can be expensive and time-consuming.

* You can detect errors early if data doesn’t match the schema.

So, we encourage you to always define your schema up front whenever you want to read a large file from a data source.

### Two ways to define a schema

Spark allows you to define a schema in two ways. One is to define it programmatically, and the other is to employ a **Data Definition Language (DDL)** string, which is much simpler and easier to read.

To define a schema programmatically for a DataFrame with three named columns, `author`, `title`, and `pages`, you can use the Spark DataFrame API. For example:

```python
# In Python
from pyspark.sql.types import *

schema = StructType([StructField("author", StringType(), False),
  StructField("title", StringType(), False),
  StructField("pages", IntegerType(), False)])
```

Defining the same schema using DDL is much simpler:

```python
# In Python
schema = "author STRING, title STRING, pages INT"
```
