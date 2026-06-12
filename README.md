# 📦  Order API

A Django REST Framework backend for managing warehouse products, inventory, and customer orders with stock validation, authentication, and order management.

---

## 🚀 Features

- User registration & JWT authentication
- Product management (staff only)
- Inventory tracking with stock safety
- Order creation with atomic stock deduction
- Order cancellation with stock restoration
- Role-based permissions (customer & staff)
- Product search & filtering
- Historical pricing in orders
- SQLite database (no external DB required)

---

## 🛠 Tech Stack

- Django
- Django REST Framework
- SQLite
- SimpleJWT Authentication

---

## 📥 Installation

### 1. Clone the project

```bash
git clone <repository-url>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver