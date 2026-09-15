from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database import SessionLocal
import models
from utils import hash_password


router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_admin(request: Request, db):

    user_id = request.session.get("user_id")

    if not user_id:
        return None

    user = db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return None

    role = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.id == user.role_id
    ).first()

    if not role or role.value != "Admin":
        return None

    return user


@router.get("/user-master")
def user_master_page(
    request: Request,
    search: str = "",
    role_filter: str = ""
):

    db = SessionLocal()

    admin = get_admin(request, db)

    if not admin:
        db.close()

        if not request.session.get("user_id"):
            return RedirectResponse(
                url="/login",
                status_code=303
            )

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )


    # Get Role master
    role_master = db.query(
        models.MasterTable
    ).filter(
        models.MasterTable.name == "Role"
    ).first()


    roles = []

    if role_master:

        roles = db.query(
            models.MasterListTable
        ).filter(
            models.MasterListTable.tag_code == role_master.tag_code
        ).all()


    # Get users
    query = db.query(models.User)


    # Search
    if search:

        search_value = f"%{search.strip()}%"

        query = query.filter(
            (models.User.name.ilike(search_value)) |
            (models.User.email.ilike(search_value))
        )


    # Role filter
    if role_filter:

        selected_role = db.query(
            models.MasterListTable
        ).filter(
            models.MasterListTable.id == int(role_filter)
        ).first()

        if selected_role:

            query = query.filter(
                models.User.role_id == selected_role.id
            )


    users = query.all()

    db.close()


    return templates.TemplateResponse(
        name="user_master.html",
        request=request,
        context={
            "users": users,
            "roles": roles,
            "search": search,
            "role_filter": role_filter
        }
    )


@router.post("/user-master/create")
def create_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_id: int = Form(...)
):

    db = SessionLocal()

    admin = get_admin(request, db)

    if not admin:

        db.close()

        if not request.session.get("user_id"):
            return RedirectResponse(
                url="/login",
                status_code=303
            )

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )


    # Check duplicate email
    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()

    if existing_user:
        db.close()

        return RedirectResponse(
            url="/user-master?error=email_exists",
            status_code=303
        )


    # Make sure selected role exists
    role = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.id == role_id
    ).first()

    if not role:
        db.close()

        return RedirectResponse(
            url="/user-master?error=invalid_role",
            status_code=303
        )


    hashed_password = hash_password(password)


    user = models.User(
        name=name,
        email=email,
        password=hashed_password,
        role_id=role.id
    )


    db.add(user)
    db.commit()
    db.close()


    return RedirectResponse(
        url="/user-master",
        status_code=303
    )


@router.post("/user-master/{user_id}/edit")
def edit_user(
    request: Request,
    user_id: int,
    role_id: int = Form(...)
):

    db = SessionLocal()

    admin = get_admin(request, db)

    if not admin:

        db.close()

        if not request.session.get("user_id"):
            return RedirectResponse(
                url="/login",
                status_code=303
            )

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )


    user = db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()


    if not user:

        db.close()

        return RedirectResponse(
            url="/user-master",
            status_code=303
        )


    role = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.id == role_id
    ).first()


    if not role:

        db.close()

        return RedirectResponse(
            url="/user-master",
            status_code=303
        )


    user.role_id = role.id

    db.commit()
    db.close()


    return RedirectResponse(
        url="/user-master",
        status_code=303
    )