from fastapi import Request
from database import SessionLocal
import models


def get_current_user(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return None

    db = SessionLocal()

    user = db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()

    db.close()

    return user

def get_user_role(user):

    if not user:
        return None

    db = SessionLocal()

    role = db.query(
        models.MasterListTable
    ).filter(
        models.MasterListTable.id == user.role_id
    ).first()

    db.close()

    if not role:
        return None

    return role.value

def require_staff(user):

    role = get_user_role(user)

    if role not in ["Admin", "Support Staff"]:
        return False

    return True