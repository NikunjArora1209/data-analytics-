from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum
import pandas as pd

spark = SparkSession.builder.appName("DF").getOrCreate()


df = spark.read.csv("FinalREAData.csv", header=True, inferSchema=True)

df = df.toDF(*[c.strip() for c in df.columns])


df.show(5)


df = df.withColumn("Quantity", col("Quantity").cast("int"))



daily_demand = df.groupBy("Product Name", "Order Date").agg(
    sum("Quantity").alias("Demand")
)


pdf = daily_demand.toPandas()


pdf["Order Date"] = pd.to_datetime(pdf["Order Date"], errors="coerce")

pdf = pdf.sort_values(by=["Product Name", "Order Date"])

e
pdf["Moving_Average"] = pdf.groupby("Product Name")["Demand"] \
                           .rolling(3).mean().reset_index(0, drop=True)


pdf.to_csv("Demand_Forecast_Data.csv", index=False)

print("DONE")