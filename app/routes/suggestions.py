from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..dependencies import get_current_user, templates

router = APIRouter()


@router.get("/suggestions", response_class=HTMLResponse)
def view_suggestions(
    request: Request,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    suggestions = (
        db.query(models.Suggestion)
        .order_by(models.Suggestion.timestamp.desc())
        .all()
    )
    return templates.TemplateResponse(
        "suggestions.html",
        {"request": request, "suggestions": suggestions, "username": user.username},
    )


@router.post("/suggestions")
def add_suggestion(
    content: str = Form(...),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    suggestion = models.Suggestion(user_id=user.id, content=content)
    db.add(suggestion)
    db.commit()
    return RedirectResponse(url="/suggestions", status_code=status.HTTP_303_SEE_OTHER)
