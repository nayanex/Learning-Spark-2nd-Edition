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


