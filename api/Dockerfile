FROM python:3.11

WORKDIR /api

RUN useradd -ms /bin/bash apiuser
USER apiuser

COPY pizzaApi.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "pizzaApi.py"]
