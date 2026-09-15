# resolveDesk

A web-based Ticket Management System built with **FastAPI**, **SQLite**, **SQLAlchemy**, **Jinja2**, **HTML**, and **CSS**.

resolveDesk allows users to create and track support tickets, while Admins manage tickets and Support Staff work on assigned tickets.

---

## Table of Contents

- [Features](#features)
- [Ticket Workflow](#ticket-workflow)
- [Master Data](#master-data)
- [Database](#database)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Authentication](#authentication)
- [Ticket Assignment](#ticket-assignment)
- [Role-Based Access](#role-based-access)
- [Purpose](#purpose)
- [Project Status](#project-status)
- [Author](#author)

---

## Features

### Authentication
- User registration
- Secure password hashing with bcrypt
- Login and logout using session-based authentication
- Role-based access control
- Session-based user authentication

### User
- Register through the public registration page
- Create support tickets
- View their own tickets
- View ticket details
- Comment on their own tickets
- Track ticket status and priority

### Support Staff
- Login using their account
- View tickets assigned to them
- Work on multiple assigned tickets
- Update ticket status
- Move tickets through the support workflow
- Add comments to assigned tickets

### Admin
- View all tickets
- Assign tickets to Support Staff
- Reassign tickets
- Assign multiple tickets to the same Support Staff
- Filter tickets by assigned staff
- Manage Master Data
- Manage users through User Master

---

## Ticket Workflow

```text
User creates ticket
        ↓
      Open
        ↓
Admin assigns Support Staff
        ↓
   In Progress
        ↓
    Resolved
        ↓
     Closed
```

A Support Staff member can have multiple tickets assigned at the same time.

---

## Master Data

The application uses master data for values such as:

| Category | Values |
|---|---|
| **Priority** | Low, Medium, High |
| **Status** | Open, In Progress, Resolved, Closed |
| **Role** | User, Support Staff, Admin |

---

## Database

**Current database:**
- SQLite
- SQLAlchemy ORM

**Main tables:**
- `users`
- `tickets`
- `comments`
- `master_table`
- `master_list_table`

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- HTML5
- CSS3
- bcrypt
- Session Authentication

---


## Installation

1. **Clone the repository**
```bash
   git clone <your-github-repository-url>
   cd resolveDesk
```

2. **Create a virtual environment**
```bash
   python -m venv venv
```

3. **Activate the virtual environment (Windows)**
```bash
   venv\Scripts\activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Create a `.env` file**
```env
   SECRET_KEY=your-secret-key
```

6. **Run the application**
```bash
   uvicorn main:app --reload
```

7. **Open the application in your browser**
```
   http://127.0.0.1:8000
```

---

## Authentication

Passwords are never stored as plain text.

resolveDesk uses:
- **bcrypt** for password hashing
- **Session-based authentication**
- **Role-based authorization**

Public registration automatically creates a **User** account. Role selection is not available on the public registration form — admin-controlled user management is used for creating accounts with different roles.

---

## Ticket Assignment

Admins can assign tickets to Support Staff. There is no one-ticket-at-a-time restriction.

**Example:**
```text
Staff A
├── Ticket #101
├── Ticket #102
├── Ticket #103
└── Ticket #104
```

All assigned tickets are available to the staff member through the **My Assigned Tickets** page.

---

## Role-Based Access

```text
User
├── Create tickets
├── View own tickets
└── Comment on own tickets

Support Staff
├── View assigned tickets
├── Work on assigned tickets
├── Update ticket status
└── Comment on assigned tickets

Admin
├── View all tickets
├── Assign tickets
├── Reassign tickets
├── Manage Master Data
└── Manage Users
```

---

## Purpose

resolveDesk was developed as a practical Help Desk application to demonstrate:

- Backend web development
- FastAPI development
- Database design
- SQLAlchemy ORM
- Authentication & Authorization
- Role-based access control
- CRUD operations
- Ticket management
- Master data management
- Server-side rendering with Jinja2

---

## Project Status

🚧 **Currently under development.**

**Planned Deployment:**
- Neon PostgreSQL
- Render

*A live demo link will be added after deployment.*
