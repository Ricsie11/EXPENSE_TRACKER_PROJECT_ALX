# Expense Tracker (Django REST API)

A premium, modern personal expense/income tracker backend built with Django REST Framework. The API supports secure user management, JWT authentication, and comprehensive financial tracking.

## ✨ Features

- **User Authentication**: Secure signup and login using JWT (JSON Web Tokens).
- **Profile Management**: User profiles with profile picture upload support.
- **Financial Tracking**: CRUD operations for Expenses, Incomes, and user-defined Categories.
- **Dynamic Summaries**: Real-time financial overviews (Daily, Weekly, Monthly, Yearly, and Total).
- **Category Breakdown**: Detailed visualization data for spending patterns.
- **Robust API**: Enhanced error handling and data validation to prevent 500 errors.

## 🛠️ Stack & Dependencies

- **Python 3.11+**
- **Django**: Core web framework.
- **Django REST Framework**: For building the robust API.
- **SimpleJWT**: Secure authentication layer.
- **Pillow**: Image processing for profile pictures.
- **Django Filter**: For dynamic transaction filtering.
- **dj-database-url & python-decouple**: For secure environment management.

## ⚙️ Environment Variables

Create a `.env` file in the root directory (where `manage.py` is):


## 🚀 Quick Setup (Local)

1. **Clone and Setup Virtual Environment**:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Run Migrations**:

   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start the Server**:
   ```powershell
   python manage.py runserver
   ```

## 🔗 API Endpoints

The API is base-routed at `api/v1.0/`.

### Authentication & Profile

- `POST api/v1.0/signup/` — Register a new user.
- `POST api/v1.0/login/` — Standard JWT login.
- `GET api/v1.0/users/me/` — Get authenticated user details.
- `POST api/v1.0/profile/update/` — Upload/update profile picture (Multipart/Form-Data).

### Financial Records

- `GET/POST api/v1.0/expenses/` — Manage expenses.
- `GET/POST api/v1.0/incomes/` — Manage incomes.
- `GET/POST api/v1.0/categories/` — Manage custom categories.
- `GET/PUT/DELETE api/v1.0/expenses/<id>/` — Detail expense management.

### Summaries & Charts

- `GET api/v1.0/summary/` — Overall financial totals (Income/Expense/Balance).
- `GET api/v1.0/category/summary/` — Spending breakdown by category for charts.

## 🧪 Testing

Run standard Django tests:

```powershell
python manage.py test
```

## 📝 Deployment

The project is configured for deployment on **Render**. Ensure you set the `DATABASE_URL` and `SECRET_KEY` in the Render environment settings. For media files (profile pictures), a persistent disk or cloud storage (AWS S3/Cloudinary) is recommended for production.
