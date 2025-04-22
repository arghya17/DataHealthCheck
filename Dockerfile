# Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt
# CMD gunicorn -w 4 --timeout 120 -b 0.0.0.0:5000 app:app
CMD python app.py
