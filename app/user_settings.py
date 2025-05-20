from sqlalchemy.orm import Session

from . import models


def get_user_settings(db: Session, user_id: int) -> models.UserSettings:
    """Return a user's settings row, creating defaults if needed."""
    settings = db.query(models.UserSettings).filter_by(user_id=user_id).first()
    if not settings:
        settings = models.UserSettings(user_id=user_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings
