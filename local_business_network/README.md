#  Local Business Network

A full-featured web platform built with Django that connects users to local businesses. It includes business profiles, reviews, messaging, analytics, and real-time chat powered by Django Channels and Redis.

## Features

- Business profile creation & management
- User registration (email + Google OAuth)
- Real-time chat system (Channels + WebSockets)
- Analytics dashboard (views, clicks, engagement)
- Rating and reviews system (1 to 5 stars)
- Media/image upload support
- Dynamic business listing and details view

---

## 🧱 Tech Stack

| Layer            | Technology                          |
|------------------|--------------------------------------|
| Backend          | Django 4.1                           |
| Auth             | Django Allauth + Google OAuth        |
| Real-time        | Django Channels + Redis              |
| Database         | PostgreSQL                           |
| Web Server       | Daphne (ASGI)                        |
| Templating       | Django Templates                     |
| Extra Packages   | `django-extensions`, `psycopg2`      |

---

## System Requirements

- Python 3.8+
- PostgreSQL
- Redis (for real-time communication)
- pip / virtualenv (for dependency management)

---

## ⚙️ Installation Guide

### 1. Clone the Project

```bash
git clone https://github.com/yourusername/local_business_network.git
cd local_business_network
