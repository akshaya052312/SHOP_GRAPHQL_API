# Django + Graphene GraphQL CRUD API for Shop Model

A comprehensive GraphQL API built with Django and Graphene for managing shop data with complete CRUD operations.

## Overview

This project implements a GraphQL API for a Shop model that supports creating, reading, updating, and deleting shop information. Each shop can have multiple associated email addresses and phone numbers stored in related models.

## Prerequisites

- Python 3.10+
- pip (Python package manager)

## Tech Stack

- **Django 4.2**: Web framework
- **Graphene-Django 3.2.2**: GraphQL library for Django
- **django-cors-headers 4.3.1**: CORS support for cross-origin requests

## Setup Instructions

### 1. Clone or Extract the Project
```bash
cd shop_graphql_api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **On Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
  
- **On Windows (CMD):**
  ```cmd
  venv\Scripts\activate
  ```

- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

The GraphQL endpoint will be available at: **http://127.0.0.1:8000/graphql/**

Open this URL in your browser to access the GraphiQL interactive interface.

## Project Structure

```
shop_graphql_api/
├── core/
│   ├── __pycache__/
│   ├── settings.py           # Django settings with GraphQL config
│   ├── urls.py              # URL routing with GraphQL endpoint
│   ├── asgi.py              # ASGI configuration
│   ├── wsgi.py              # WSGI configuration
│   └── schema.py            # Root GraphQL schema
├── shop/
│   ├── migrations/          # Database migrations
│   ├── __pycache__/
│   ├── admin.py             # Django admin registration
│   ├── apps.py              # App configuration
│   ├── models.py            # Shop, ShopEmail, ShopPhone models
│   ├── schema.py            # GraphQL types and mutations
│   ├── tests.py             # Unit tests
│   └── views.py             # Views (minimal for GraphQL-only project)
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database (created after migrations)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Models

### Shop
- `id` (Integer, Primary Key)
- `name` (CharField, max_length=255)
- `address` (TextField)

### ShopEmail (Related to Shop)
- `id` (Integer, Primary Key)
- `shop` (ForeignKey → Shop with related_name='emails')
- `email` (EmailField)

### ShopPhone (Related to Shop)
- `id` (Integer, Primary Key)
- `shop` (ForeignKey → Shop with related_name='phones')
- `phone` (CharField, max_length=20)

## GraphQL API Examples

### 1. CREATE - Add a New Shop

```graphql
mutation {
  createShop(
    name: "FreshMart",
    address: "Hyderabad, Telangana",
    emails: ["fresh@mart.com", "support@freshmart.com"],
    phones: ["9999999999", "8888888888"]
  ) {
    shop {
      id
      name
      address
      emails { id email }
      phones { id phone }
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "createShop": {
      "shop": {
        "id": "1",
        "name": "FreshMart",
        "address": "Hyderabad, Telangana",
        "emails": [
          {"id": "1", "email": "fresh@mart.com"},
          {"id": "2", "email": "support@freshmart.com"}
        ],
        "phones": [
          {"id": "1", "phone": "9999999999"},
          {"id": "2", "phone": "8888888888"}
        ]
      }
    }
  }
}
```

### 2. READ ALL - Get All Shops

```graphql
query {
  allShops {
    id
    name
    address
    emails { email }
    phones { phone }
  }
}
```

**Response:**
```json
{
  "data": {
    "allShops": [
      {
        "id": "1",
        "name": "FreshMart",
        "address": "Hyderabad, Telangana",
        "emails": [
          {"email": "fresh@mart.com"},
          {"email": "support@freshmart.com"}
        ],
        "phones": [
          {"phone": "9999999999"},
          {"phone": "8888888888"}
        ]
      }
    ]
  }
}
```

### 3. READ ONE - Get a Specific Shop

```graphql
query {
  shop(id: 1) {
    id
    name
    address
    emails { email }
    phones { phone }
  }
}
```

**Response:**
```json
{
  "data": {
    "shop": {
      "id": "1",
      "name": "FreshMart",
      "address": "Hyderabad, Telangana",
      "emails": [
        {"email": "fresh@mart.com"},
        {"email": "support@freshmart.com"}
      ],
      "phones": [
        {"phone": "9999999999"},
        {"phone": "8888888888"}
      ]
    }
  }
}
```

### 4. UPDATE - Modify Shop Information

```graphql
mutation {
  updateShop(
    id: 1,
    name: "FreshMart Updated",
    emails: ["new@freshmart.com"],
    phones: ["7777777777"]
  ) {
    shop {
      id
      name
      address
      emails { email }
      phones { phone }
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "updateShop": {
      "shop": {
        "id": "1",
        "name": "FreshMart Updated",
        "address": "Hyderabad, Telangana",
        "emails": [
          {"email": "new@freshmart.com"}
        ],
        "phones": [
          {"phone": "7777777777"}
        ]
      }
    }
  }
}
```

### 5. DELETE - Remove a Shop

```graphql
mutation {
  deleteShop(id: 1) {
    ok
  }
}
```

**Response:**
```json
{
  "data": {
    "deleteShop": {
      "ok": true
    }
  }
}
```

## Testing

A test script is included to verify all CRUD operations:

```bash
python test_graphql.py
```

This script performs:
1. CREATE - Creates a new shop with emails and phones
2. READ ALL - Fetches all shops
3. READ ONE - Fetches a specific shop by ID
4. UPDATE - Updates shop information
5. DELETE - Removes the shop

## Configuration Files

### settings.py
- Added `graphene_django`, `corsheaders`, and `shop` to INSTALLED_APPS
- Added `corsheaders.middleware.CorsMiddleware` to MIDDLEWARE
- Configured GRAPHENE to use `core.schema.schema`
- Enabled CORS for all origins (development only)

### urls.py
- Configured GraphQL endpoint at `/graphql/`
- Enabled GraphiQL interactive interface
- Disabled CSRF protection for GraphQL endpoint (can be re-enabled in production)

### Environment Variables (.env)

For development, you can create a `.env` file in the project root to manage environment variables:

```bash
# .env (Example)

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database (PostgreSQL - uncomment for production)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=shop_graphql_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
# CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# GraphQL
GRAPHENE_SCHEMA=core.schema.schema

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# API Keys (if needed)
API_KEY=your-api-key-here
```

**Note:** Install `python-decouple` to load .env variables in your Django settings:
```bash
pip install python-decouple
```

Then in `settings.py`:
```python
from decouple import config

DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='your-default-secret-key')
```

## Usage Notes

### Optional Arguments in Mutations
- In `createShop`: `emails` and `phones` lists are optional
- In `updateShop`: All arguments except `id` are optional
- Only provided fields will be updated (partial updates supported)

### Email and Phone Updates
- When updating `emails` or `phones`, all existing values are replaced
- Provide an empty list `[]` to remove all emails/phones

## Django Admin

Access the Django admin interface at: **http://127.0.0.1:8000/admin/**

Default credentials need to be set up by running:
```bash
python manage.py createsuperuser
```

From the admin, you can:
- View, create, edit, and delete shops
- Manage associated emails and phones
- Monitor data changes

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set secure values for `SECRET_KEY`
5. Enable HTTPS and use secure cookies
6. Update CORS settings to specific origins
7. Use a production WSGI server (Gunicorn, uWSGI, etc.)

## Troubleshooting

**Port 8000 already in use:**
```bash
python manage.py runserver 8001
```

**Database errors after model changes:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**GraphQL schema not updating:**
- Restart the development server
- Clear browser cache

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions about this GraphQL API project, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Graphene Documentation](https://docs.graphene-python.org/)
- [GraphQL Documentation](https://graphql.org/learn/)
