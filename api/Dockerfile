FROM python:3.11

WORKDIR /api

RUN apiuser -ms /bin/bash myuser
USER apiuser

COPY pizzaApi.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV RABBITMQ_URL=rabbitmq-service

CMD ["python", "pizzaApi.py"]
