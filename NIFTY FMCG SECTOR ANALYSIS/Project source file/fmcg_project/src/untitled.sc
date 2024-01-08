import org.apache.spark.sql.functions._
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{col, lag, when, avg, lit}
import org.apache.spark.sql.types.LongType


val conf = new SparkConf().setAppName("MySparkApplication").setMaster("local[2]")
val sc = new SparkContext(conf)

val spark = SparkSession.builder.appName("MySparkApplication").getOrCreate()

// Load the dataset
val chessData = spark.read.option("header", "true").csv("C:\\Users\\jaide\\Downloads\\games.csv")
chessData.show()

// Count the occurrences of wins for each side
val whiteWins = chessData.filter($"winner" === "white").count()
val blackWins = chessData.filter($"winner" === "black").count()
val totalGames = chessData.count()

// Calculate win percentages
val whiteWinPercentage = (whiteWins.toDouble / totalGames) * 100
val blackWinPercentage = (blackWins.toDouble / totalGames) * 100

// Calculate the statistical significance of the win percentage difference
val winPercentageDifference = whiteWinPercentage - blackWinPercentage
val significanceLevel = 0.05 // Define the significance level for the test

// Perform a two-proportion z-test to check if the win percentage difference is statistically significant
val zScore = math.abs((whiteWinPercentage / 100 - blackWinPercentage / 100) / math.sqrt(((whiteWinPercentage / 100) * (1 - whiteWinPercentage / 100)) / totalGames + ((blackWinPercentage / 100) * (1 - blackWinPercentage / 100)) / totalGames))
val criticalValue = org.apache.commons.math3.distribution.NormalDistribution.inverseCumulativeProbability(1 - significanceLevel / 2)
val isSignificant = zScore > criticalValue

// Display results
println(s"White wins: $whiteWins games")
println(s"Black wins: $blackWins games")
println(s"Total games analyzed: $totalGames")
println(s"Percentage of white wins: $whiteWinPercentage%")
println(s"Percentage of black wins: $blackWinPercentage%")
println(s"Win percentage difference: $winPercentageDifference%")
println(s"Is the win percentage difference statistically significant at $significanceLevel significance level? $isSignificant")



sc.stop()