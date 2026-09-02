from fastapi import FastAPI, HTTPException,Request,Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import engine, Base,SessionLocal
from starlette.middleware.sessions import SessionMiddleware
from utils import hash_password, verify_password
from sqlalchemy.orm import joinedload
import models
import os
from dotenv import load_dotenv
from dependencies import get_current_user,get_user_role,require_staff


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app=FastAPI()
Base.metadata.create_all(bind=engine)
templates=Jinja2Templates(directory="templates")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

@app.get("/")
def home(request: Request):
    user_id = request.session.get("user_id")

    if user_id:
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )
    else:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

#master_page
@app.get("/master")
def master_page(
    request: Request,
    tag_code: str | None = None, error: str | None = None
):

    db = SessionLocal()

    masters = db.query(models.MasterTable).all()

    selected_master = None
    values = []

    if tag_code:
        selected_master = db.query(
            models.MasterTable
        ).filter(
            models.MasterTable.tag_code == tag_code
        ).first()

        if selected_master:
            values = db.query(
                models.MasterListTable
            ).filter(
                models.MasterListTable.tag_code == tag_code
            ).all()

    db.close()

    return templates.TemplateResponse(
        name="master.html",
        request=request,
        context={
            "masters": masters,
            "selected_master": selected_master,
            "values": values,
            "error": error
        }
    )


#generate_code
def generate_tag_code(db):
    masters=db.query(models.MasterTable).all()
    if not masters:
        return "T0001"
    numbers=[]
    for master in masters:
        number = int(master.tag_code[1:])
        numbers.append(number)

    next_number = max(numbers) + 1

    return f"T{next_number:04d}"


#add_master
@app.post("/master")
def add_master(request:Request, name: str = Form(...)):
    name = name.strip()
    db = SessionLocal()
    tag_code = generate_tag_code(db)
    master = models.MasterTable(name=name, tag_code=tag_code)
    db.add(master)
    db.commit()
    db.close()
    return RedirectResponse(
        url="/master",
        status_code=303
    )

#delete_master
@app.post("/master/{master_id}/delete")
def delete_master(master_id: int):

    db = SessionLocal()
    master = db.query(models.MasterTable).filter(models.MasterTable.id == master_id).first()
    if master:
        tag_code = master.tag_code
        values = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == tag_code).all()
        for value in values:
            db.delete(value)
        db.delete(master)
        db.commit()
    db.close()

    return RedirectResponse(
        url="/master",
        status_code=303
    )



#add_master_value
@app.post("/master/{tag_code}/value")
def add_master_value(
    tag_code: str,
    value: str = Form(...)
):
    value = value.strip()
    db = SessionLocal()
    master = db.query(models.MasterTable).filter(models.MasterTable.tag_code == tag_code).first()
    
    if master:
        existing_value = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == tag_code,models.MasterListTable.value == value).first()

        if not existing_value:
            master_value = models.MasterListTable(tag_code=tag_code,value=value)
            db.add(master_value)
            db.commit()
        else:
            db.close()
            return RedirectResponse(
            url=f"/master?tag_code={tag_code}&error=duplicate",
            status_code=303
        )

    db.close()

    return RedirectResponse(
        url=f"/master?tag_code={tag_code}",
        status_code=303
    )

#delete_master_value
@app.post("/master/value/{value_id}")
def delete_master_value(value_id: int):

    db = SessionLocal()

    master_value = db.query(models.MasterListTable).filter(models.MasterListTable.id == value_id).first()
    if master_value:
        tag_code = master_value.tag_code
        db.delete(master_value)
        db.commit()
    else:
        tag_code = ""

    db.close()

    return RedirectResponse(
        url=f"/master?tag_code={tag_code}",
        status_code=303
    )

#register_page
@app.get("/register")
def register_page(request: Request, error: str | None = None):

    db = SessionLocal()

    roles = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == "T0003"
    ).all()

    db.close()

    return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={
            "roles": roles,
            "error": error
        }
    )

#register_user
@app.post("/register")
def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_id: int = Form(...)
):

    db = SessionLocal()

    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()

    if existing_user:
        db.close()

        return RedirectResponse(
            url="/register?error=email_exists",
            status_code=303
        )

    hashed_password = hash_password(password)

    user = models.User(
        name=name,
        email=email,
        password=hashed_password,
        role_id=role_id
    )

    db.add(user)
    db.commit()

    db.close()

    return RedirectResponse(
        url="/login",
        status_code=303
    )

