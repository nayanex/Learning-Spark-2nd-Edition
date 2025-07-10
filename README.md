# Learning Spark

## What is Spark?

- big data and analytics unified processing engine
- big data distributed computing
- unified engine designed for large-scale distributed data processing, on premises, in data centers or in the cloud
- provides in-memory storage for intermediate computations, making it much faster than Hadoop MapReduce
- it incorporates libraries with composable APIs for machine learning (MLlib), SQL for interactive queries (Spark SQL), stream processing (Structured Streaming) for interacting with real-time data, and graph processing (GraphX)

## What's Spark's design philosophy?

### Speed

Spark builds its query computations as a directed acyclic graph (DAG); its DAG scheduler and query optimizer construct an efficient computational graph that can usually be decomposed into task that are executed in parallel across workers on the cluster.

It also has its physical execution engine, Tungsten, which uses **whole-stage** code generation to generate compact code for execution.

With the intermediate results retained in memory and its limited disk I/O, this gives a huge performance boost.

### Ease of use

It provides data abstractions like DataFrames and Datasets. By providing a set of **transformations** and **actions** as **operations**, Spark offers a simple programming model that you can use to build data applications in familiar languages.

### Modularity

Spark operations can be applied across many types of workloads and expressed in any of the supported programming languages: Scala, Java, Python, SQL and R. Spark offers unified libraries with well-documented APIs that include core components: Spark SQL, Spark Structured Streaming, Spark MlLib and GraphX, combining all the workloads running under one engine.

### Extensibility

Spark focuses on its fast, parallel computation engine rather than on storage. unlike Apache Hadoop, which included both storage and compute, Spark decouples the two. That means you can use Spark to read data stored in myriad sources - Apache Hadoop, Apache Cassandra, MongoDB, RDBMSs and more - and process it all in memory.

The community of Spark developers maintains a list of third-party spark packages as part of the growing ecosystem. The rich ecosystem of packages include Spark connectors for a variety of external data sources, performance monitors and more.

## What are Apache Spark Components as a Unified stack?

Spark offers 4 distinct components as libraries for diverse workloads: Spark SQL, Spark MLlib, Spark Streaming and Graph X. Each of these components is separate from Spark's core fault-tolerant engine, in that you use your APIs to write your Spark application and Spark converts this into a DAG that is executed by the core engine. The underlying code id decomposed into highly compact bytecode that is executed in the workers's JVMs across the cluster.

![alt text](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0103.png)

## Spark's Distributed Execution

Spark is a distributed data processing engine with its components working collaboratively on a cluster of machines. you need to understand how all the components of Spark's distributed architecture work together and communicate, and what deployment modes are available.

At a high level in the Spark architecture, a Spark application consists of a driver program that is responsible for orchestrating parallel operations on the Spark cluster. The driver accesses the distributed components in the cluster - the Spark executors and cluster manager - through a SparkSession.

![alt text](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0104.png)

### Spark Driver

As the part of the Spark application responsible for instantiating a Spark Session, the Spark driver has multiple roles:

- communicates with the cluster manager
- requests resources (CPU, memory, etc.) from the cluster manager for Spark's executors (JVMs)
- transforms all the Spark operations into DAG computations, schedules them and distributes their execution as tasks across the Spark executors. Once the resources are allocated, it communicates directly with the executors.

### SparkSession

The Spark session is a unified conduit to all Spark operations and data. Through this one conduit, you ca create JVM runtime parameters, define DataFrames and Datasets, read from data sources, access catalog metadata, and issue Spark SQL queries. SparkSession provides a single unified entry point to all of Spark's functionality.


You can create a `SparkSession` per JVM and use it to perform a number of Spark operations

### Cluster Manager

It is responsible for managing and allocating resources for the cluster of nodes on which your Spark applications runs.

### Spark Executor

