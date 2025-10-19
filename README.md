# Expense Tracker (Django REST API)

A simple personal expense/income tracker built with Django REST Framework. The API supports user registration, JWT authentication, CRUD operations for expenses, incomes and categories, and summary endpoints (total income, total expense, balance, and category breakdown).


## Features

- User registration with JWT token generation (access & refresh)
- JWT-based authentication for protected endpoints
- CRUD for Expenses, Incomes and Categories
- Summary endpoints: overall balance and category-wise breakdown
- Admin site with models registered

## Stack & Dependencies

- Python 3.11+ (project was generated with Django 5.2.6)
- Django
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- dj-database-url (used for parsing DATABASE_URL in settings)
- python-decouple (for environment config)


## Environment variables

The project expects the following environment variables (used in `settings.py` via `python-decouple`):

- SECRET_KEY — Django secret key
- DEBUG — set to `True` or `False` (default: `False`)
- DATABASE_URL — database connection URL (e.g., for Postgres on Render)

If you deploy to Render, the settings file already allows Render's domain in `CSRF_TRUSTED_ORIGINS`.

## Quick setup (local)

This project doesn't include a lockfile in the repo root, so use one of the approaches below depending on your environment.

Using pipenv (if you prefer):

```powershell
pipenv install --python 3.11 django djangorestframework djangorestframework-simplejwt django-filter python-decouple dj-database-url
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Using a virtualenv + pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install django djangorestframework djangorestframework-simplejwt django-filter python-decouple dj-database-url
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Replace the package list above with any project-specific requirements if you have a `requirements.txt` or `Pipfile` elsewhere.

## Running tests

No tests were detected in the project apart from an empty `tracker/tests.py`. Add tests under the `tracker/tests.py` or `tracker/tests/` and run:

```powershell
python manage.py test
```

## API endpoints

The application mounts the tracker API under `api/v1.0/`.

Authentication:
- POST `api/v1.0/signup/` — register a new user. Request body: {"username":"...","email":"...","password":"..."}. Returns `refresh` and `access` tokens.
- POST `api/v1.0/login/` — obtain JWT tokens (use `rest_framework_simplejwt.views.TokenObtainPairView`). Body: {"username":"...","password":"..."}
- POST `api/v1.0/token/refresh/` — refresh access token using the refresh token.

Expenses:
- GET `api/v1.0/expenses/` — list authenticated user's expenses (paginated)
- POST `api/v1.0/expenses/` — create expense ({"amount","category","description","date"})
- GET/PUT/DELETE `api/v1.0/expenses/<id>/` — retrieve, update or delete a specific expense

Incomes:
- GET `api/v1.0/incomes/` — list incomes
- POST `api/v1.0/incomes/` — create income
- GET/PUT/DELETE `api/v1.0/incomes/<id>/` — retrieve, update or delete income

Categories:
- GET `api/v1.0/categories/` — list categories
- POST `api/v1.0/categories/` — create category ({"name","type"})
- GET/PUT/DELETE `api/v1.0/categories/<id>/` — manage a category

Summaries:
- GET `api/v1.0/summary/` — returns total_income, total_expense, balance for the authenticated user
- GET `api/v1.0/category/summary/` — returns income and expense totals broken down by category

Admin:
- GET `admin/` — Django admin site (create a superuser to access)
- Utility endpoint: `api/v1.0/create-admin/` — creates a default admin user with username `admin` and password `admin123` (use carefully; consider removing in production)

## Example: Register and use access token

1. Register (curl example):

```powershell
curl -X POST "http://127.0.0.1:8000/api/v1.0/signup/" -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","password":"secretpass"}'
```

2. Use returned `access` token to call protected endpoints:

```powershell
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/api/v1.0/expenses/
```

## Notes & suggestions

- Security: The `create-admin/` view creates a default admin with a hard-coded password; remove or protect it before deploying to production.
- Add automated tests for serializers, views, and permission checks.
- Add request/response examples and a Postman or OpenAPI/Swagger spec for easier integration.

