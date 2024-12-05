FROM python:3.13.1-alpine
EXPOSE 5000
COPY ./src ./src
COPY ./requirements.txt ./src/requirements.txt
WORKDIR ./src
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