#login_page
@app.get("/login")
def login_page(request: Request,error: str | None = None):

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={
            "error": error}
    )

#login_user
@app.post("/login")
def login_user(request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()

    if not user:
        db.close()

        return RedirectResponse(
            url="/login?error=user not found",
            status_code=303
        )

    password_correct = verify_password(
        password,
        user.password
    )

    if not password_correct:
        db.close()

        return RedirectResponse(
            url="/login?error=incorrect password",
            status_code=303
        )

    request.session["user_id"] = user.id
    db.close()
    

    return RedirectResponse(
                url="/dashboard",
                status_code=303
            )

#logout_user
@app.post("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )

# dashboard
@app.get("/dashboard")
def dashboard(request: Request):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    role = get_user_role(user)

    # ---------------- USER DASHBOARD ----------------

    if role == "User":

        db = SessionLocal()

        tickets = db.query(
            models.Ticket
        ).options(
            joinedload(models.Ticket.priority),
            joinedload(models.Ticket.status),
            joinedload(models.Ticket.assignee)
        ).filter(
            models.Ticket.created_by == user.id
        ).all()

        db.close()

        return templates.TemplateResponse(
            name="user_dashboard.html",
            request=request,
            context={
                "user": user,
                "tickets": tickets
            }
        )

    # ---------------- STAFF / ADMIN DASHBOARD ----------------

    if role in ["Admin", "Support Staff"]:

        db = SessionLocal()

        tickets = db.query(
            models.Ticket
        ).options(
            joinedload(models.Ticket.creator),
            joinedload(models.Ticket.priority),
            joinedload(models.Ticket.status),
            joinedload(models.Ticket.assignee)
        ).all()

        # Get all Support Staff
        support_staff = db.query(
            models.User
        ).join(
            models.MasterListTable,
            models.User.role_id == models.MasterListTable.id
        ).filter(
            models.MasterListTable.value == "Support Staff"
        ).all()

        # change status

        statuses = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == "T0002").all()

        # Available staff for each ticket
        available_staff_by_ticket = {}

        for ticket in tickets:

            available_staff = []

            for staff in support_staff:

                # If this staff member is already assigned
                # to the current ticket, keep them visible.
                if ticket.assigned_to == staff.id:
                    available_staff.append(staff)
                    continue

                # Check whether staff has another active ticket
                active_ticket = db.query(
                    models.Ticket
                ).filter(
                    models.Ticket.assigned_to == staff.id,
                    models.Ticket.status.has(
                        models.MasterListTable.value != "Closed"
                    ),
                    models.Ticket.id != ticket.id
                ).first()

                # If no active ticket, staff is available
                if not active_ticket:
                    available_staff.append(staff)

            available_staff_by_ticket[ticket.id] = available_staff

        db.close()

        return templates.TemplateResponse(
            name="staff_dashboard.html",
            request=request,
            context={
                "user": user,
                "tickets": tickets,
                "available_staff_by_ticket": available_staff_by_ticket,
                "statuses": statuses
            }
        )

    # Unknown role
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )

#admin_tickets
@app.get("/admin/tickets")
def admin_tickets(request: Request):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    if not require_staff(user):
        return {
            "message": "Access denied"
        }

    return {
        "message": "Welcome to the staff ticket management"
    }

#create_ticket_page
@app.get("/tickets/create")
def create_ticket_page(request: Request):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    db = SessionLocal()

    priorities = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == "T0001"
    ).all()

    statuses = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == "T0002"
    ).all()

    db.close()

    return templates.TemplateResponse(
        name="create_ticket.html",
        request=request,
        context={
            "user": user,
            "priorities": priorities,
            "statuses": statuses
        }
    )

# create_ticket
@app.post("/tickets/create")
def create_ticket(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    priority_id: int = Form(...)
):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    db = SessionLocal()

    # Find the "Open" status from master data
    open_status = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == "T0002",
        models.MasterListTable.value == "Open"
    ).first()

    if not open_status:
        db.close()

        raise HTTPException(
            status_code=500,
            detail="Open status not found in master data"
        )

    ticket = models.Ticket(
        title=title,
        description=description,
        priority_id=priority_id,
        status_id=open_status.id,
        created_by=user.id
    )

    db.add(ticket)
    db.commit()

    db.close()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# Assign Ticket
