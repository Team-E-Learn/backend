# TODO TEST THIS FILE

FROM python:3.13.1-alpine

# Install PostgreSQL client
RUN apk add --no-cache postgresql-client

# Run PostgreSQL database and user
RUN mkdir /var/lib/postgresql/data

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
CMD ["sh", "-c", "pg_ctl -D /var/lib/postgresql/data start & python ./main.py"]