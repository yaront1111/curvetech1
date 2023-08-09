import unittest
from unittest.mock import patch
from api.pizzaApi import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

    @patch('api.pizzaApi.check_database_connection', return_value="OK")
    @patch('api.pizzaApi.check_message_queue', return_value="OK")
    def test_health(self, mock_check_db, mock_check_queue):
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'OK', 'database': 'OK', 'queue': 'OK'})

    @patch('api.pizzaApi.verify_service_token', return_value=False)
    def test_order_unauthorized(self, mock_check_auth):
        response = self.app.post("/order", json={})
        self.assertEqual(response.status_code, 401)

    @patch('api.pizzaApi.verify_service_token', return_value=True)
    @patch('api.pizzaApi.add_order_to_queue')
    def test_order_authorized_valid(self, mock_add_order, mock_check_auth):
        response = self.app.post(
            "/order",
            json={"pizza-type": "margherita", "size": "personal", "amount": 1},
            headers={"Authorization": "Bearer mock"}
        )
        self.assertEqual(response.status_code, 200)

    @patch('api.pizzaApi.verify_service_token', return_value=True)
    def test_order_invalid_pizza_type(self, mock_check_auth):
        response = self.app.post(
            "/order",
            json={"pizza-type": "invalid_type", "size": "personal", "amount": 1},
            headers={"Authorization": "Bearer mock"}
        )
        self.assertEqual(response.status_code, 400)

    @patch('api.pizzaApi.verify_service_token', return_value=True)
    def test_order_invalid_size(self, mock_check_auth):
        response = self.app.post(
            "/order",
            json={"pizza-type": "margherita", "size": "invalid_size", "amount": 1},
            headers={"Authorization": "Bearer mock"}
        )
        self.assertEqual(response.status_code, 400)

    @patch('api.pizzaApi.verify_service_token', return_value=True)
    def test_order_invalid_amount(self, mock_check_auth):
        response = self.app.post(
            "/order",
            json={"pizza-type": "margherita", "size": "personal", "amount": 0},
            headers={"Authorization": "Bearer mock"}
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
