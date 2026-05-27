# Travel Planner API

A backend RESTful API for managing travel projects and places to visit. Built with FastAPI, SQLAlchemy, and JWT authentication. The system integrates with the Art Institute of Chicago API for validating external places.

---

## 🚀 Features

- JWT authentication (login system)
- Travel projects CRUD
- Project places management (add, update, mark as visited)
- Notes per place
- External API validation (Art Institute of Chicago)
- Pagination & filtering
- Caching layer for external API
- Database persistence (SQLite by default)
- Dockerized setup
- Seed script for admin user
- Auto-generated Swagger documentation

---

## 📦 Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Passlib (Argon2 password hashing)
- Python-JOSE (JWT auth)
- Docker / Docker Compose

---

## ⚙️ Project Structure

```
app/
 ├── core/
 ├── models/
 ├── routers/
 ├── services/
 ├── database.py
 ├── main.py
 ├── seed.py
```

## 📚 API Documentation

After running the server, Swagger documentation is available:

```
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```
http://127.0.0.1:8000/openapi.json
```

## 📌 Main Endpoints

### Auth

* POST `/auth/login`

### Projects

* POST `/projects/` — create project
* GET `/projects/` — list projects
* GET `/projects/{project_id}` — get project
* PUT `/projects/{project_id}` — update project
* DELETE `/projects/{project_id}` — delete project

### Places

* POST `/projects/{project_id}/places/` — add place
* GET `/projects/{project_id}/places/` — list places
* GET `/projects/{project_id}/places/{place_id}` — get place
* PUT `/projects/{project_id}/places/{place_id}` — update notes / visited
* DELETE `/projects/{project_id}/places/{place_id}` — remove place

---

## 🐳 Run with Docker

### Build and run:

```bash
docker-compose up --build
```

### API will be available at:

```
http://127.0.0.1:8000
```

---

## 📌 Seed User

To create an initial admin user:

### Environment variables (.env)

```
USERNAME=admin
PASSWORD=admin123
SECRET_KEY=supersecretkey
```

### Run seed script:

```bash
python -m app.seed
```

---

## 🔐 Authentication

The API uses JWT authentication.

### Login endpoint:
```

POST /auth/login

````

Request:
```json
{
  "username": "admin",
  "password": "admin123"
}
````

Response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

Use token in headers:

```
Authorization: Bearer <token>
```

---

## 🌍 External API

This project uses:

**Art Institute of Chicago API**
[https://api.artic.edu/docs/](https://api.artic.edu/docs/)

Used for validating and fetching artwork (places).

---

## 🧠 Notes

* Maximum 10 places per project
* A project is marked as completed when all places are visited
* A project cannot be deleted if it contains visited places
* External place is validated before insertion