A Spark executor runs on each worker node in the cluster. The executors communicate with the driver program and are responsible for executing tasks on workers. In most deployments modes, only a single executor runs per node.

## Deployment Modes

Because the cluster manager is agnostic to where it runs (as long as it can manager Spark's executors and fulfill resource requests), Spark can be deployed in some of the most popular environments.

| Mode           | Spark driver                                              | Spark executor                                      | Cluster manager                                                                 |
|----------------|-----------------------------------------------------------|-----------------------------------------------------|----------------------------------------------------------------------------------|
| Local          | Runs on a single JVM, like a laptop or single node        | Runs on the same JVM as the driver                 | Runs on the same host                                                            |
| Standalone     | Can run on any node in the cluster                        | Each node in the cluster will launch its own executor JVM | Can be allocated arbitrarily to any host in the cluster                         |
| YARN (client)  | Runs on a client, not part of the cluster                 | YARN’s NodeManager’s container                      | YARN’s Resource Manager works with YARN’s Application Master to allocate the containers on NodeManagers for executors |
| YARN (cluster) | Runs with the YARN Application Master                     | Same as YARN client mode                            | Same as YARN client mode                                                         |
| Kubernetes     | Runs in a Kubernetes pod                                  | Each worker runs within its own pod                 | Kubernetes Master                                                                |


## Distributed data and partitions

Actual physical data is distributed across storage as partitions residing in either HDFS or cloud storage. While the data is distributed as partitions across the physical cluster, Spark treats each partition as a high-level logical data abstraction-as a Data.


![alt text](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0106.png)

Partitioning allow for efficient parallelism. A distributed scheme of breaking up data into chunks or partitions allows Spark executors to process only data that is close to them, minimizing network bandwidth. That is, each executor's core is assigned its own data partition to work on.

For example, this code snippet will break up the physical data stored across clusters into eight partitions, and each executor will get one or more partitions to read into its memory:

```python
# In Python
log_df = spark.read.text("path_to_large_text_file").repartition(8)
print(log_df.rdd.getNumPartitions())
```

And this code will create a DataFrame of 10,000 integers distributed over eight partitions in memory:

```python
# In Python
df = spark.range(0, 10000, 1, 8)
print(df.rdd.getNumPartitions())
```

## The Developer's Experience

Data engineers use Spark to parallelize computations and it hides all the complexity of distribution and fault tolerance. This leaves them free to focus on using high-level DataFrame-based APIs and domain-specific language (DSL) queries to do ETL, reading and combining data from multiple sources.

## What is the advantage of using Spark?

- Efficient for interactive or iterative computing jobs and a simple framework to learning. It's simple, fast and easy.

- Early papers published on Spark demonstrated that it was 10 to 20 times faster than Hadoop MapReduce for certain jobs, nowadays it's many orders of magnitude.

- highly fault-tolerant, embarrassingly parallel, support in-memory storage for intermediate results between iterative map and reduce computations., offer easy and composable APIs in multiple languages as a programming model,


## For which cases do you recommend using Spark code?

* Processing in parallel large data sets distributed across a cluster
* Performing ad hoc of interactive queries to explore and visualize data sets
* Building, training, and evaluation machine learning models using MLlib
* Implementing end-to-end data pipelines from myriad streams of data
* Analyzing graph data sets and social networks


## Talk about its architecture

## What are the advantages of using it, what are the adjectives that you would use?

Think of:

* scale


## What are some ways of programming? Example: Functional, Declarative, Imperative.


## Can you talk about MapReduce?

## What's the difference between and Data Scientist and Data Engineer?



## My Observations

- I find Spark easy to use, there is very little boilerplate, it's simple and well designed, easy to manage, has good fault tolerance, it has SQL-like queries, pandas-like flavors... and most importantly, it's FAST!


## What does it mean to have good fault-tolerance?


## What is batch processing?


## When to use monorepo? What's the advantage of it?

If you have many scattered systems or packages, each with their own APIs and configurations, it further adds to the operations complexity engineers have to deal with on a daily basis it will also have a steep learning curve for new developers joining the team.


## Getting Started with Apache Spark 

Let's use the 'local mode', where all the processing is done on a single machine in a Spark shell - this is an easy way to learn the framework, providing a quick feedback loop for iteratively performing Spark operations. Using a Spark shell, you can prototype Spark operations with small data sets before writing a complex Spark application, but for large data sets or real work where you want to reap the benefits of distributed execution, local mode is not suitable - you'll want to use the YARN or Kubernetes deployment mode instead,

The shell only supports Scala, Python and R. You can write a Spark application in any of the supported languages (including Java) and issue queries in Spark SQL. 

## Downloading Apache Spark

Go to the Apache Spark official website and download it for the operations system of choice. 

Developers who only care about learning Spark in Python  have the option of installing PySpark from **PyPI repository**. if you only program in Python, you don't have to install all the other libraries necessary to run Scala, Java or R; this makes the binary smaller.

There are some extra dependencies that can be installed for SQL, ML and MLlib, via `pip install pyspark[sql, ml, mllib]`.

You will need to install Java 8 or above on your machine and set the **JAVA_HOME** environment variable.

Spark comes with 4 widely used interpreters that act like interactive "shells" and enable ad hoc data analysis: `pyspark`, `spark-shell`, `spark-sql`, `sparkR`. These shells have been augmented to support connecting to the cluster and to allow you to load distributed data into Spark workers' memory. Whether you are dealing with gigabytes of data or small data sets, Spark shells are conductive to learning Spark quickly.

To start PySpark just type `pyspark`, in case you have installed PySpark from PyPI in your activated Python environment.

Some useful commands:

```bash
>>> pyspark --help
...
>>> pyspark
...
>>> spark.version
```

ok. Now you are ready to use Spark interpretive shells locally.

## Using the Local Machine

Spark computations are expressed as operations. These operations are then converted into low-level RDD-based bytecode as tasks, which are distributed to Spark's executors for execution.

Let's see an example illustrating the use of the high-level Structured APIs. In it we read in a text file as a DataFrame, show a sample of the strings read, and count the total number of lines in the file. The `show(10, false)` operation on the DataFrame only displays the first 10 lines without truncating; by default the `truncate` Boolean flag is `true`.

To exit any of the Spark shells, press `Ctrl-D`. As you can see, this rapid interactivity with Spark shells is conducive not only to rapid  learning, but to rapid prototyping, too.

The API syntax and signature parity across both Scala and Python is something that has been improved throughout Spark's evolution from 1.x.

We will focus more on the Structured APIs; since Spark 2.x, RDDs are now consigned to low-level APIs.

> Every computation expressed in high-level Structured APIs is decomposed into low-level optimized and generated RDD operations and then converted into Scala bytecode for the executors’ JVMs. This generated RDD operation code is not accessible to users, nor is it the same as the user-facing RDD APIs.

## Understanding Spark Application Concepts

To understand what’s happening under the hood with our sample code, you’ll need to be familiar with some of the key concepts of a Spark application and how the code is transformed and executed as tasks across the Spark executors:

### Application

A user program built on Spark using its APIs. It consists of a driver program and executors on the cluster

### SparkSession

An object that provides a point of entry to interact with underlying Spark functionality and allows programming Spark with its APIs. In an interactive Spark shell, the Spark driver instantiates a `SparkSession` for you, while in a Spark application, you create a `SparkSession` object yourself

### Job

A parallel computation consisting of multiple tasks that gets spawned in response to a Spark action (e.g., `save()`, `collect()`).

### Stage

Each job gets divided into a smaller sets of tasks called stages that depend on each other.

### Task

A single unit of work or execution that will be sent to a Spark executor.

Here’s a simplified diagram that shows the hierarchy and flow of a Spark application

```scss
SPARK APPLICATION
└── Driver Program
    └── SparkSession
        └── [ Your Code using Spark APIs ]
            └── Action Triggered (e.g., collect(), save())
                └── JOB
                    └── STAGE 1
                    │   └── TASK 1
                    │   └── TASK 2
                    │   └── ...
                    └── STAGE 2
                        └── TASK 1
                        └── TASK 2
                        └── ...

Executors (on the cluster) ← receive and run individual TASKS
```

Let’s dig into these concepts in a little more detail.

## Spark Application and SparkSession

At the core of every Spark application is the Spark driver program, which creates a `SparkSession` object. When you're working with a Spark shell, the driver is part of the shell and the `SparkSession` object (accessible via the variable `spark`) is created for you.

In previous example, because you launched the Spark shell locally on your laptop, all the operations ran locally, in a single JVM. But you can just as easily launch s Spark shell to analyze data in parallel on a cluster as in local mode.  The commands `spark-shell --help` or `pyspark --help` will show you how to connect to the Spark cluster manager.

Spark components communicate through the Spark driver in Spark’s distributed architecture:

![Spark components communicate through the Spark driver in Spark’s distributed architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0202.png)

## Spark Jobs

During interactive sessions with Spark shells, the driver converts your Spark application into one or more Spark Jobs. It then transforms each job into a DAG. This, in essence, is Sparks's execution plan, where each node with a DAG could be single or multiple Spark stages.

![ Spark driver creating one or more Spark jobs](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0203.png)

## Spark Stages

As part of the DAG nodes, stages are created based on what operations can be performed serially or in parallel. Not all Spark operations can happen in a single stage, so they may be divided into multiple stages. Often stages are delineated on the operator's computation boundaries, where they dictate data transfer among Spark executors.

![Spark job creating one or more stages](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0204.png)

In simpler terms:

* A **stage** in Spark is a chunk of the computation that can be executed without a shuffle.

* When an operation requires a **shuffle** (data movement between executors), Spark **delineates** or **splits** the computation into a new stage at that point.

This is crucial for Spark's performance and planning, as stages help manage where and how data moves across the cluster.

## Spark Tasks

Each stage is comprised of Spark tasks (a unit of execution), which are then federated across each Spark executor; each task maps to a single core and works on a single partition of data. As such, an executor with 16 cores can have 16 or more tasks working on 16 or more partitions in parallel, making the execution of Spark's tasks exceedingly parallel!

![Spark stage creating one or more tasks to be distributed to executors](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0205.png)

## Transformations, Actions, and Lazy Evaluation

Spark operations on distributed data can be classified into two types: _transformations_ and _actions_. Transformations, transform a Spark DataFrame into a new DataFrame without altering the original data, giving it the property of immutability. Put another way, an operation such as `select()` or `filter` will not change the original DataFrame; instead, it will return the transformed results of the operation as a new DataFrame.

All transformations are evaluated lazily. That is, their results are not computed immediately, but they are recorded or remembered as a _lineage_. A recorded lineage allows Spark, at a later time in its execution plan, to rearrange certain transformations, coalesce them, or optimize transformations into stages for more efficient execution. Lazy evaluation is Spark's strategy for delaying execution until an action is invoked or data is "touched" (read from or written to disk).

An action triggers the lazy evaluation of all the recorded transformations. In the following image, all transformations T are recorded until the action A is invoked. Each transformation T produces a new DataFrame.

![Lazy transformations and eager actions](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0206.png)

While lazy evaluation allows Spark to optimize your queries by peeking into your chained transformations, lineage and data immutability provide fault tolerance. Because Spark records each transformation in its lineage and the DataFrames are immutable between transformation, it can reproduce its original state by simply replaying the recorded lineage, giving it resiliency in the event of failures.


| Transformations | Actions   |
|-----------------|-----------|
| orderBy()       | show()    |
| groupBy()       | take()    |
| filter()        | count()   |
| select()        | collect() |
| join()          | save()    |

The action is what triggers the execution  of all transformations recorded as part of the query execution plan. In this example, nothing happens until `filtered.count()` is executed in the shell.

```python
strings = spark.read.text("README.md")
filtered = strings.filter(strings.value.contains("Spark"))
filtered.count()
```

Other simplified ways to write the above code:

```python
spark.read.text("README.md").filter("value LIKE '%Spark%'").count()
```

```python
from pyspark.sql.functions import col

spark.read.text("README.md").filter(col("value").contains("Spark")).count()
```

Note that the code above gets the `Total number of lines containing the word Spark`, not the number of occurrences.

## Narrow and Wide Transformations

As noted, transformations are operations that Spark evaluates lazily. A huge advantage of the lazy evaluation scheme is that Spark can inspect your computational query and ascertain how it can optimize it. This optimization can be done by either joining or pipelining some operations and assigning them to a stage, or breaking them into stages by determining which operations require a shuffle or exchange of data across clusters.

Transformations can be classified as having either **narrow dependencies** or **wide dependencies**. Any transformation where a single output partition can be computed from a single input partition is a narrow transformation. For example, in the previous code snippet, `filter()` and `contains()` represent narrow transformations because they can operate on a single partition and produce the resulting output partition without any exchange of data.

However, transformations such as `groupBy()` or `orderBy()` instruct Spark to perform wide transformations, where data from other partitions is read in, combined, and written to disk. If we were to sort the `filtered` DataFrame from a preceding example by calling `.orderBy()`, each partition will be locally sorted, but we need to force a shuffle of data from each of the executor's partitions across the cluster to sort all of the records. In contrast to narrow transformations, wide transformations require output  from other partitions to compute the final aggregation.

![alt text](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0207.png)

## The Spark UI

Spark includes a [graphical user interface ](https://spark.apache.org/docs/latest/web-ui.html) that you can use to inspect or monitor Spark applications in their various stages of decomposition - that is jobs, stages and tasks. Depending on how Spark is deployed, the driver launches a Web UI, running by default on port 4040, where you can view metrics details such as:

* a list of scheduler stages and tasks
* a summary of RDD sizes and memory usage
* information about the environment
* information about the running executors
* All the Spark SQL queries

In local mode, you can access this interface at [http://localhost:4040/](http://<localhost>:4040) in a web browser.

> When you launch `spark-shell`, part of the output shows the localhost URL to access at port 4040.

Let’s inspect how the Python example from the previous section translates into jobs, stages, and tasks. To view what the DAG looks like, click on “DAG Visualization” in the web UI. As image shows, the driver created a single job and a single stage.

![The DAG for our simple Python example](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0208.png)

Notice that there is no **Exchange**, where data is exchanged between executors, required because there is only a single stage. The individual operations of the stage are shown in blue boxes.

Stage 0 is comprised of one task. If you have multiple tasks, they will be executed in parallel. You can view the details of each stage in the Stages tab, as shown in image.

![alt text](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0209.png)

> The UI provides a microscopic lens into Spark’s internal workings as a tool for debugging and inspecting.

## Databricks Community Edition

Databricks is a company that offers a managed Apache Spark platform in the cloud. In addition to running Spark locally on your own machine, you can try many of the examples in this and other chapters using the **Databricks Free Tier** — the modern replacement for the now-deprecated **Community Edition**. The Free Tier provides temporary access to a full-featured Databricks environment, including support for Python, R, Scala, SQL, Delta Lake, and machine learning workflows. It also includes tutorials, sample datasets, and notebooks, making it ideal for experimentation and learning. You can write your own notebooks or import others, including Jupyter notebooks, and take advantage of collaborative features and cloud-backed compute.

[Databricks Free Edition](https://www.databricks.com/learn/free-edition)

## Your First Standalone Application

### Counting M&Ms for the Cookie Monster


