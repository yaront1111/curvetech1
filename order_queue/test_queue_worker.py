import unittest
import json
from unittest.mock import patch, MagicMock
from order_queue.queue_worker import process_order, callback


class TestQueueWorker(unittest.TestCase):

    @patch('order_queue.queue_worker.orders_collection')
    def test_process_order_valid(self, mock_orders_collection):
        mock_insert_one = MagicMock()
        mock_orders_collection.insert_one = mock_insert_one

        order_message = {'pizza-type': 'margherita', 'size': 'personal', 'amount': 2}
        process_order(order_message)

        # Verify that insert_one was called with the expected data
        order_data = {"pizza_type": order_message['pizza-type'], "size": order_message['size'], "amount": order_message['amount']}
        mock_insert_one.assert_called_once_with(order_data)

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
