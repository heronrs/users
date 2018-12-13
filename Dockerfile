FROM python:3.6.7-stretch

COPY . /app

WORKDIR /app

RUN sh -c "pip install -r requirements.txt"

RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser

USER appuser

CMD ["sh", "-c", "/usr/local/bin/gunicorn --access-logfile - -b 0.0.0.0:8000 'api:create_app()'"]

EXPOSE 8000