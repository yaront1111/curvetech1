import pika
import logging
import json
import os
from pymongo import MongoClient

# Configuration
class Config:
    RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "pizza-ordering-rabbitmq")
    RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USERNAME", "user")
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "password")
    MONGO_USERNAME = os.environ.get('MONGODB_USERNAME', 'user')
    MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD', 'password')
    MONGO_URL = (
        f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}'
        '@pizza-ordering-mongodb:27017/pizza_db'
    )


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
client = MongoClient(Config.MONGO_URL)
db = client['pizza_db']
orders_collection = db['orders']


# Order processing
def process_order(order_message):
    try:
        # Extract order details
        pizza_type = order_message['pizza-type']
        size = order_message['size']
        amount = order_message['amount']
        logger.info(f"Processing order: {pizza_type} - {size} - {amount}")

        # Insert the order into MongoDB
        order_data = {"pizza_type": pizza_type, "size": size, "amount": amount}
        result = orders_collection.insert_one(order_data)
        logger.info(f"Order inserted into MongoDB with ID: {result.inserted_id}")

    except Exception as e:
        logger.error(f"Failed to process order: {e}")
        raise


# RabbitMQ Callback
def callback(ch, method, properties, body):
    try:
        order_message = json.loads(body)
        process_order(order_message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        # TODO: dead-letter queue


# Main function
def main():
    credentials = pika.PlainCredentials(Config.RABBITMQ_USERNAME, Config.RABBITMQ_PASSWORD)
    connection_params = pika.ConnectionParameters(Config.RABBITMQ_URL, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='pizza_orders')
    channel.basic_consume(queue='pizza_orders', on_message_callback=callback)

    logger.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
