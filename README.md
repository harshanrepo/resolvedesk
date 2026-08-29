# ResolveDesk 🎫

A support ticket management system built with **FastAPI**.

> 🚧 **Status: Currently Under Construction**
>
> ResolveDesk is an ongoing project. Features are being developed and improved step by step.

## 📌 About

ResolveDesk is a beginner-friendly Help Desk web application where users can create and track support tickets, while support staff and administrators can manage tickets, update statuses, assign tickets, and respond to users.

The project is being built from scratch to understand how a complete web application works with **FastAPI, databases, authentication, CRUD operations, and server-side templates**.

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Frontend:** HTML, CSS
* **Templates:** Jinja2
* **Authentication:** Sessions / Cookies
* **Password Security:** Password Hashing

## 🚀 Planned Features

### User

* User registration and login
* Create support tickets
* View personal tickets
* View ticket details
* Add comments
* Track ticket status

### Admin / Support Staff

* View all tickets
* Update ticket status
* Change ticket priority
* Assign tickets to support staff
* Add comments
* Close tickets

### Ticket Management

Each ticket will contain:

* Title
* Description
* Priority
* Status
* Created by
* Assigned staff
* Created date
* Updated date

## 🗄️ Database Structure

The application will use three main tables:

```text
Users
  │
  └── creates ──> Tickets
                    │
                    └── has ──> Comments
```

## 📚 Learning Goals

This project is being developed to practice:

* FastAPI routing
* RESTful operations
* Pydantic schemas
* SQLAlchemy
* SQLite
* Database relationships
* CRUD operations
* Jinja2 templates
* HTML forms
* Sessions and cookies
* Authentication & authorization
* Password hashing
* Form validation
* Filtering and searching
* Clean project structure

## 📂 Project Status

The project is currently under active development.

Development will be completed step by step, starting from the database and authentication system and progressing toward ticket management, admin functionality, frontend templates, styling, and testing.

## 🔮 Future Improvements

Possible future additions include:

* Email notifications
* Ticket search and advanced filtering
* Pagination
* File attachments
* Dashboard statistics
* REST API documentation
* Improved role and permission management

---

**Built with FastAPI • SQLAlchemy • SQLite • Jinja2**
