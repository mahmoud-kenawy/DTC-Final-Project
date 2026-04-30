import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import (
    StructType, StructField, StringType, ArrayType,
    DoubleType, LongType, IntegerType
)


def main():
    project_id = os.getenv("GCP_PROJECT_ID", "usgs-gcp")
    dataset = os.getenv("GCP_BQ_DATASET", "usgs_data")
    table = "earthquake"

    spark = SparkSession.builder \
        .appName("USGS_Earthquake_Kafka_Consumer") \
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.0"
        ) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # غيّر السطر ده
    kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka-stream:9092')

    # 1. Read Stream from Kafka
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", "earthquake-data") \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

    # 2. Define Schema for USGS GeoJSON
    schema = StructType([
        StructField("type", StringType(), True),
        StructField("features", ArrayType(StructType([
            StructField("id", StringType(), True),
            StructField("properties", StructType([
                StructField("mag", DoubleType(), True),
                StructField("place", StringType(), True),
                StructField("time", LongType(), True),
                StructField("updated", LongType(), True),
                StructField("tz", IntegerType(), True),
                StructField("url", StringType(), True),
                StructField("detail", StringType(), True)
            ]))
        ])), True)
    ])

    # 3. Parse JSON and Explode Features Array
    parsed_stream = raw_stream \
        .selectExpr("CAST(value AS STRING) as json_str") \
        .withColumn("data", from_json(col("json_str"), schema)) \
        .select(explode(col("data.features")).alias("feature"))

    # 4. Flatten columns to match BigQuery schema
    flattened_stream = parsed_stream.select(
        col("feature.id").alias("id"),
        col("feature.properties.mag").alias("properties_mag"),
        col("feature.properties.place").alias("properties_place"),
        col("feature.properties.time").alias("properties_time"),
        col("feature.properties.updated").alias("properties_updated"),
        col("feature.properties.tz").alias("properties_tz"),
        col("feature.properties.url").alias("properties_url"),
        col("feature.properties.detail").alias("properties_detail")
    )

    # 5. Write Stream to BigQuery
    def write_to_bigquery(df, epoch_id):
        if not df.isEmpty():
            df_unique = df.dropDuplicates(["id"])
            df_unique.write \
                .format("bigquery") \
                .option("table", f"{project_id}.{dataset}.{table}") \
                .option("writeMethod", "direct") \
                .mode("append") \
                .save()
            print(f"Batch {epoch_id} written to BigQuery — {df_unique.count()} rows.")

    query = flattened_stream.writeStream \
        .foreachBatch(write_to_bigquery) \
        .outputMode("append") \
        .option("checkpointLocation", "/tmp/spark-checkpoint/earthquake") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()
