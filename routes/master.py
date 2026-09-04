from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from dependencies import get_current_user,get_user_role


router = APIRouter()
templates=Jinja2Templates(directory="templates")



#master_page
@router.get("/master")
def master_page(
    request: Request,
    tag_code: str | None = None, error: str | None = None
):

    db = SessionLocal()

    masters = db.query(models.MasterTable).all()

    user = get_current_user(request)

    if not user:
        return RedirectResponse("/login", status_code=303)

    role = get_user_role(user)

    if role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access Master Data"
        )

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
    "user": user,
    "role": role,
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
        numbers.routerend(number)

    next_number = max(numbers) + 1

    return f"T{next_number:04d}"


#add_master
@router.post("/master")
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
@router.post("/master/{master_id}/delete")
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
@router.post("/master/{tag_code}/value")
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
@router.post("/master/value/{value_id}")
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
