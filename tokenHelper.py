import jwt

SERVICE_SECRET_KEY = "2oecR4tYj7WZ5gAeXnD9pHmTbVq1sKfE"

def generate_service_token():
    payload = {
        "service_id": "pizza-api",
        "permissions": ["POST", "GET"],
    }
    token = jwt.encode(payload, SERVICE_SECRET_KEY, algorithm="HS256")
    return token

# Generate and print the token
token = generate_service_token()
print(token)