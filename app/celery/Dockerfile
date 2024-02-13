FROM python:3.9-slim

COPY ./celery_requirements.txt requirements.txt
RUN pip3 install --upgrade pip -r requirements.txt

CMD ["celery", "--broker=amqp://guest:guest@rabbitmq:5672/", "flower"]