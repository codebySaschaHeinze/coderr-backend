# Coderr Backend (Django REST Framework)

Backend API for the Coderr frontend (https://github.com/codebySaschaHeinze/coderr-frontend.git).  
Provides token-based authentication, user profiles, offers (with package details), orders, reviews, and aggregated platform base info.

## Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- DRF Token Authentication
- django-cors-headers
- django-filter
- Pillow (image fields)
- SQLite (dev)

## Key Concepts

- Authentication via `Authorization: Token <token>`
- Custom user model (`auth_app.User`) with role-based user types:
  - `customer`
  - `business`
- Automatic profile creation on registration (`Profile` is linked via `OneToOneField`)
- Offer structure:
  - one `Offer`
  - exactly **3** `OfferDetail` packages (`basic`, `standard`, `premium`)
- Orders are created by **customers** from an `offer_detail_id`
- Reviews are created by **customers** for **business** users (one review per customer/business pair)
- Public aggregated platform stats available via `/api/base-info/`

## API Base URL

```text
http://127.0.0.1:8000/api/
```

## Authentication

- This project uses DRF Token Authentication.

- Header format (protected endpoints)
- Authorization: Token <your_token>

## Endpoints

### Auth

#### POST /api/registration/

- Request: username, email, password, repeated_password, type (customer or business)
- Response: token, user_id, username, email
- Notes: Creates a Profile automatically. Passwords must match.

#### POST /api/login/

- Request: username, password
- Response: token, user_id, username, email

### Profiles

#### GET /api/profile/<user_id>/

- Auth required
- Read access for authenticated users

#### PATCH /api/profile/<user_id>/

- Auth required (Only profile owner)
- Supports profile fields and nested user email update

#### GET /api/profiles/business/

- Auth required
- Returns profile list for users with type='business'

#### GET /api/profiles/customer/

- Auth required
- Returns profile list for users with type='customer'

### Offers

#### GET /api/offers/

- Public offer list with filtering, search, and pagination
- Filters: creator_id, min_price, max_delivery_time

#### POST /api/offers/

- Auth required (Only business users)
- Request: title, description, image, and exactly 3 details

#### GET /api/offers/<id>/

- Auth required
- Returns offer with detail links and aggregated min values

#### PATCH /api/offers/<id>/

- Auth required (Only owner)
- Supports nested updates for the 3 packages

#### DELETE /api/offers/<id>/

- Auth required (Only owner)

### Orders

#### GET /api/orders/

- Auth required
- Returns orders where user is either customer or business provider

#### POST /api/orders/

- Auth required (Only customers)
- Request: offer_detail_id

#### PATCH /api/orders/<id>/

- Auth required (Only business users)
- Allowed field: status (in_progress, completed, cancelled)

#### GET /api/order-count/<business_user_id>/

- Auth required
- Returns count of in-progress orders

### Reviews

#### GET /api/reviews/

- Auth required
- Filtering: business_user_id, reviewer_id

#### POST /api/reviews/

- Auth required (Only customers)
- Request: business_user (ID), rating, description

#### DELETE /api/reviews/<id>/

- Auth required (Only owner)

### Base Info

#### GET /api/base-info/

- No auth required
- Response: review_count, average_rating, business_profile_count, offer_count

## Data Model (Relations)

- User has one Profile (1:1)
- Business User creates many Offers (1:n)
- Offer has exactly 3 OfferDetails (1:3)
- Customer creates many Orders (1:n)
- Business receives many Orders (1:n)
- Customer writes many Reviews (1:n)

## Project Structure

```text
coderr-backend/
├─ core/                              Django project (settings, root urls, wsgi/asgi)
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
│
├─ auth_app/                          Custom user model + auth API
│  ├─ migrations/
│  ├─ tests/
│  │  ├─ test_happy.py
│  │  └─ test_unhappy.py
│  ├─ api/
│  │  ├─ serializers.py
│  │  ├─ urls.py
│  │  ├─ validators.py
│  │  └─ views.py
│  ├─ management/
│  │  └─ commands/
│  │     └─ seed_guest_users.py       Guest demo users + profiles (custom command, if added)
│  ├─ admin.py
│  ├─ apps.py
│  └─ models.py
│
├─ profile_app/                       Profile domain (detail + customer/business lists)
│  ├─ migrations/
│  ├─ tests/
│  │  ├─ test_happy.py
│  │  └─ test_unhappy.py
│  ├─ api/
│  │  ├─ permissions.py
│  │  ├─ serializers.py
│  │  ├─ urls.py
│  │  ├─ validators.py
│  │  └─ views.py
│  ├─ admin.py
│  ├─ apps.py
│  └─ models.py
│
├─ offers_app/                        Offers + offer package details
│  ├─ migrations/
│  ├─ tests/
│  │  ├─ test_happy.py
│  │  └─ test_unhappy.py
│  ├─ api/
│  │  ├─ filters.py
│  │  ├─ pagination.py
│  │  ├─ permissions.py
│  │  ├─ serializers.py
│  │  ├─ urls.py
│  │  ├─ validators.py
│  │  └─ views.py
│  ├─ admin.py
│  ├─ apps.py
│  └─ models.py
│
├─ orders_app/                        Orders domain
│  ├─ migrations/
│  ├─ tests/
│  │  ├─ test_happy.py
│  │  └─ test_unhappy.py
│  ├─ api/
│  │  ├─ permissions.py
│  │  ├─ serializers.py
│  │  ├─ urls.py
│  │  ├─ validators.py
│  │  └─ views.py
│  ├─ admin.py
│  ├─ apps.py
│  └─ models.py
│
├─ reviews_app/                       Reviews domain
│  ├─ migrations/
│  ├─ tests/
│  │  ├─ test_happy.py
│  │  └─ test_unhappy.py
│  ├─ api/
│  │  ├─ filters.py
│  │  ├─ permissions.py
│  │  ├─ serializers.py
│  │  ├─ urls.py
│  │  ├─ validators.py
│  │  └─ views.py
│  ├─ admin.py
│  ├─ apps.py
│  └─ models.py
│
├─ baseinfo_app/                      Public aggregated platform data
│  ├─ migrations/
│  ├─ tests/
│  │  └─ test_happy.py
│  ├─ api/
│  │  ├─ urls.py
│  │  └─ views.py
│  ├─ admin.py
│  ├─ apps.py
│  └─ models.py
│
├─ .env.template
├─ .gitignore
├─ manage.py
├─ README.md
└─ requirements.txt
```

## Setup (Local Development)

### 1) Create and activate venv

Windows (PowerShell):

```text
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```text
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```text
pip install -r requirements.txt
```

If requirements.txt is not yet present:

```text
pip install django djangorestframework django-cors-headers
pip install python-dotenv
pip freeze > requirements.txt
```

### 3) Environment variables

Create a .env file (use .env.template as reference)

The project loads .env via python-dotenv in core/settings.py

SECRET_KEY='add_your_secret_key_here'

##### Optional:

DEBUG=1

### 4) Run migrations

```text
python manage.py migrate
```

### 5) Create guest users (customer and business)

```text
python manage.py seed_guest_user
```

### 6) Start server

```text
python manage.py runserver
```

##### API will be available at:

http://127.0.0.1:8000/api/

##### Authentication Header (Example)

For all protected endpoints send:

Authorization: Token <your_token>

##### Notes

This project is intended for local development and learning.

Do not use the Django development server in production.

For production, use a proper WSGI/ASGI server and a production database.

##### License

Educational / internal project (adjust as needed).
