import time
import json
import sys
import random
from confluent_kafka import Producer
from faker import Faker
from datetime import datetime
import argparse
from kafka import KafkaProducer

def simulate_transaction():
    fake = Faker()
    amount = round(random.uniform(10, 1000), 2)
    status = random.choice(["approved", "approved", "approved", "declined",])
    adquirente = random.choice(["Rede", "Cielo", "GetNet", "Stone"])
    estado = random.choice(['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'] )
    transaction = {
        "amount": amount,
        "status": status,
        "estado": estado,
        "adquirente": adquirente,
        "transaction_occured_at": datetime.now().isoformat(" ", "milliseconds")
    }
    print(json.dumps(transaction, ensure_ascii=False, indent=2))
    return transaction

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record produced to {msg.topic()} partition [{msg.partition()}] @ offset {msg.offset()}")

def send_transactions(topic, count):
    for _ in range(count):
        transaction = simulate_transaction()
        try:
            publish_to_kafka(topic, json.dumps(transaction).encode('utf-8'))
            print(f"Sent: {transaction}")
        except Exception as e:
            print(f"Error producing message: {e}")
        sleep_ms = random.randint(MIN_FREQUENCY, MAX_FREQUENCY)/1000
        print(sleep_ms)
        time.sleep(sleep_ms)

# serialize object to json and publish message to kafka topic
def publish_to_kafka(topic, message):
                        
    producer = KafkaProducer(
        **configs
    )            
    producer.send(topic, value=message)
    print("Topic: {0}, Value: {1}".format(topic, message))

if __name__ == "__main__":
    KAFKA_BROKER = sys.argv[1]
    KAFKA_PORT = sys.argv[2]
    KAFKA_TOPIC = "transaction"
    MIN_FREQUENCY = 2
    MAX_FREQUENCY = 3
    COUNT = 100000000

    configs = {
        'bootstrap_servers': KAFKA_BROKER + ":" + KAFKA_PORT,
        'security_protocol': "SASL_SSL",
        'sasl_mechanism': "SCRAM-SHA-256",
        'sasl_plain_username': "superuser",
        'sasl_plain_password': "secretpassword"
    }

    send_transactions(
        topic=KAFKA_TOPIC,
        count=COUNT
    )

