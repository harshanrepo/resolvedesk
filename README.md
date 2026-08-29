# ResolveDesk 🎫

A web-based **Support Ticket Management System** built with **FastAPI**. ResolveDesk allows users to create and track support tickets while administrators and support staff can manage, assign, and resolve them.

## 🚀 Features

### 👤 User

* Register and login
* Secure password hashing
* Create support tickets
* View personal tickets
* View ticket details
* Add comments
* Track ticket status
* View ticket priority and assignment

### 🛠️ Admin / Support Staff

* Login with role-based access
* View all support tickets
* Change ticket status
* Change ticket priority
* Assign tickets to support staff
* Add comments
* Resolve and close tickets

## 🎫 Ticket Management

Each ticket contains:

* **Title**
* **Description**
* **Priority** — Low / Medium / High
* **Status** — Open / In Progress / Resolved / Closed
* **Created By**
* **Assigned Staff**
* **Created Date**
* **Updated Date**

## 🧰 Tech Stack

| Technology             | Purpose                   |
| ---------------------- | ------------------------- |
| **FastAPI**            | Backend framework         |
| **SQLite**             | Database                  |
| **SQLAlchemy**         | ORM / Database management |
| **Jinja2**             | HTML templating           |
| **HTML5**              | Frontend structure        |
| **CSS3**               | Styling                   |
| **Sessions / Cookies** | Authentication            |
| **Password Hashing**   | Secure password storage   |

## 🗄️ Database Structure

The application uses three main tables:

```text
Users
 └── creates → Tickets
                  └── has → Comments
```

### Tables

* `users`
* `tickets`
* `comments`

## 📂 Project Structure

```text
resolvedesk/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tickets.py
│   │   └── admin.py
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── tickets.html
│   │   ├── create_ticket.html
│   │   ├── ticket_detail.html
│   │   └── admin/
│   │
│   └── static/
│       └── css/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/resolvedesk.git
```

```bash
cd resolvedesk
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

Open the application at:

```text
http://127.0.0.1:8000
```

## 🔐 Authentication & Authorization

ResolveDesk uses session-based authentication.

Users can only access and manage their own tickets, while administrators/support staff have access to ticket management features.

Passwords are stored using secure password hashing rather than storing plain-text passwords.

## 📚 What I Learned

This project was built to understand how a real-world FastAPI web application is structured.

Key concepts practiced:

* FastAPI routing
* REST API concepts
* GET / POST / PUT / DELETE
* Pydantic schemas
* SQLAlchemy ORM
* SQLite database
* Database relationships
* CRUD operations
* Jinja2 templates
* HTML forms
* Form validation
* Sessions and cookies
* Authentication
* Authorization
* Password hashing
* Role-based access control
* Query parameters
* Filtering and searching
* Project structure

## 🎯 Future Improvements

* Email notifications
* File attachments for tickets
* Ticket search and advanced filtering
* Pagination
* Admin dashboard with statistics
* API documentation
* REST API endpoints
* Docker support
* PostgreSQL support

## 👨‍💻 Author

**Harshan**

Built as a learning project to understand **FastAPI backend development, authentication, database relationships, and full-stack web application development**.

```

### ⭐ Project

**ResolveDesk — Support Ticket Management System**

**Built with:** FastAPI • SQLAlchemy • SQLite • Jinja2 • HTML • CSS
```
