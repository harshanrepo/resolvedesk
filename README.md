# resolveDesk

**Currently in Progress**

[![Live Demo](https://img.shields.io/badge/LIVE%20DEMO-resolvedesk--hydk.onrender.com-0d1117?style=for-the-badge&logo=render&logoColor=white)](https://resolvedesk-hydk.onrender.com)

A web-based Ticket Management System built with **FastAPI**, **SQLite**, **SQLAlchemy**, **Jinja2**, **HTML**, and **CSS**.

resolveDesk lets Users create and track support tickets, Admins manage tickets and users, and Support Staff work through tickets assigned to them.

---

## Table of Contents

- [Features](#features)
- [Ticket Workflow](#ticket-workflow)
- [Master Data](#master-data)
- [Database](#database)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Authentication](#authentication)
- [Ticket Assignment](#ticket-assignment)
- [Role-Based Access](#role-based-access)
- [Purpose](#purpose)
- [Author](#author)

---

## Features

### Authentication
- User registration
- Secure password hashing with bcrypt
- Session-based login/logout
- Role-based access control

### User
- Register through the public registration page
- Create support tickets
- View own tickets and their details
- Comment on own tickets
- Track ticket status and priority

### Support Staff
- View tickets assigned to them
- Work on multiple assigned tickets at once
- Update ticket status
- Comment on assigned tickets

### Admin
- View all tickets
- Assign and reassign tickets to Support Staff
- Filter tickets by assigned staff
- Manage Master Data (priorities, statuses, roles)
- Manage users via User Master

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

| Category | Values |
|---|---|
| **Priority** | Low, Medium, High |
| **Status** | Open, In Progress, Resolved, Closed |
| **Role** | User, Support Staff, Admin |
| **Ticket Type** | Software, Hardware |

---

## Database

- **Engine:** SQLite
- **ORM:** SQLAlchemy

**Tables:** `users`, `tickets`, `comments`, `master_table`, `master_list_table`

---

## Tech Stack

Python · FastAPI · SQLAlchemy · SQLite · Jinja2 · HTML5 · CSS3 · bcrypt · Session Authentication

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

3. **Activate the virtual environment**
```bash
   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Create a `.env` file**
```env
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///./resolveDesk.db
```

6. **Run the application**
```bash
   uvicorn main:app --reload
```

7. **Open in your browser**
   http://127.0.0.1:8000


---

## Authentication

Passwords are never stored as plain text.

- **bcrypt** for password hashing
- **Session-based** authentication
- **Role-based** authorization

Public registration always creates a **User** account. Accounts with other roles (Support Staff, Admin) are created through admin-controlled User Master, not the public form.

---

## Ticket Assignment

Admins can assign tickets to Support Staff with no one-ticket-at-a-time limit:

```text
Staff A
├── Ticket #101
├── Ticket #102
├── Ticket #103
└── Ticket #104
```

All tickets assigned to a staff member appear on their **My Assigned Tickets** page.

---

## Role-Based Access

```text
User
├── Create tickets
├── View own tickets
└── Comment on own tickets

Support Staff
├── View assigned tickets
├── Update ticket status
└── Comment on assigned tickets

Admin
├── View all tickets
├── Assign / reassign tickets
├── Manage Master Data
└── Manage Users
```

## Purpose

resolveDesk was built as a practical Help Desk application to demonstrate:

- FastAPI backend development
- Database design with SQLAlchemy ORM
- Authentication & role-based authorization
- CRUD operations and ticket workflow management
- Master data management
- Server-side rendering with Jinja2

---

## Author

**Shri Harshan M**

[![Email](https://skillicons.dev/icons?i=gmail)](mailto:shriharshancse@gmail.com)&nbsp;&nbsp;&nbsp;[![LinkedIn](https://skillicons.dev/icons?i=linkedin)](https://www.linkedin.com/in/mrshri-harshan/)&nbsp;&nbsp;&nbsp;[![Portfolio](https://skillicons.dev/icons?i=vercel)](https://harshan-portfolio.onrender.com)
