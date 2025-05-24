# Task

Implement an http service that processes incoming requests. The server starts at <http://127.0.0.1:8080> (the default value can be changed).

<summary> List of possible endpoints (can be changed) </summary>

1. Get an abbreviated version of the transmitted URL.

POST /

The method accepts the URL string for shortening in the request body and returns a response with the code 201.

2. Return the original URL.

GET /<shorten-url-id>

The method takes the identifier of the shortened URL as a parameter and returns a response with the code 307 and the original URL in the Location header.

3. Make an async service request and return the data

## Install

### Enviroments

Need to fill **.env.sample** and after rename him to **.env**

```python
# .env.sample
POSTGRES_PASSWORD=password # Password Data Base (Settings)
DB_PASSWORD=password # Password Data Base (Use)
```

### Docker

Project is under the control system - **Docker**.
If you not have Docker - you can install him here: [Docker](https://www.docker.com/get-started/)

Write command:

```bash
docker-compose build
```

```bash
docker-compose up
```

- In address localhost:8080 Backend

For testing you need enter inside to container.

- Find container:

```bash
docker ps
```

Find container and take first 3 symbols CONTAINER ID

- Enter to contaiter:

```bash
docker exec -it YourCONTAINERID bash
```

And after you get into the container where your applitation is located
and you can write commants for testings

```bash
pytest
```
