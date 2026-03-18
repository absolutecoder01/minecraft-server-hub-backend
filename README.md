# Minecraft Server Hub - Backend

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)](https://jwt.io)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Backend for Minecraft server management platform with professional authentication, authorization, and admin dashboard.

---

## Features

### 🔐 Authentication & Authorization
- ✅ JWT tokens stored in **httpOnly cookies**
- ✅ **CSRF protection** for all POST/PUT/DELETE requests
- ✅ Password hashing with **Argon2** algorithm
- ✅ User role system (**user** / **admin**)
- ✅ `@admin_required` decorator for admin endpoints

### 🖥️ Server Management
- ✅ Full **CRUD** (Create, Read, Update, Delete)
- ✅ Permission system (owner OR admin)
- ✅ Data validation before database save
- ✅ User-Server relationships

### 📊 Admin Dashboard
- ✅ General statistics (users, servers, admins)
- ✅ User distribution by role
- ✅ Servers grouped by game mode
- ✅ SQL aggregations (COUNT, GROUP BY)

---

## Tech Stack

| Category | Technology |
| :--- | :--- |
| **Framework** | Flask 3.0+ |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Authentication** | Flask-JWT-Extended (cookies) |
| **Hashing** | Argon2 |
| **CORS** | Flask-CORS |
| **Environment** | python-dotenv |

---

## Installation

### 1. Clone Repository
`git clone https://github.com/yourusername/minecraft-server-hub-backend.git`
`cd minecraft-server-hub-backend`

### 2. Create Virtual Environment
Windows: `python -m venv venv` + `venv\Scripts\activate`
macOS/Linux: `python3 -m venv venv` + `source venv/bin/activate`

### 3. Install Dependencies
`pip install -r requirements.txt`

### 4. Configure Environment Variables
`cp .env.example .env`
Edit .env and set: `JWT_SECRET_KEY=your-very-long-and-random-secret-key`

### 5. Run Server
`python app.py`
Server will be available at: **http://127.0.0.1:5000**

---

## Configuration

### Environment Variables (.env)
| Variable | Description | Required |
| --- | --- | --- |
| JWT_SECRET_KEY | Key for signing JWT tokens | ✅ Yes |

### Flask Configuration (app.py)
| Variable | Default Value | Description |
| --- | --- | --- |
| SQLALCHEMY_DATABASE_URI | sqlite:///database.db | Database connection |
| JWT_TOKEN_LOCATION | ["cookies"] | Token storage location |
| JWT_COOKIE_SECURE | False | HTTPS only in production |
| JWT_COOKIE_CSRF_PROTECT | True | CSRF protection |
| JWT_CSRF_HEADER_NAME | X-CSRF-TOKEN | CSRF header name |

---

## 📁 Project Structure

minecraft-server-hub-backend/
├── app.py                 # Main Flask application file
├── models.py              # Database models (User, Server)
├── utils.py               # Helper functions (password hashing)
├── .env                   # Environment variables (not in git!)
├── .gitignore             # Ignored files
├── requirements.txt       # Python dependencies
└── README.md              # Documentation

---

## API Documentation

Base URL: http://localhost:5000

---

### Authentication

#### Register
POST /api/auth/register
Content-Type: application/json

Body:
{
  "username": "new_user",
  "password": "secure_password",
  "role": "user"
}

Response (201):
{
  "message": "User created successfully"
}

---

#### Login
POST /api/auth/login
Content-Type: application/json

Body:
{
  "username": "new_user",
  "password": "secure_password"
}

Response (200):
{
  "msg": "login successful"
}
Sets cookies: access_token_cookie + csrf_access_token

---

#### Logout
POST /api/auth/logout
X-CSRF-TOKEN: <csrf_token_from_cookie>

Response (200):
{
  "msg": "Logout successful"
}

---

### Server Management

#### Get All Servers
GET /api/servers
Authorization: Cookie (access_token_cookie)

Response (200):
[
  {
    "id": 1,
    "name": "My Server",
    "ip_address": "192.168.1.100",
    "version": "1.20.1",
    "game_mode": "survival",
    "image_url": "https://example.com/image.png",
    "owner_id": 1
  }
]

---

#### Get Server Details
GET /api/servers/<id>
Authorization: Cookie (access_token_cookie)

Response (200):
{
  "id": 1,
  "name": "My Server",
  "ip_address": "192.168.1.100",
  "version": "1.20.1",
  "game_mode": "survival",
  "image_url": "https://example.com/image.png",
  "owner_id": 1
}

---

#### Create Server
POST /api/servers
Content-Type: application/json
X-CSRF-TOKEN: <csrf_token_from_cookie>
Authorization: Cookie (access_token_cookie)

Body:
{
  "name": "New Server",
  "ip_address": "192.168.1.100",
  "version": "1.20.1",
  "game_mode": "survival",
  "image_url": "https://example.com/image.png"
}

Response (201):
{
  "message": "Succesfully created server!"
}

---

#### Update Server
PUT /api/servers/<id>
Content-Type: application/json
X-CSRF-TOKEN: <csrf_token_from_cookie>
Authorization: Cookie (access_token_cookie)

Body (only fields to update):
{
  "name": "Updated Name",
  "version": "1.20.4"
}

Response (200):
{
  "message": "Server updated successfully!"
}

---

#### Delete Server
DELETE /api/servers/<id>
X-CSRF-TOKEN: <csrf_token_from_cookie>
Authorization: Cookie (access_token_cookie)

Response (204): No Content

---

### Admin Dashboard

#### Get Statistics
GET /api/admin/stats
Authorization: Cookie (access_token_cookie)

Required: admin role

Response (200):
{
  "total_user_count": 50,
  "total_server_count": 40,
  "total_admin_count": 5,
  "users_by_role": {
    "user": 45,
    "admin": 5
  },
  "server_by_game_mode": {
    "survival": 15,
    "creative": 8,
    "pvp": 12
  }
}

---

## Authentication

### How JWT Works in This Project?

1. Login → Server returns token in httpOnly cookie
2. CSRF Token → Additional cookie csrf_access_token
3. Every Request → Browser automatically sends cookies
4. CSRF Header → For POST/PUT/DELETE add header X-CSRF-TOKEN

### Getting CSRF Token (JavaScript)

function getCookie(name) {
  const value = '; ' + document.cookie;
  const parts = value.split('; ' + name + '=');
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Usage in fetch
const csrfToken = getCookie('csrf_access_token');

fetch('/api/servers', {
  method: 'POST',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRF-TOKEN': csrfToken
  },
  body: JSON.stringify({...})
});

---

## Testing

### Testing in Postman

1. Login (POST /api/auth/login)
2. Copy CSRF token from cookies
3. Add header X-CSRF-TOKEN to POST/PUT/DELETE requests
4. Enable "Automatically follow redirects" and "Persist cookies"

### Endpoint Summary

| Endpoint | Method | Auth | CSRF | Status |
| --- | --- | --- | --- | --- |
| /api/auth/register | POST | ❌ | ❌ | ✅ |
| /api/auth/login | POST | ❌ | ❌ | ✅ |
| /api/auth/logout | POST | ✅ | ✅ | ✅ |
| /api/servers | GET | ✅ | ❌ | ✅ |
| /api/servers | POST | ✅ | ✅ | ✅ |
| /api/servers/<id> | PUT | ✅ | ✅ | ✅ |
| /api/servers/<id> | DELETE | ✅ | ✅ | ✅ |
| /api/admin/stats | GET | ✅ + Admin | ❌ | ✅ |

---

## Security

### Implemented Security Features

| Feature | Status | Description |
| --- | --- | --- |
| JWT Cookies | ✅ | Tokens in httpOnly cookies |
| CSRF Protection | ✅ | CSRF token validation |
| Password Hashing | ✅ | Argon2 (most secure) |
| SQL Injection | ✅ | SQLAlchemy ORM |
| CORS | ✅ | Configurable origins |
| Role-Based Access | ✅ | User / Admin |

### Production Recommendations

Before deploy, change in app.py:
- JWT_COOKIE_SECURE = True (HTTPS only)
- JWT_COOKIE_SAMESITE = "Lax" (CSRF protection)
- CORS origins = ["https://your-domain.com"] (specific domains)
- app.debug = False (disable debug mode)

---

## Author

**Author:** AbsoluteCoder01

**Project:** Minecraft Server Hub Backend

---

<div align="center">

**If you like this project, give it a ⭐**

</div>
