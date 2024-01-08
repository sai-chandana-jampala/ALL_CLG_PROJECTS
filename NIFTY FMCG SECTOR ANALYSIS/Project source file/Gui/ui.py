import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import month, avg, stddev, col, lag, date_format, last, first
from pyspark.sql.window import Window
import pandas as pd
import os
os.environ['PYSPARK_PYTHON'] = '/bin/python3'  # Adjust the path accordingly

# Create a Spark session
spark = SparkSession.builder.appName("GoldAnalysis").getOrCreate()

# Assuming 'df' is your PySpark DataFrame
df = spark.read.csv("home/vignesh/Downloads/GOLDBEES.csv", header=True)

# Functions for each analysis
def display_monthly_average():
    monthly_avg_price = df \
        .withColumn("Month", month("Date")) \
        .groupBy("Month") \
        .agg(avg("Close").alias("Avg_Close")) \
        .orderBy("Month")

    pandas_df = monthly_avg_price.toPandas()

    plt.figure(figsize=(10, 6))
    plt.plot(pandas_df['Month'], pandas_df['Avg_Close'], marker='o', linestyle='-', color='b')
    plt.title('Monthly Average Gold Prices')
    plt.xlabel('Month')
    plt.ylabel('Average Closing Price')
    plt.grid(True)
    plt.show()

def monthly_volatility():
    monthly_volatility = df \
        .withColumn("Month", month("Date")) \
        .groupBy("Month") \
        .agg(stddev((col("High") - col("Low")) / col("Close")).alias("Monthly_Volatility")) \
        .orderBy("Month")

    pandas_volatility_df = monthly_volatility.toPandas()

    plt.figure(figsize=(10, 6))
    plt.bar(pandas_volatility_df['Month'], pandas_volatility_df['Monthly_Volatility'], color='orange')
    plt.title('Monthly Price Volatility')
    plt.xlabel('Month')
    plt.ylabel('Volatility (High-Low/Close)')
    plt.grid(axis='y')
    plt.show()

def seasonal_patterns():
    # Apply the same analysis for seasonal patterns
    seasonal_patterns = df \
    .withColumn("Month", month("Date")) \
    .groupBy("Month") \
    .agg(avg("Close").alias("Avg_Close")) \
    .orderBy("Month")

    # Show the resulting DataFrame
    seasonal_patterns.show()

    # Convert PySpark DataFrame to Pandas DataFrame for plotting
    pandas_seasonal_df = seasonal_patterns.toPandas()

    # Plot the seasonal patterns
    plt.figure(figsize=(10, 6))
    plt.plot(pandas_seasonal_df['Month'], pandas_seasonal_df['Avg_Close'], marker='o', linestyle='-', color='green')
    plt.title('Seasonal Patterns in Gold Prices')
    plt.xlabel('Month')
    plt.ylabel('Average Closing Price')
    plt.grid(True)
    plt.show()

def roi():
    # Apply the same analysis for return on investments (ROI)
    window_spec = Window.orderBy("Date")
    roi = df \
    .withColumn("ROI", (col("Close") - first("Close").over(window_spec)) / first("Close").over(window_spec) * 100)

    # Show the resulting DataFrame
    roi.show()

    # Convert PySpark DataFrame to Pandas DataFrame for plotting
    pandas_roi_df = roi.toPandas()

    # Plot the return on investments
    plt.figure(figsize=(10, 6))
    plt.plot(pandas_roi_df['Date'], pandas_roi_df['ROI'], marker='o', linestyle='-', color='purple')
    plt.title('Return on Investments in Gold')
    plt.xlabel('Date')
    plt.ylabel('ROI (%)')
    plt.grid(True)
    plt.show()


