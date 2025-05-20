from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.exception_handlers import http_exception_handler as fastapi_http_exception_handler
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from . import auth, models
from .database import Base, engine, get_db
from .user_settings import get_user_settings
from .routes import (
    auth as auth_routes,
    forecast as forecast_routes,
    pages as pages_routes,
    suggestions as suggestions_routes,
    settings as settings_routes,
)
from .dependencies import templates

Base.metadata.create_all(bind=engine)


def create_default_user(db: Session) -> None:
    """Create a default user if one does not already exist."""
    if not db.query(models.User).filter(models.User.username == "test").first():
        hashed = auth.get_password_hash("test")
        user = models.User(username="test", hashed_password=hashed)
        db.add(user)
        db.commit()
        get_user_settings(db, user.id)


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")


@app.on_event("startup")
def startup_event() -> None:
    """Run startup tasks like creating the default user."""
    get_db_override = app.dependency_overrides.get(get_db, get_db)
    db_gen = get_db_override()
    db = next(db_gen)
    try:
        create_default_user(db)
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Redirect unauthorized users to the login page with a warning."""
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        url = app.url_path_for("login_form") + "?error=Please%20log%20in%20to%20access%20that%20page"
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    return await fastapi_http_exception_handler(request, exc)


app.include_router(auth_routes.router)
app.include_router(forecast_routes.router)
app.include_router(pages_routes.router)
app.include_router(suggestions_routes.router)
app.include_router(settings_routes.router)
