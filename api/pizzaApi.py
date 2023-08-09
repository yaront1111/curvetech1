from flask import Flask, request, jsonify
import pika
import jwt
from pymongo import MongoClient
from jwt.exceptions import InvalidTokenError
import os


# Configuration
class Config:
    SERVICE_SECRET_KEY = os.environ.get("SERVICE_SECRET_KEY")
    MONGO_USERNAME = os.environ.get('MONGODB_USERNAME', 'user')
    MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD', 'password')
    MONGO_URL = (
        f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}'
        '@pizza-ordering-mongodb:27017/pizza_db'
    )
    RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USERNAME", "user")
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "password")


# Application setup
app = Flask(__name__)
app.config.from_object(Config)


# Database and queue utilities
def check_database_connection():
    try:
        client = MongoClient(app.config['MONGO_URL'])
        client.admin.command("ismaster")
        return "OK"
    except Exception as e:
        app.logger.error(f"Database check failed: {e}")
        return "ERROR"


def check_message_queue():
    try:
        creds = pika.PlainCredentials(app.config['RABBITMQ_USERNAME'],
                                      app.config['RABBITMQ_PASSWORD'])
        connection_params = pika.ConnectionParameters(
            app.config['RABBITMQ_URL'], credentials=creds
        )
        connection = pika.BlockingConnection(connection_params)
        connection.close()
        return "OK"
    except Exception as e:
        app.logger.error(f"Message queue check failed: {e}")
        return "ERROR"


# Token and order utilities
def verify_service_token(token):
    try:
        jwt.decode(token, app.config['SERVICE_SECRET_KEY'], algorithms=["HS256"])
        return True
    except InvalidTokenError:
        return False


def add_order_to_queue(order):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=app.config['RABBITMQ_URL'])
    )
    channel = connection.channel()
    channel.queue_declare(queue='pizza_orders')
    channel.basic_publish(
        exchange='', routing_key='pizza_orders', body=str(order)
    )
    connection.close()


# Routes
@app.route("/health", methods=["GET"])
def health():
    db_status = check_database_connection()
    queue_status = check_message_queue()
    overall_status = "OK" if db_status and queue_status else "ERROR"
    return jsonify(status=overall_status, database=db_status, queue=queue_status), 200


@app.route("/order", methods=["POST"])
def order():
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, debug=True)

    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if auth_header else None

        if not verify_service_token(token):
            return jsonify(error="Unauthorized"), 401

        data = request.json
        pizza_type = data.get("pizza-type")
        size = data.get("size")
        amount = data.get("amount")

        allowed_pizza_types = ["margherita", "pugliese", "marinara"]
        allowed_sizes = ["personal", "family"]

        if (
            not all([pizza_type, size, amount])
            or pizza_type not in allowed_pizza_types
            or size not in allowed_sizes
            or amount < 1
        ):
            return jsonify(error="Invalid input"), 400

        order_details = {
            "pizza_type": pizza_type,
            "size": size,
            "amount": amount
        }
        add_order_to_queue(order_details)

        return jsonify(status="Order received"), 200
    except Exception as e:
        app.logger.error(f"Order processing failed: {e}")
        return jsonify(error="Internal server error"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
