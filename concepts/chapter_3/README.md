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

`expressivity, simplicity, composability, and uniformity`




