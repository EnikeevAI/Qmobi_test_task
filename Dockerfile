
FROM python:3.8-alpine
COPY . /opt/app
WORKDIR /opt/app
CMD ["python", "./app.py"]