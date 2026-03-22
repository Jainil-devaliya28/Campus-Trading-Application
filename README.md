# CampusTrade — Setup Guide

## Prerequisites
- Python 3.10+
- MySQL 8.0+ (running locally or remote)

---

## 1. Clone / extract the project

```
campus_trading/
├── app.py
├── seed_admin.py
├── schema.sql
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py
    ├── config.py
    ├── models.py
    ├── helpers.py
    ├── routes/
    │   ├── auth.py
    │   ├── main.py
    │   ├── products.py
    │   ├── chat.py
    │   ├── demands.py
    │   └── admin.py
    ├── templates/
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   ├── marketplace.html
    │   ├── add_product.html
    │   ├── product_detail.html
    │   ├── profile.html
    │   ├── edit_profile.html
    │   ├── chat.html
    │   ├── demands.html
    │   ├── add_demand.html
    │   ├── feedback.html
    │   ├── admin_dashboard.html
    │   ├── admin_logs.html
    │   ├── admin_members.html
    │   └── admin_feedbacks.html
    └── static/
        └── css/
            └── style.css
```

---

## 2. Create the MySQL database

```sql
-- In your MySQL client:
CREATE DATABASE campus_trading CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or run the full schema:
```bash
mysql -u root -p < schema.sql
```

---

## 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your DB credentials
```

`.env` contents:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=campus_trading
SECRET_KEY=some-random-secret-key-here
```

---

## 4. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 5. Run the application

```bash
python app.py
```

Flask will auto-create all tables via `db.create_all()` on first run.

---

## 6. Seed the admin user

In a **second terminal** (while the app is running, or after stopping it):

```bash
python seed_admin.py
```

This creates:
- Email: `admin@campustrade.com`
- Password: `admin123`

> ⚠️ Change the password after first login!

---

## 7. Open the app

```
http://localhost:5000
```

---

## Feature Map

| Feature               | URL                         | Role       |
|-----------------------|-----------------------------|------------|
| Register              | /register                   | Public     |
| Login                 | /login                      | Public     |
| Dashboard             | /dashboard                  | User       |
| Marketplace           | /marketplace                | User       |
| Add Product           | /product/add                | User       |
| Product Detail        | /product/<id>               | User       |
| Buy Product           | POST /product/<id>/buy      | User       |
| Bargain               | POST /product/<id>/bargain  | User       |
| Review                | POST /product/<id>/review   | User       |
| Edit Product          | /product/<id>/edit          | Owner      |
| Delete Product        | POST /product/<id>/delete   | Owner/Admin|
| Profile / Portfolio   | /profile/<id>               | User       |
| Edit Profile          | /profile/edit               | Owner      |
| Chat Inbox            | /chat                       | User       |
| Conversation          | /chat/<partner_id>          | User       |
| Demands Board         | /demands                    | User       |
| Raise Demand          | /demands/add                | User       |
| Feedback              | /feedback                   | User       |
| Admin Dashboard       | /admin                      | Admin      |
| Admin Logs            | /admin/logs                 | Admin      |
| Admin Members         | /admin/members              | Admin      |
| Admin Feedbacks       | /admin/feedbacks            | Admin      |

---

## RBAC Summary

| Action                        | User | Admin |
|-------------------------------|------|-------|
| View marketplace              | ✅   | ✅    |
| Add/edit/delete own products  | ✅   | ✅    |
| Delete ANY product            | ❌   | ✅    |
| View system logs              | ❌   | ✅    |
| Manage member roles           | ❌   | ✅    |
| View all feedbacks            | ❌   | ✅    |
| Buy / bargain / review        | ✅   | ✅    |
| Chat / demands / feedback     | ✅   | ✅    |

---

## Troubleshooting

**MySQL connection error:**  
Check your `.env` credentials. Ensure MySQL is running and the `campus_trading` database exists.

**`ModuleNotFoundError: No module named 'app'`:**  
Run `python app.py` from the `campus_trading/` root directory (where `app.py` lives).

**Tables not created:**  
The app calls `db.create_all()` on startup. Ensure DB credentials are correct and the database exists.

**Bcrypt error on Windows:**  
Run `pip install bcrypt` explicitly if Flask-Bcrypt has issues.