@app.post("/admin/tickets/{ticket_id}/assign")
def assign_ticket(
    request: Request,
    ticket_id: int,
    assigned_to: int | None = Form(None)
):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    role = get_user_role(user)

    if role not in ["Admin", "Support Staff"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to assign tickets"
        )

    db = SessionLocal()

    ticket = db.query(
        models.Ticket
    ).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )
    
    if assigned_to is not None:

        staff = db.query(
            models.User
        ).filter(
            models.User.id == assigned_to
        ).first()

        if not staff:
            db.close()

            raise HTTPException(
                status_code=404,
                detail="Support staff not found"
            )

        staff_role = get_user_role(staff)

        if staff_role != "Support Staff":
            db.close()

            raise HTTPException(
                status_code=400,
                detail="Only Support Staff can be assigned"
            )

        active_ticket = db.query(
            models.Ticket
        ).filter(
            models.Ticket.assigned_to == staff.id,
            models.Ticket.status.has(
                models.MasterListTable.value != "Closed"
            ),
            models.Ticket.id != ticket.id
        ).first()

        if active_ticket:
            db.close()

            raise HTTPException(
                status_code=400,
                detail="This staff member is already working on an active ticket"
            )

    ticket.assigned_to = assigned_to

    db.commit()

    db.close()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# Ticket Details
@app.get("/tickets/{ticket_id}")
def ticket_detail(
    request: Request,
    ticket_id: int
):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    db = SessionLocal()

    ticket = db.query(
    models.Ticket
    ).options(
        joinedload(models.Ticket.creator),
        joinedload(models.Ticket.priority),
        joinedload(models.Ticket.status),
        joinedload(models.Ticket.assignee)
    ).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    role = get_user_role(user)

    can_comment = False
    comment_message = None

    if role == "User":
        if ticket.created_by == user.id:
            can_comment = True
        else:
            db.close()
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to view this ticket"
            )

    elif role == "Support Staff":
        if ticket.assigned_to == user.id:
            can_comment = True
        else:
            comment_message = "You can only comment on tickets assigned to you."

    elif role == "Admin":
        can_comment = True

    comments = db.query(
        models.Comment
    ).filter(
        models.Comment.ticket_id == ticket.id
    ).order_by(
        models.Comment.created_at.asc()
    ).all()

    db.close()


    # Admin and Support Staff can view any ticket
    return templates.TemplateResponse(
        name="ticket_detail.html",
        request=request,
        context={
            "user": user,
            "ticket": ticket,
            "comments":comments,
            "can_comment": can_comment,
            "comment_message": comment_message
        }
    )

# Add Comment
@app.post("/tickets/{ticket_id}/comments")
def add_comment(
    request: Request,
    ticket_id: int,
    comment: str = Form(...)
):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    comment = comment.strip()

    if not comment:
        raise HTTPException(
            status_code=400,
            detail="Comment cannot be empty"
        )

    db = SessionLocal()

    ticket = db.query(
        models.Ticket
    ).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Normal user can comment only on their own ticket
    role = get_user_role(user)

    if role == "User":
        if ticket.created_by != user.id:
            db.close()
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to comment on this ticket"
            )

    elif role == "Support Staff":
        if ticket.assigned_to != user.id:
            db.close()
            raise HTTPException(
                status_code=403,
                detail="You can only comment on tickets assigned to you"
            )

    elif role == "Admin":
            pass

    else:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to comment"
        )

    new_comment = models.Comment(
        ticket_id=ticket.id,
        user_id=user.id,
        comment=comment
    )

    db.add(new_comment)
    db.commit()

    db.close()

    return RedirectResponse(
        url=f"/tickets/{ticket_id}",
        status_code=303
    )

#change status
@app.post("/admin/tickets/{ticket_id}/status")
def update_ticket_status(
    request: Request,
    ticket_id: int,
    status_id: int = Form(...)
):
    user = get_current_user(request)

    if not user:
        return RedirectResponse("/login", status_code=303)

    role = get_user_role(user)

    if role not in ["Admin", "Support Staff"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to change ticket status"
        )

    db = SessionLocal()

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    status = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.id == status_id,
        models.MasterListTable.tag_code == "T0002"
    ).first()

    if not status:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    current_status = db.query(models.MasterListTable).filter(models.MasterListTable.id == ticket.status_id).first()
    
    if status.value == "Close":
        if current_status.value != "Resolved":
            db.close()
            raise HTTPException(
                status_code=400,
                detail="Ticket must be Resolved before it can be Closed"
            )

    ticket.status_id = status.id
    
    db.commit()
    db.close()

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )