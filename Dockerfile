FROM python:3.13.1-alpine
COPY ./src ./src
WORKDIR ./src
CMD ["python", "./main.py"]
