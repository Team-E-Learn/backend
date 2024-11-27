FROM python:3.12.7-alpine
ADD main.py ./
CMD ["python", "./main.py"]
