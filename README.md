
# Learn Background Processing with Python & RabbitMQ

Background Processing With RabbitMQ, Python, and Flask - Here we are using a simple Flask Webpage that has form to add a username and it submits it to a Queue and the worker(s) processes them wither DB or kust stdout.

To enhance the performance of your web application, we run background processes and create a microservice & containerized enviornment.

It's quite common practise to use background processing to enhance the responsiveness and performance of your online apps. Having precise control over the background activities is challenging. You should run how many? Can they be scaled up or down?

We will employ the following for this:
- Docker makes it easier for programmers to create portable and lightweight software containers that streamline the creation, testing, and deployment of applications. 
- A prominent asynchronous message broker that can manage millions of messages is RabbitMQ.
- Flask Server acting as a Producer and linking RabbitMQ with Pika
- RabbitMQ connection using Pika and Python script as a worker


## Dependency

- Java
- Install [docker](https://www.docker.com/products/docker-desktop/) 
- VsCode or any editor

    
## Deployment & Run

To deploy this project run

```bash
#Build all containers
docker-compose build
or 
docker-compose build web
docker-compose build worker
docker-compose build rabbitmq


#Run container and scale worker to 5 instances
docker-compose up --remove-orphans -d
or
docker-compose up rabbitmq --remove-orphans -d
docker-compose up web --remove-orphans -d
docker-compose up worker--scale worker=5 --remove-orphans -d


# Stop and Clean 
docker-compose down 
or
docker-compose stop web
docker-compose stop worker
docker-compose stop rabbitmq
```


## API Reference

#### Add User

```http
  POST http://127.0.0.1:5000/login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | Pat Quigley |


## Demo

Screenshots

## Docker Containers Running
![Docker Containers Running](https://github.com/austinnoronha/UI-References-and-Screenshots/blob/421ac5b7dbeead5900a675dd8f1945176e5dac4b/common-images/demo%20-%20bg%20-%20docker%201.jpg)


## Test Run using Postman
![Docker Containers Running](https://github.com/austinnoronha/UI-References-and-Screenshots/blob/421ac5b7dbeead5900a675dd8f1945176e5dac4b/common-images/demo%20-%20bg%20-%20postman%201.jpg)


## RabbitMQ Queue
![RabbitMQ Queue](https://github.com/austinnoronha/UI-References-and-Screenshots/blob/421ac5b7dbeead5900a675dd8f1945176e5dac4b/common-images/demo%20-%20bg%20-%20rabbitmq%201%20-%205%20consumers.jpg)

## Environment Variables

To run this project, you will need to add the following environment variables to your `docker-compose.yaml`

```bash
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_PORT=5672

```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Roadmap

- Support for MongoDB with a Model

- Support for a task Manager using Celery


## Tech Stack

**Client:** Bootstrap

**Server:** Flask Python

**Queue:** RabbitMq

**Containerization:** Docker - docker compose
