FROM python:3.11

WORKDIR /queue

RUN useradd -ms /bin/bash appuser
USER appuser

COPY queue_worker.py .
COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run the application
CMD ["python", "queue_worker.py"]
