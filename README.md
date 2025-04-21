# Local Business Network

A web platform built with Django that connects users to local businesses. It includes business profiles, reviews, messaging, analytics, and real-time chat support.

---

## 🚀 Features

- Business profile creation & management  
- User authentication (Email + Google OAuth)  
- Ratings and Reviews  
- Analytics Dashboard (views, clicks, engagement)  
- Image uploads for businesses  
- Business listings with search and filters  

---

## 🧰 Tech Stack

| Layer      | Tech                               |
|------------|------------------------------------|
| Backend    | Django 4.1                          |
| Auth       | Django Allauth, Google OAuth2       |
| Database   | PostgreSQL                          |
| Frontend   | Django Templates (HTML, CSS, JS)    |
| Extras     | Pillow, psycopg2, django-extensions |

---

## ✅ Requirements

- Python 3.8+
- PostgreSQL
- Git
- pip + virtualenv

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mokinsi/local_business_network.git
cd local_business_network

STEP 2
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

CREATE DATABASE local_business_db;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'local_business_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


python manage.py makemigrations
python manage.py migrate

🗄️ Database Recreation Code
To reinitialize the database (for development):


python manage.py flush
python manage.py migrate