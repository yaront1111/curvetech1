import unittest
import json
from unittest.mock import patch, MagicMock
from order_queue.queue_worker import process_order, callback


class TestQueueWorker(unittest.TestCase):

    @patch('order_queue.queue_worker.MongoClient')
    def test_process_order_valid(self, mock_mongo_client):
        mock_collection = MagicMock()
        mock_mongo_client.return_value.pizza_orders_db.orders = mock_collection

        order_message = {'pizza-type': 'margherita', 'size': 'personal', 'amount': 2}
        process_order(order_message)
        mock_collection.insert_one.assert_called_with({
            'pizza_type': 'margherita', 'size': 'personal', 'amount': 2})

    @patch('pymongo.MongoClient')
    def test_process_order_invalid_type(self, mock_mongo_client):
        order_message = {'pizza-type': 'margherita', 'size': 'personal', 'amount': '2'}  # Invalid type for amount
        with self.assertRaises(Exception):
            process_order(order_message)

    @patch('order_queue.queue_worker.process_order')
    def test_callback_valid_message(self, mock_process_order):
        ch, method, properties = MagicMock(), MagicMock(), MagicMock()
        body = json.dumps({'pizza-type': 'margherita', 'size': 'personal', 'amount': 2})

        callback(ch, method, properties, body)
        mock_process_order.assert_called_once()
        ch.basic_ack.assert_called_once_with(delivery_tag=method.delivery_tag)

    @patch('order_queue.queue_worker.logger')
    def test_callback_invalid_message(self, mock_logger):
        ch, method, properties = MagicMock(), MagicMock(), MagicMock()
        body = "Invalid JSON"

        callback(ch, method, properties, body)
        mock_logger.error.assert_called_with('Failed to process message: Expecting value: line 1 column 1 (char 0)')


if __name__ == '__main__':
    unittest.main()
