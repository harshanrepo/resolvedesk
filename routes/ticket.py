from fastapi import APIRouter, Request, Form
from dependencies import get_current_user,get_user_role,require_staff
from fastapi.responses import RedirectResponse
import models
from sqlalchemy.orm import joinedload
from database import SessionLocal
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="templates")
from fastapi import HTTPException
from utils import time_ago


router = APIRouter()


#admin_tickets
@router.get("/admin/tickets")
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


# create_ticket
@router.post("/tickets/create")
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
@router.post("/admin/tickets/{ticket_id}/assign")
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
@router.get("/tickets/{ticket_id}")
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
    ).options(
        joinedload(models.Comment.user)
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
            "comment_message": comment_message,
            "time_ago": time_ago
        }
    )

# Add Comment
@router.post("/tickets/{ticket_id}/comments")
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
@router.post("/admin/tickets/{ticket_id}/status")
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
    
    if status.value == "Closed":
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