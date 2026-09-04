import bcrypt
import models
from datetime import datetime, timezone

def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hashed_bytes
    )

def get_master_by_name(db, name):
    return db.query(
        models.MasterTable
    ).filter(
        models.MasterTable.name == name
    ).first()


def time_ago(created_at):
    # Database stores UTC time as a naive datetime
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    # Current UTC time
    now = datetime.now(timezone.utc)

    difference = now - created_at

    seconds = difference.total_seconds()

    if seconds < 60:
        return "Just now"

    minutes = int(seconds // 60)

    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    hours = int(minutes // 60)

    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    days = int(hours // 24)

    if days == 1:
        return "Yesterday"

    if days < 30:
        return f"{days} days ago"

    months = int(days // 30)

    if months == 1:
        return "1 month ago"

    return f"{months} months ago"