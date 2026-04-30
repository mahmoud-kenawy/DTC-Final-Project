from confluent_kafka import Producer
import requests
import json
import time
import os

producer = Producer({
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
})

while True:
    try:
        print("Producing data to Kafka...")
        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            time.sleep(60)
            continue

        print("Data fetched successfully")
        json_data = json.loads(response.text)

        producer.produce(
            'earthquake-data',
            value=json.dumps(json_data).encode('utf-8')
        )
        producer.flush()
        print("Data produced to Kafka successfully")

    except requests.exceptions.Timeout:
        print("Request timed out. Retrying in 60 seconds...")

    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")

    time.sleep(60)
