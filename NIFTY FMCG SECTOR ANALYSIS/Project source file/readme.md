BIG DATA AND DATABASE MANAGEMENT SYSTEM
21AIE304

NIFTY FMCG SECTOR ANALYSIS 

BATCH: B
GROUP: 2

## Overview
This project demonstrates setting up a Spark Scala project in IntelliJ IDEA, integrating with a MySQL database using JDBC for data processing.


Project Source file:
- fmcg_project (codes file)
----- src -> main -> scala -> Project.sc
- Gui (gui files)
- Visualizations
- BatchB_Group2_BDMS_Endsem_report.pdf (report)
- fmcg_data.csv (dataset)
- BatchB_Group2_BDMS_Endsem.pptx



## Prerequisites
- IntelliJ IDEA
- Scala Plugin for IntelliJ
- Apache Spark
- MySQL Database
- JDBC Driver for MySQL

## Steps to Set Up

### 1. Install IntelliJ IDEA and Scala Plugin
- Download and install IntelliJ IDEA: https://www.jetbrains.com/idea/download/
- Install the Scala plugin: Open IntelliJ -> Configure -> Plugins -> Search for "Scala" -> Install and Restart IntelliJ.

### 2. Create a New Scala Project
- Open IntelliJ -> File -> New -> Project -> Scala -> sbt -> Next.
- Set project details and click Finish.

### 3. Add Spark Dependency
- Open `build.sbt` file.
- Add the Spark dependency:
  ```scala
  libraryDependencies += "org.apache.spark" %% "spark-core" % "3.2.0"


We have to create a scala worksheet with .sc extension (Project.sc)

Set Spark home: Edit configurations -> Add new configuration -> Set Spark home in "Environment variables."

### 4. Add JDBC Dependency

- Open `build.sbt` file.
- From https://mvnrepository.com/artifact/com.mysql/mysql-connector-j get the sbt file.
- libraryDependencies += "mysql" % "mysql-connector-java" % "8.0.23"


### 5. Connect to MySQL using JDBC
- Open project.sc
- val spark = SparkSession.builder()
  .appName("JDBC Spark")
  .config("spark.master", "local")
  .getOrCreate()

// Database connection properties
val url = "jdbc:mysql://localhost:3306/project"
val properties = new java.util.Properties()
properties.setProperty("user", "root")
properties.setProperty("password", "jaidev@2003")


Run your scala worksheet (project.sc) with all analysis and machine learning code within it.

To run the GUI, All the visualizations and the main code along with the webpage(.html) created is added in a single folder. On running the gui.html we can access the interactive web page made. 