from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.models import Notification
from app.schemas.schemas import Notification as NotificationSchema, NotificationCreate

router = APIRouter()


@router.post("/", response_model=NotificationSchema)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.get("/{notification_id}", response_model=NotificationSchema)
def get_notification(notification_id: UUID, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.get("/user/{user_id}", response_model=List[NotificationSchema])
def get_user_notifications(user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == user_id).offset(skip).limit(limit).all()
    return notifications


@router.patch("/{notification_id}/read", response_model=NotificationSchema)
def mark_notification_as_read(notification_id: UUID, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.read = True
    db.commit()
    db.refresh(notification)
    return notification