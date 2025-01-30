FROM python:3.13.1-alpine

# Expose the port for the Python application
EXPOSE 5000

# Copy project files
COPY ./src ./src
COPY ./requirements.txt ./src/requirements.txt

# Set working directory
WORKDIR ./src

# Install dependencies
RUN pip install -r requirements.txt

# Start PostgreSQL and the Python application
CMD ["python", "./main.py"]
