### “BUSINESS FINDER: A COMPREHENSIVE SERVICE DISCOVERY PLATFORM FOR ENHANCED BUSINESS EXPOSURE AND CONSUMER    ENGAGEMENT”

A web platform built with Django that connects users to local businesses. It includes business profiles, reviews, messaging, analytics, and real-time chat support.

---

##  Features

- Business profile creation & management
- User authentication (Email + Google OAuth)
- Ratings and Reviews
- Analytics Dashboard (views, clicks, engagement)
- Image uploads for businesses
- Business listings with search and filters

---

##  Tech Stack

| Layer      | Tech                               |
|------------|------------------------------------|
| Backend    | Django 4.1                          |
| Auth       | Django Allauth, Google OAuth2       |
| Database   | PostgreSQL                          |
| Frontend   | Django Templates (HTML, CSS, JS)    |
| Extras     | Pillow, psycopg2, django-extensions |

---

##  Requirements

- Python 3.8+
- PostgreSQL
- pip + virtualenv (for managing Python dependencies)
- PostgreSQL installed on your local machine

---

##  Setup Instructions

### 1. Download the Project Files
download the project files from cd, and extract them to your desired location on your computer.

### 2. Create a Virtual Environment
Once you have the project files extracted, you need to create a virtual environment to isolate your Python dependencies. This ensures that the required packages do not conflict with other projects or system-wide Python installations.
### on windows
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
Once the virtual environment is activated, install all required Python packages by running:

pip install -r requirements.txt
This will install all dependencies listed in the requirements.txt file.

4. Setup PostgreSQL Database
Create a PostgreSQL database and configure it in your Django settings.py file.

### Create the Database
In PostgreSQL, run the following command to create the database:

CREATE DATABASE local_business_db;
Update Database Configuration

Go to the settings.py file located in the project folder. In the DATABASES section, update it with your PostgreSQL credentials:


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'local_business_db',
        'USER': 'your_db_user',       ### Replace with your PostgreSQL username
        'PASSWORD': 'your_db_password',  # Replace with your PostgreSQL password
        'HOST': 'localhost',          # Use 'localhost' if running the DB locally
        'PORT': '5432',               # Default PostgreSQL port
    }
}
5. Apply Migrations
After configuring the database, run the migrations to create the necessary database tables:

python manage.py makemigrations
python manage.py migrate

This will create the required database tables for your Django application.

🗄️ Database Recreation Code
If you need to reset the database or start over, you can use the following commands to flush the existing data and recreate the database schema.

### Flush the Database
To delete all data in your database:

python manage.py flush
This will prompt you to confirm that you want to delete all data from the database.

### Recreate the Database Schema
To reapply the migrations (i.e., recreate the database schema):

python manage.py migrate
This will apply any pending migrations and recreate the database structure.

### Running the Project
Once everything is set up, you can run the Django development server:

python manage.py runserver
This will start the server at http://127.0.0.1:8000/ on your local machine. You can open this URL in your browser to view the project.

### Notes
This project uses PostgreSQL as the database, so ensure that PostgreSQL is installed and running before starting the setup.

Make sure that the appropriate database credentials are set in the settings.py file.

If you encounter any issues with migrations or database setup, check that PostgreSQL is running and that your database credentials are correct.

If you do not have PostgreSQL installed, follow the PostgreSQL installation guide for your operating system.