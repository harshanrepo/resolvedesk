# resolveDesk

A beginner-friendly Help Desk / Ticket Management web application built with FastAPI, SQLite, SQLAlchemy, Jinja2, HTML, and CSS.

## Features

- User registration and login
- Session-based authentication
- Role-based access control
- Create and manage support tickets
- Ticket priority and status management
- Ticket comments
- Support Staff assigned-ticket management
- Admin ticket assignment and reassignment
- Master Data management
- Responsive dashboard UI
- Password hashing using bcrypt

## User Roles

### User

- Register and login
- View personal dashboard
- Create tickets
- View own tickets
- View ticket details
- Comment on own tickets

### Support Staff

- View assigned tickets
- Update ticket status
- Close assigned tickets
- Comment on assigned tickets

### Admin

- View all tickets
- Assign and reassign tickets
- Manage Master Data

## Ticket Workflow

```text
User creates ticket
        ↓
      Open
        ↓
Admin assigns ticket
        ↓
Support Staff works on ticket
        ↓
   In Progress
        ↓
     Resolved
        ↓
      Closed
```

## Tech Stack

- Backend: FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Templates: Jinja2
- Frontend: HTML, CSS
- Authentication: Session / Cookie
- Password Hashing: bcrypt
- Environment Variables: python-dotenv

## Project Structure

```text
resolveDesk/
│
├── main.py
├── models.py
├── database.py
├── dependencies.py
├── utils.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── ticket.py
│   └── master.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── user_dashboard.html
│   ├── staff_dashboard.html
│   ├── my_assigned_tickets.html
│   ├── ticket_detail.html
│   └── master.html
│
├── static/
│   ├── base.css
│   ├── auth.css
│   ├── dashboard.css
│   ├── master.css
│   ├── ticket_detail.css
│   └── favicon.ico
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Database

The application uses SQLite with SQLAlchemy.

Main tables:

- users
- tickets
- comments
- master_table
- master_list_table

Master Data is used for values such as:

### Priority

- Low
- Medium
- High

### Status

- Open
- In Progress
- Resolved
- Closed

### Role

- User
- Support Staff
- Admin

## Installation

Clone the repository:

```bash
git clone <your-github-repository-url>
cd resolveDesk
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
```

Run the application:

```bash
uvicorn main:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

## Authentication

resolveDesk uses session-based authentication.

After login, the user's ID is stored in the session. The application uses that ID to identify the logged-in user and control access to tickets and dashboard features.

Passwords are never stored as plain text. They are hashed using bcrypt.

## Purpose

This project was built to understand how a real-world FastAPI web application works, including:

- Authentication
- Authorization
- CRUD operations
- Database relationships
- Form handling
- Sessions
- Role-based access
- Jinja2 templates
- Responsive frontend design
- Admin and staff workflows

## Status

Completed

Built as a learning and portfolio project.
