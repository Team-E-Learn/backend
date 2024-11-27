FROM python:3.12.7-alpine
COPY ./src ./src
WORKDIR ./src
CMD ["python", "./main.py"]
