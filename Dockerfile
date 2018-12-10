FROM python:3.6.7-stretch

COPY . /app
WORKDIR /app

RUN sh -c "pip install -r requirements.txt -r requirements_dev.txt"

EXPOSE 8000