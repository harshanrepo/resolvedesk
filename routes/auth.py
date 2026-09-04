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

    db = SessionLocal()
    roleMaster=get_master_by_name(db, "Role")

    if not roleMaster:
        db.close()
        raise HTTPException(
            status_code=500,
            detail="Role master data not found"
        )

    roles = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.tag_code == roleMaster.tag_code
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
@router.post("/register")
def register_user(request: Request,
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

    roleMaster=get_master_by_name(db, "Role")

    if existing_user:
        roles = db.query(
                models.MasterListTable
            ).filter(
                models.MasterListTable.tag_code == roleMaster.tag_code
            ).all()
        
        db.close()

        return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={
            "error": "email_exists",
            "roles": roles
        }
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