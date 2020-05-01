FROM python:3.6.9-slim-stretch
COPY requirements.txt .
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY src/ .
RUN mkdir /app/model /app/logs
CMD ["python","wsgi.py"]