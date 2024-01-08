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

val options = Map("header" -> "true", "inferSchema" -> "true", "delimiter" -> ",")
val csvFilePath = "C:\\Users\\jaide\\Downloads\\fmcg_data.csv"
val niftyFMCG = spark.read.options(options).csv(csvFilePath)
niftyFMCG.show()


val niftyFMCGWithDate = niftyFMCG.withColumn("Date", to_date(col("Date")))


//Percentage Change in Closing Price
val percentageChange = niftyFMCG
  .withColumn("PercentChange", ((col("Close") - lag("Close", 1).over(Window.orderBy("Date"))) / lag("Close", 1).over(Window.orderBy("Date"))) * 100)

percentageChange.show()

//Relative Strength Index (RSI)
val rsiWindow: Int = 14

val rsi = niftyFMCG
  .withColumn("PriceChange", col("Close") - lag("Close", 1).over(Window.orderBy("Date")))
  .withColumn("Gain", when(col("PriceChange") > 0, col("PriceChange")).otherwise(0))
  .withColumn("Loss", when(col("PriceChange") < 0, -col("PriceChange")).otherwise(0))
  .withColumn("AverageGain", avg("Gain").over(Window.orderBy("Date").rowsBetween(-rsiWindow, -1)))
  .withColumn("AverageLoss", avg("Loss").over(Window.orderBy("Date").rowsBetween(-rsiWindow, -1)))
  .withColumn("RS", col("AverageGain") / col("AverageLoss"))
  .withColumn("RSI", lit(100.0) - (lit(100.0) / (lit(1.0) + col("RS"))))
  .orderBy("Date")

rsi.show()

//Market Sentiment Analysis
val marketSentiment = niftyFMCG
  .withColumn("Sentiment", when(col("Close") > lag("Close", 1).over(Window.orderBy("Date")), "Positive").otherwise("Negative"))
  .orderBy("Date")

marketSentiment.show()


//Percentage Change in Sales
val salesPercentageChange = niftyFMCG
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
val rollingStdDevClosing = niftyFMCG
  .withColumn("RollingStdDev", stddev(col("Close")).over(Window.orderBy("Date").rowsBetween(-5, 0)))

rollingStdDevClosing.show()

// Cumulative returns
val cumulativeReturns = niftyFMCG
  .withColumn("Return", (col("Close") - lag("Close", 1).over(Window.orderBy("Date"))) / lag("Close", 1).over(Window.orderBy("Date")))
  .withColumn("CumulativeReturn", sum(col("Return")).over(Window.orderBy("Date")))
  .orderBy("Date")

cumulativeReturns.show()

//Price and Volume Correlation
val priceVolumeCorrelation = niftyFMCG
  .select(corr(col("Close"), col("Volume")).alias("Correlation"))

priceVolumeCorrelation.show()

//Price Gap Analysis
val priceGap = niftyFMCG
  .withColumn("PriceGap", col("Open") - col("Close"))
  .orderBy(desc("PriceGap"))

priceGap.show()

//Moving Average Analysis
val movingAvg = niftyFMCG
  .withColumn("5DayMovingAvg", avg(col("Close")).over(Window.orderBy("Date").rowsBetween(-4, 0)))
  .orderBy("Date")

movingAvg.show()

// High-Low Range Analysis
val highLowRange = niftyFMCG
  .withColumn("HighLowRange", col("High") - col("Low"))
  .orderBy(desc("HighLowRange"))

highLowRange.show()


// Trading Volume Trends
val volumeTrends = niftyFMCG
  .withColumn("VolumeTrend", col("Volume") - lag("Volume", 1).over(Window.orderBy("Date")))
  .orderBy("Date")

volumeTrends.show()







// Stop SparkContext and SparkSession when done
sc.stop()
spark.stop()


