from fastapi import APIRouter, Request,HTTPException
from dependencies import get_current_user,get_user_role
from fastapi.responses import RedirectResponse
import models
from sqlalchemy.orm import joinedload
from database import SessionLocal
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="templates")
from utils import get_master_by_name, time_ago

router = APIRouter()


# dashboard
@router.get("/dashboard")
def dashboard(
    request: Request,
    search: str | None = None,
    status: str | None = None,
    priority_id: int | None = None,
    assigned_to: str | None = None
):

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

        query = db.query(
            models.Ticket
        ).options(
            joinedload(models.Ticket.priority),
            joinedload(models.Ticket.status),
            joinedload(models.Ticket.assignee)
        ).filter(
            models.Ticket.created_by == user.id
        )

        roleMaster=get_master_by_name(db, "Priority")
        status_master = get_master_by_name(db, "Status")

        priorities = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == roleMaster.tag_code).all()
        statuses = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == status_master.tag_code).all()

        # Search by Ticket ID or Title
        if search:
            search = search.strip()

            if search.isdigit():
                query = query.filter(
                    models.Ticket.id == int(search)
                )
            else:
                query = query.filter(
                    models.Ticket.title.ilike(f"%{search}%")
                )

        # Filter by Status
        if status:
            query = query.join(
                models.MasterListTable,
                models.Ticket.status_id == models.MasterListTable.id
            ).filter(
                models.MasterListTable.value == status
            )

        # Filter by Priority
        if priority_id:
            query = query.filter(
                models.Ticket.priority_id == priority_id
            )

        
        tickets = query.all()

        total_tickets = len(tickets)

        open_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "Open"
        )

        in_progress_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "In Progress"
        )

        resolved_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "Resolved"
        )

        closed_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "Closed"
)


        db.close()

        return templates.TemplateResponse(
            name="user_dashboard.html",
            request=request,
            context={
            "user": user,
            "tickets": tickets,
            "priorities": priorities,
            "statuses": statuses,

            "search": search,
            "status_filter": status,
            "priority_filter": priority_id,
            

            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "closed_tickets": closed_tickets,
            "time_ago": time_ago,
}
        )

    # ---------------- STAFF / ADMIN DASHBOARD ----------------

    if role in ["Admin", "Support Staff"]:

        db = SessionLocal()

        priority_master = get_master_by_name(db, "Priority")
        status_master = get_master_by_name(db, "Status")

        priorities = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == priority_master.tag_code).all()
        statuses = db.query(models.MasterListTable).filter(models.MasterListTable.tag_code == status_master.tag_code).all()

        query = db.query(models.Ticket
            ).options(
            joinedload(models.Ticket.creator),
            joinedload(models.Ticket.priority),
            joinedload(models.Ticket.status),
            joinedload(models.Ticket.assignee)
            )

        # Search by Ticket ID, Title or Creator
        if search:
            search = search.strip()

            if search.isdigit():
                query = query.filter(
                    models.Ticket.id == int(search)
                )
            else:
                query = query.join(
                    models.User,
                    models.Ticket.created_by == models.User.id
                ).filter(
                    (models.Ticket.title.ilike(f"%{search}%")) |
                    (models.User.name.ilike(f"%{search}%"))
                )

        # Filter by Status
        if status:
            query = query.join(
                models.MasterListTable,
                models.Ticket.status_id == models.MasterListTable.id
            ).filter(
                models.MasterListTable.value == status
            )

        # Filter by Priority
        if priority_id:
            query = query.filter(
                models.Ticket.priority_id == priority_id
            )

        # Filter by Assigned To (only for Admin)
        if assigned_to and role == "Admin":
                query = query.filter(models.Ticket.assigned_to == int(assigned_to))
        

        tickets = query.all()

        total_tickets = len(tickets)

        open_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "Open"
        )

        in_progress_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "In Progress"
        )

        resolved_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "Resolved"
        )

        closed_tickets = sum(
            1 for ticket in tickets
            if ticket.status.value == "Closed"
        )

        # Get all Support Staff
        support_staff = db.query(
            models.User
        ).join(
            models.MasterListTable,
            models.User.role_id == models.MasterListTable.id
        ).filter(
            models.MasterListTable.value == "Support Staff"
        ).all()

        active_tickets = db.query(models.Ticket).filter(models.Ticket.assigned_to.isnot(None),models.Ticket.status.has(models.MasterListTable.value != "Closed")).all()

        busy_staff_ids = {ticket.assigned_to for ticket in active_tickets}

        # Available staff for each ticket
        available_staff_by_ticket = {}

        for ticket in tickets:

            available_staff = []

            for staff in support_staff:

                if ticket.assigned_to == staff.id:
                    available_staff.append(staff)
                    continue

                if staff.id not in busy_staff_ids:
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
            "statuses": statuses,
            "priorities": priorities,
            "role": role,

            "search": search,
            "status_filter": status,
            "priority_filter": priority_id,
            "support_staff": support_staff,
            "assigned_to_filter": assigned_to,

            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "closed_tickets": closed_tickets,
            "time_ago": time_ago,
            }
        )

    # Unknown role
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )


@router.get("/my-assigned-tickets")
def my_assigned_tickets(
    request: Request,
    search: str | None = None,
    status: str | None = None,
    priority_id: str | None = None
):

    user = get_current_user(request)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    role = get_user_role(user)

    # Only Support Staff can access this page
    if role != "Support Staff":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this page"
        )

    db = SessionLocal()

    query = db.query(
    models.Ticket
    ).options(
        joinedload(models.Ticket.creator),
        joinedload(models.Ticket.priority),
        joinedload(models.Ticket.status)
    ).filter(
        models.Ticket.assigned_to == user.id
    )

    # Search by Ticket ID or Title
    if search:
        search = search.strip()

        if search.isdigit():
            query = query.filter(
                models.Ticket.id == int(search)
            )
        else:
            query = query.filter(
                models.Ticket.title.ilike(f"%{search}%")
            )

    # Filter by Status
    if status:
        query = query.join(
            models.MasterListTable,
            models.Ticket.status_id == models.MasterListTable.id
        ).filter(
            models.MasterListTable.value == status
        )

    # Filter by Priority
    if priority_id:
        query = query.filter(
        models.Ticket.priority_id == int(priority_id)
    )

    priority_master = get_master_by_name(db, "Priority")
    status_master = get_master_by_name(db, "Status")

    priorities = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == priority_master.tag_code
    ).all()

    statuses = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == status_master.tag_code
    ).all()

    tickets = query.all()

    total_tickets = len(tickets)

    open_tickets = sum(
        1 for ticket in tickets
        if ticket.status.value == "Open"
    )

    in_progress_tickets = sum(
        1 for ticket in tickets
        if ticket.status.value == "In Progress"
    )

    resolved_tickets = sum(
        1 for ticket in tickets
        if ticket.status.value == "Resolved"
    )

    closed_tickets = sum(
        1 for ticket in tickets
        if ticket.status.value == "Closed"
    )

    db.close()
    
    return templates.TemplateResponse(
        name="my_assigned_tickets.html",
        request=request,
        context={
            "user": user,
            "tickets": tickets,
            "priorities": priorities,
            "statuses": statuses,
            "search": search,
            "status_filter": status,
            "priority_filter": priority_id,

            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "closed_tickets": closed_tickets,
            "time_ago": time_ago,
        }
    )