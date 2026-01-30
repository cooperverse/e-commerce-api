
## E-Commerce API

***click here for 👉*** [API Documentation](https://cooperverse.github.io/e-commerce-api/)

A RESTful backend service for an E-Commerce platform, built with Django and Django REST Framework (DRF). Supports user authentication, product management, order workflows, and background tasks. Designed to be frontend-agnostic for web or mobile apps.

All endpoints, request/response examples, and authentication details are fully documented in the live API documentation linked above.
## Features

- User authentication (signup/login/logout)

- Product CRUD (create, read, update, delete)

- Order creation and tracking

- JWT-based authentication

- Background tasks with Celery + Redis

- Fully containerized with Docker


## Tech Stack
**Backend:** Python, Django, Django REST Framework

 **Database:** SQLite (default) / PostgreSQL (optional)

 **Task Queue:** Celery + Redis

 **Container:** Docker

 **Authentication:** Token / JWT

 **Documentation:** Live API Docs (GitHub Pages)
## API Documentation

All API endpoints, request/response examples, and authentication details are fully documented here:

[See Documentation](https://cooperverse.github.io/e-commerce-api/)


## Screenshots

![App Screenshot1](https://github.com/cooperverse/e-commerce-api/blob/main/media/api1.png)

![App Screenshot2](https://github.com/cooperverse/e-commerce-api/blob/main/media/api2.png)


## API Reference

#### Authentication

| Method | Endpoint     | Description                |
| :-------- | :------- | :------------------------- |
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/`    | Login & get auth token |
| `POST` | `/api/auth/logout/`   | Logout |

#### Products

| Method | Endpoint     | Description                |
| :-------- | :------- | :------------------------- |
| `GET` | `/api/products/` | List all products |
| `GET` | `/api/products/{id}/` | Retrieve product details |
| `POST`| `/api/products/`   | Create a new product (auth required) |
| `PUT/PATCH` | `/api/products/{id}/`|Update product (auth required) |
| `DELETE` | `/api/products/{id}/`| Delete product (auth required) |

#### Orders

| Method | Endpoint     | Description                |
| :-------- | :------- | :------------------------- |
| `GET` | `/api/orders/` | List user orders |
| `GET` | `/api/orders/{id}/`    | Retrieve order details |
| `POST` | `/api/orders/`   | Create a new order |


## Installation

Clone the Repository

```bash
  git clone https://github.com/cooperverse/e-commerce-api.git
cd e-commerce-api
```
Using Virtual Environment (Optional if not using Docker)

```bash
  python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```
Install Dependencies

```bash
 pip install -r requirements.txt
```
Database Migrations

```bash
  python manage.py makemigrations
python manage.py migrate
```
### Docker Setup (Recommended)
1. Build Docker image
```bash
  docker build -t e-commerce-api .

```
2. Run containers

```bash
  docker-compose up -d

```
This starts Django, Redis, and Celery workers automatically.
## Background Tasks with Celery & Redis

- Celery handles asynchronous tasks, using Redis as the broker.

- All tasks are defined in your existing `api/tasks.py` file.
### Start Redis

```bash
  docker-compose up -d redis
```
### Start Celery Worker
```lua
  celery -A config worker --loglevel=info

```

### Start Celery Beat (Optional, for scheduled tasks)
```lua
  celery -A config beat --loglevel=info

```
To trigger a task asynchronously, import it from api/tasks.py and call .delay() in your view.
## Contributing

- Fork the repository

- Create a feature branch (git checkout -b feature-name)

- Commit changes (git commit -m "Add feature")

- Push to branch (git push origin feature-name)

- Open a Pull Request


## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Authors

- [@cooperverse](https://www.github.com/cooperverse)


