import pika
import logging
import json
import os
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "rabbitmq-service")
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb-service')
client = MongoClient(MONGO_URL)
db = client['pizza_db']
orders_collection = db['orders']

def process_order(order_message):

    try:
        pizza_type = order_message['pizza-type']
        size = order_message['size']
        amount = order_message['amount']
        logger.info(f"Processing order: {pizza_type} - {size} - {amount}")

        # Connect to MongoDB
        client = MongoClient(MONGO_URL)
        db = client.pizza_orders_db
        collection = db.orders

        # Insert the order into the MongoDB collection
        order_data = {
            "pizza_type": pizza_type,
            "size": size,
            "amount": amount
        }
        result = collection.insert_one(order_data)
        logger.info(f"Order inserted into MongoDB with ID: {result.inserted_id}")

    except Exception as e:
        logger.error(f"Failed to process order: {e}")
        raise

def callback(ch, method, properties, body):
    try:
        order_message = json.loads(body)
        process_order(order_message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        #TODO dead-letter queue

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue='pizza_orders')

    channel.basic_consume(queue='pizza_orders', on_message_callback=callback)

    logger.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()