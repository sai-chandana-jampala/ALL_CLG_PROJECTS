import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{col, lag, when, avg, lit}


val conf = new SparkConf().setAppName("MySparkApplication").setMaster("local[2]")
val sc = new SparkContext(conf)



val spark = SparkSession.builder.appName("MySparkApplication").getOrCreate()

val spark = SparkSession.builder()
  .appName("JDBC Spark")
  .config("spark.master", "local")
  .getOrCreate()

// Database connection properties
val url = "jdbc:mysql://localhost:3306/project"
val properties = new java.util.Properties()
properties.setProperty("user", "root")
properties.setProperty("password", "jaidev@2003")

// Read data from the database table using JDBC
val df = spark.read.jdbc(url, "stock_data ", properties).na.fill(0)
df.show()





val niftyFMCGWithDate = df.withColumn("Date", to_date(col("Date")))


//Percentage Change in Closing Price
val percentageChange = df
  .withColumn("PercentChange", ((col("Close") - lag("Close", 1).over(Window.orderBy("Date"))) / lag("Close", 1).over(Window.orderBy("Date"))) * 100)

percentageChange.show()


//Market Sentiment Analysis
val marketSentiment = df
  .withColumn("Sentiment", when(col("Close") > lag("Close", 1).over(Window.orderBy("Date")), "Positive").otherwise("Negative"))
  .orderBy("Date")

marketSentiment.show()

//Relative Strength Index (RSI)
val rsiWindow: Int = 14

val rsi = df
  .withColumn("PriceChange", col("Close") - lag("Close", 1).over(Window.orderBy("Date")))
  .withColumn("Gain", when(col("PriceChange") > 0, col("PriceChange")).otherwise(0))
  .withColumn("Loss", when(col("PriceChange") < 0, -col("PriceChange")).otherwise(0))
  .withColumn("AverageGain", avg("Gain").over(Window.orderBy("Date").rowsBetween(-rsiWindow, -1)))
  .withColumn("AverageLoss", avg("Loss").over(Window.orderBy("Date").rowsBetween(-rsiWindow, -1)))
  .withColumn("RS", col("AverageGain") / col("AverageLoss"))
  .withColumn("RSI", lit(100.0) - (lit(100.0) / (lit(1.0) + col("RS"))))
  .orderBy("Date")

rsi.show()



//Percentage Change in Sales
val salesPercentageChange = df
  .withColumn("SalesChange", ((col("Volume") - lag("Volume", 1).over(Window.orderBy("Date"))) / lag("Volume", 1).over(Window.orderBy("Date"))) * 100)

salesPercentageChange.show()

//Monthly Price Momentum
val monthlyPriceMomentum = niftyFMCGWithDate
  .withColumn("Month", month(col("Date")))
  .withColumn("PriceMomentum", col("Close") - lag("Close", 1).over(Window.partitionBy("Month").orderBy("Date")))
  .groupBy("Month")
  .agg(avg(col("PriceMomentum")).alias("AvgPriceMomentum"))
  .orderBy("Month")

monthlyPriceMomentum.show()

//Rolling Standard Deviation of Closing Price
val rollingStdDevClosing = df
  .withColumn("RollingStdDev", stddev(col("Close")).over(Window.orderBy("Date").rowsBetween(-5, 0)))

rollingStdDevClosing.show()

//Price and Volume Correlation
val priceVolumeCorrelation = df
  .select(corr(col("Close"), col("Volume")).alias("Correlation"))

priceVolumeCorrelation.show()

// Cumulative returns
val cumulativeReturns = df
  .withColumn("Return", (col("Close") - lag("Close", 1).over(Window.orderBy("Date"))) / lag("Close", 1).over(Window.orderBy("Date")))
  .withColumn("CumulativeReturn", sum(col("Return")).over(Window.orderBy("Date")))
  .orderBy("Date")

cumulativeReturns.show()

//Price Gap Analysis
val priceGapWithMonth = df
  .withColumn("PriceGap", col("Open") - col("Close"))
  .withColumn("Month", month(col("Date")))
  .orderBy(desc("PriceGap"))
  .limit(50)
  .groupBy("Month")
  .count()
  .orderBy(desc("count"))


priceGapWithMonth.show()

//Moving Average Analysis
val movingAvg = df
  .withColumn("5DayMovingAvg", avg(col("Close")).over(Window.orderBy("Date").rowsBetween(-4, 0)))
  .orderBy("Date")

movingAvg.show()

// High-Low Range Analysis
val highLowRange = df
  .withColumn("HighLowRange", col("High") - col("Low"))
  .orderBy(desc("HighLowRange"))

highLowRange.show()


// Trading Volume Trends
val volumeTrends = df
  .withColumn("VolumeTrend", col("Volume") - lag("Volume", 1).over(Window.orderBy("Date")))
  .orderBy("Date")

volumeTrends.show()


import org.apache.spark.ml.regression.LinearRegression
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.ml.evaluation.RegressionEvaluator

val featureColumns = Array("Open", "High", "Low", "Volume")  // Adjust these based on your dataset
val assembler = new VectorAssembler().setInputCols(featureColumns).setOutputCol("features")
val assembledDF = assembler.transform(df).select("features", "Close")


// Split the data into training and test sets (80% training, 20% testing)
val Array(trainingData, testData) = assembledDF.randomSplit(Array(0.8, 0.2), seed = 1234)

// Create a linear regression model
val lr = new LinearRegression().setLabelCol("Close").setFeaturesCol("features")

// Fit the model to the training data
val lrModel = lr.fit(trainingData)

// Make predictions on the test data
val predictions = lrModel.transform(testData)
// Evaluate the performance of the model
val evaluator = new RegressionEvaluator().setLabelCol("Close").setPredictionCol("prediction").setMetricName("rmse")
val rmse = evaluator.evaluate(predictions)
println(s"Root Mean Squared Error (RMSE) on test data = $rmse")

// Show the predicted values
predictions.select("features", "Close", "prediction").show()





sc.stop()
spark.stop()







