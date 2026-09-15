from fastapi import APIRouter, Request, Form,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models
from utils import hash_password, verify_password, get_master_by_name

router = APIRouter()
templates=Jinja2Templates(directory="templates")


#register_page
@router.get("/register")
def register_page(request: Request, error: str | None = None):

    user_id = request.session.get("user_id")

    if user_id:
        db = SessionLocal()

        user = db.query(
            models.User
        ).filter(
            models.User.id == user_id
        ).first()

        if user:
            role = db.query(
                models.MasterListTable
            ).filter(
                models.MasterListTable.id == user.role_id
            ).first()

            db.close()

            if role and role.value == "Support Staff":
                return RedirectResponse(
                    url="/dashboard",
                    status_code=303
                )
        else:
            db.close()

    return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={
            "error": error
        }
    )

#register_user
@router.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()

    if existing_user:
        db.close()

        return templates.TemplateResponse(
            name="register.html",
            request=request,
            context={
                "error": "email_exists"
            }
        )

    # Get the User role
    role_master = get_master_by_name(db, "Role")

    if not role_master:
        db.close()
        raise HTTPException(
            status_code=500,
            detail="Role master data not found"
        )

    user_role = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == role_master.tag_code,
        models.MasterListTable.value == "User"
    ).first()

    if not user_role:
        db.close()
        raise HTTPException(
            status_code=500,
            detail="User role not found"
        )

    hashed_password = hash_password(password)

    user = models.User(
        name=name,
        email=email,
        password=hashed_password,
        role_id=user_role.id
    )

    db.add(user)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/login",
        status_code=303
    )

#login_page
@router.get("/login")
def login_page(request: Request,error: str | None = None):

    return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={
                "error": error,
            }
    )

#login_user
@router.post("/login")
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

        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={
                "error": "user not found",
            }
        )

    password_correct = verify_password(
        password,
        user.password
    )

    if not password_correct:
        db.close()

        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={
                "error": "user not found",
            }
        )

    request.session["user_id"] = user.id
    db.close()
    

    return RedirectResponse(
                url="/dashboard",
                status_code=303
            )

#logout_user
@router.post("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )