from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from routes import auth,dashboard,ticket,master


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app=FastAPI()
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(ticket.router)
app.include_router(master.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)
app.add_middleware(SessionMiddleware,secret_key=SECRET_KEY)

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







