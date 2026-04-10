from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count

def main():
    # Create Spark Session
    spark = SparkSession.builder \
        .appName("SupplyChain_REA") \
        .getOrCreate()

    # Load dataset
    file_path = "SupplychainData.csv"
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Rename columns
    df = (
        df.withColumnRenamed("Days for shipping (real)", "ATA")
          .withColumnRenamed("Days for shipment (scheduled)", "ETA")
    )

    # Create Delay column
    df = df.withColumn("Delay", col("ATA") - col("ETA"))

    # Create Delay Status
    df = df.withColumn(
        "Delay_Status",
        when(col("Delay") > 0, "Late").otherwise("On Time")
    )

    # Create Route column
    df = df.withColumn("Route", col("Order Region"))

    # Show shipment-level data
    print("\n Shipment-Level Data:")
    df.select("Order Id", "Route", "ATA", "ETA", "Delay", "Delay_Status").show(10, truncate=False)

    # Route Efficiency Analysis
    route_analysis = (
        df.groupBy("Route")
          .agg(
              avg("Delay").alias("Average_Delay"),
              count("Order Id").alias("Total_Orders")
          )
          .orderBy(col("Average_Delay").desc())
    )

    print("\n Route Efficiency Analysis:")
    route_analysis.show(truncate=False)

    # On-Time Delivery %
    total_orders = df.count()
    on_time_orders = df.filter(col("Delay") <= 0).count()

    on_time_percentage = (on_time_orders / total_orders) * 100 if total_orders > 0 else 0

    print(f"\n On-Time Delivery %: {on_time_percentage:.2f}%")

    # Save final dataset (avoid large memory issues)
    output_path = "Final_REA_Data.csv"
    df.coalesce(1).write.csv(output_path, header=True, mode="overwrite")

    print("\n Final dataset saved successfully!")

    spark.stop()


if __name__ == "__main__":
    main()