def short_term():
    # Apply the same analysis for short-term trend
    short_term_trend = df \
    .withColumn("ShortTermMA", avg(col("Close")).over(Window.orderBy("Date").rowsBetween(-10, 0)))

    # Show the resulting DataFrame for short-term trend
    short_term_trend.select("Date", "Close", "ShortTermMA").show()

    # Convert PySpark DataFrame to Pandas DataFrame for plotting
    pandas_short_term_df = short_term_trend.toPandas()

    # Plot the short-term trend
    plt.figure(figsize=(10, 6))
    plt.plot(pandas_short_term_df['Date'], pandas_short_term_df['Close'], label='Closing Price', color='blue')
    plt.plot(pandas_short_term_df['Date'], pandas_short_term_df['ShortTermMA'], label='Short-Term Moving Average', linestyle='--', color='orange')
    plt.title('Short-Term Trend in Gold Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def long_term():
    # Apply the same analysis for long-term trend
    long_term_trend = df \
    .withColumn("LongTermMA", avg(col("Close")).over(Window.orderBy("Date").rowsBetween(-50, 0)))

    # Show the resulting DataFrame for long-term trend
    long_term_trend.select("Date", "Close", "LongTermMA").show()

    # Convert PySpark DataFrame to Pandas DataFrame for plotting
    pandas_long_term_df = long_term_trend.toPandas()

    # Plot the long-term trend
    plt.figure(figsize=(10, 6))
    plt.plot(pandas_long_term_df['Date'], pandas_long_term_df['Close'], label='Closing Price', color='blue')
    plt.plot(pandas_long_term_df['Date'], pandas_long_term_df['LongTermMA'], label='Long-Term Moving Average', linestyle='--', color='green')
    plt.title('Long-Term Trend in Gold Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()
def rolling_volatility():
    # Apply the same analysis for rolling volatility
    rolling_volatility = df \
    .withColumn("PriceChange", col("Close") - lag("Close", 1).over(Window.orderBy("Date")))

    rolling_volatility = rolling_volatility \
    .withColumn("RollingVolatility", stddev("PriceChange").over(Window.orderBy("Date").rowsBetween(-10, 0)))

    # Show the resulting DataFrame for rolling volatility
    rolling_volatility.select("Date", "Close", "RollingVolatility").show()

    # Convert PySpark DataFrame to Pandas DataFrame for plotting
    pandas_rolling_volatility_df = rolling_volatility.toPandas()

    # Plot the rolling volatility as a bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(pandas_rolling_volatility_df['Date'], pandas_rolling_volatility_df['RollingVolatility'], color='orange')
    plt.title('Rolling Volatility in Gold Prices')
    plt.xlabel('Date')
    plt.ylabel('Rolling Volatility')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def weekday():
    weekday_price_patterns = df \
    .withColumn("Weekday", date_format(col("Date"), "E")) \
    .groupBy("Weekday") \
    .agg(avg("Close").alias("Avg_Close")) \
    .orderBy("Weekday")

    pandas_weekday_df = weekday_price_patterns.toPandas()

    # Manually reorder the DataFrame based on the weekday_order
    pandas_weekday_df['Weekday'] = pd.Categorical(pandas_weekday_df['Weekday'], categories= weekday_order, ordered=True)
    pandas_weekday_df = pandas_weekday_df.sort_values('Weekday')

    # Plot the weekday price patterns as a bar plot with adjusted y-axis limits
    plt.figure(figsize=(10, 6))
    plt.bar(pandas_weekday_df['Weekday'], pandas_weekday_df['Avg_Close'], color='purple')
    plt.title('Weekday Price Patterns in Gold Prices')
    plt.xlabel('Weekday')
    plt.ylabel('Average Closing Price')

    # Set y-axis limits to display only within the range of 45 to 55
    plt.ylim(50, 51)

    plt.show()

def month():
    month_end_price_movement = df \
    .withColumn("MonthEnd", date_format(col("Date"), "yyyy-MM")) \
    .groupBy("MonthEnd") \
    .agg(last("Close").alias("MonthEnd_Close")) \
    .orderBy("MonthEnd")

    # Show the resulting DataFrame for month-end price movements
    month_end_price_movement.show()

    # Convert PySpark DataFrame to Pandas DataFrame for plotting
    pandas_month_end_df = month_end_price_movement.toPandas()

    # Plot the month-end price movements as a line plot
    plt.figure(figsize=(12, 6))
    plt.plot(pandas_month_end_df['MonthEnd'], pandas_month_end_df['MonthEnd_Close'], marker='o', linestyle='-', color='green')
    plt.title('Month-End Price Movements in Gold Prices')
    plt.xlabel('Month-End')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
def percent_change():
    # Percentage Change in Sales
    salesPercentageChange = df \
    .withColumn("SalesChange", ((col("Volume") - lag("Volume", 1).over(Window.orderBy("Date"))) / lag("Volume", 1).over(Window.orderBy("Date"))) * 100)

    # Convert PySpark DataFrame to Pandas DataFrame
    pandas_sales_percentage_change = salesPercentageChange.toPandas()

    # Plot for Percentage Change in Sales over time
    plt.figure(figsize=(12, 6))
    plt.plot(pandas_sales_percentage_change["Date"], pandas_sales_percentage_change["SalesChange"], label="Percentage Change in Sales")
    plt.title('Percentage Change in Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Percentage Change')
    plt.legend()
    plt.show()

def arp():
    # Calculate True Range
    true_range = df.withColumn("HighLow", F.col("High") - F.col("Low")) \
    .withColumn("HighClose", F.abs(F.col("High") - F.lag("Close").over(Window.orderBy("Date")))) \
    .withColumn("LowClose", F.abs(F.col("Low") - F.lag("Close").over(Window.orderBy("Date")))) \
    .withColumn("TrueRange", F.greatest(F.col("HighLow"), F.col("HighClose"), F.col("LowClose")))

    # Calculate Average True Range (ATR)
    atr = true_range.withColumn("ATR", F.avg("TrueRange").over(Window.orderBy("Date").rowsBetween(-14, 0)))

    # Select relevant columns
    result_df = atr.select("Date", "Close", "ATR")

    # Convert the Spark DataFrame to Pandas for visualization
    result_pd = result_df.toPandas()

    # Plot the ATR values
    plt.figure(figsize=(10, 6))
    plt.plot(result_pd["Date"], result_pd["ATR"], label="ATR", color="blue")
    plt.title("Average True Range (ATR) Over Time")
    plt.xlabel("Date")
    plt.ylabel("ATR")
    plt.legend()
    plt.show()

# Stop the Spark session
spark.stop()
# Create main window
root = tk.Tk()
root.title("Gold Analysis GUI")

# Dropdown menu options
analysis_options = [
    'Monthly Average Gold Prices',
    'Monthly Price Volatility',
    'Seasonal Patterns in Gold Prices',
    'Return on Investments in Gold',
    'Short-Term Trend in Gold Prices',
    'Long-Term Trend in Gold Prices',
    'Rolling Volatility in Gold Prices',
    'Weekday Price Patterns in Gold Prices',
    'Month-End Price Movements in Gold Prices',
    'Quarterly Trends in Gold Prices',
    'Percentage Change in Sales Over Time',
    'Average True Range (ATR) Over Time'
]

selected_option = tk.StringVar(root)
selected_option.set(analysis_options[0])  # Set default option

# Dropdown menu
dropdown = ttk.Combobox(root, textvariable=selected_option, values=analysis_options)
dropdown.pack(padx=20, pady=10)

def display_visualization():
    selected_analysis = dropdown.get()
    if selected_analysis == 'Monthly Average Gold Prices':
        display_monthly_average()
    elif selected_analysis == 'Monthly Price Volatility':
        monthly_volatility()
    elif selected_analysis == 'Seasonal Patterns in Gold Prices':
        seasonal_patterns()
    elif selected_analysis == 'Return on Investments in Gold':
        roi()
    elif selected_analysis == 'Short-Term Trend in Gold Prices':
        short_term()
    # Add conditions for other analyses...
    elif selected_analysis == 'Long-Term Trend in Gold Prices':
        long_term()
    elif selected_analysis == 'Rolling Volatility in Gold Prices':
        rolling_volatility()
    elif selected_analysis == 'Weekday Price Patterns in Gold Prices':
        weekday()
    elif selected_analysis == 'Average True Range (ATR) Over Time':
        arp()

# Display visualization button
visualization_button = tk.Button(root, text="Display Visualization", command=display_visualization)
visualization_button.pack(padx=20, pady=10)

# Run the application
root.mainloop()