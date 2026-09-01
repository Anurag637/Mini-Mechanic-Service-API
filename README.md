# Mini Mechanic Service API

A Django REST API for managing mechanics and handling service requests for a mechanic service platform.

## Features
- List, create, update, and delete mechanics
- Fetch a single mechanic by ID
- Create and track service requests with default status `PENDING`
- Validation for phone numbers, vehicle numbers, missing required fields, invalid services, and invalid mechanic IDs
- Pagination and basic search/filter support
- OpenAPI schema and Swagger UI via `drf-spectacular`
- Token-based authentication for write operations
- SQLite for local runs and PostgreSQL-ready configuration
- Structured logging to console and file
- Docker support for quick local deployment

## Tech Stack
- Python 3.10+
- Django 5.2
- Django REST Framework 3.18
- drf-spectacular 0.30
- SQLite

## Project Structure
- `mechanic_service_platform/` — Django project configuration
- `mechanics/` — models, serializers, views, and API routes
- `db.sqlite3` — local SQLite database
- `requirements.txt` — Python dependencies

## Setup Instructions

1. Clone the project and navigate to the root folder.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

6. Open the API docs in the browser:

```text
http://127.0.0.1:8000/api/docs/
```

### Token Authentication

Create a user and get a token:

```http
POST /api/register/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

Then use the token in the Authorization header:

```http
Authorization: Token <your-token>
```

### PostgreSQL Configuration

Set the environment variables before running with PostgreSQL:

```bash
set POSTGRES_DB=mechanic_db
set POSTGRES_USER=mechanic_user
set POSTGRES_PASSWORD=mechanic_pass
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432
python manage.py migrate
```

### Docker

```bash
docker-compose up --build
```

Then open:

```text
http://localhost:8000/api/docs/
```

## Available Endpoints

### Mechanics
- `GET /api/mechanics/` — list mechanics
- `GET /api/mechanics/<id>/` — fetch mechanic by ID
- `POST /api/mechanics/` — create mechanic
- `PUT /api/mechanics/<id>/` — replace mechanic
- `PATCH /api/mechanics/<id>/` — update mechanic
- `DELETE /api/mechanics/<id>/` — delete mechanic

### Service Requests
- `GET /api/service-requests/` — list service requests
- `POST /api/service-requests/` — create service request

### API Schema
- `GET /api/schema/` — OpenAPI schema
- `GET /api/docs/` — Swagger UI

## Search and Filter Examples

```text
GET /api/mechanics/?search=bangalore
GET /api/mechanics/?location=Hyderabad
GET /api/mechanics/?is_open=true
```

## Sample Request / Response

Create a mechanic:

```http
POST /api/mechanics/
Content-Type: application/json

{
  "name": "Amit Kumar",
  "phone": "+919876543210",
  "location": "Bengaluru",
  "rating": 4.8,
  "is_open": true,
  "services": ["oil change", "brake service"]
}
```

Response:

```json
{
  "id": 1,
  "name": "Amit Kumar",
  "phone": "+919876543210",
  "location": "Bengaluru",
  "rating": 4.8,
  "is_open": true,
  "services": ["oil change", "brake service"]
}
```

Create a service request:

```http
POST /api/service-requests/
Content-Type: application/json

{
  "customer_name": "Neha Sharma",
  "customer_phone": "+919900001122",
  "vehicle_number": "MH12AB1234",
  "mechanic_id": 1,
  "service": "oil change",
  "problem_description": "Engine makes a noisy sound."
}
```

Response:

```json
{
  "id": 1,
  "customer_name": "Neha Sharma",
  "customer_phone": "+919900001122",
  "vehicle_number": "MH12AB1234",
  "mechanic_id": 1,
  "service": "oil change",
  "problem_description": "Engine makes a noisy sound.",
  "status": "PENDING",
  "created_at": "2026-09-01T12:00:00Z"
}
```

## Validation Rules
- Phone must be a valid 10-15 digit mobile number, optionally with a country code
- Vehicle number must match a common Indian format such as `MH12AB1234`
- Mechanic must exist for each service request
- Service must be one of the mechanic's listed services
- Required fields cannot be blank

## Running Tests

```bash
python manage.py test mechanics
```

## Notes
- The project uses SQLite by default for quick local development, while PostgreSQL support is enabled through environment variables.
- Logs are written to a `logs/mechanic_api.log` file and the console for debugging and monitoring.
- The API is production-aware enough to support a secure deployment path without changing the core project structure.
