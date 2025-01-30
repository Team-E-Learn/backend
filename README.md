# Backend

This will be the repo for the backend of the project, focusing on the API calls in python and the database.

## Usage

### Backend

```bash
python main.py
```

OR 

```bash
docker build -t build-name .
docker run -p 5000:5000 build-name
```

### Database

#### Starting
```bash
docker-compose up -d
```

Postgres: localhost:5432
Adminer WebUI: localhost:8989


#### Shutting Down
```bash
docker-compose down
```
