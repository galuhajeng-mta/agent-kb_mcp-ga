from sqlalchemy.orm import Session
from app.db import get_db
from app.models.ticket import Ticket
from app.models.staff import Staff

def detect_role(message: str) -> str:
    message = message.lower()
    if "ac" in message or "listrik" in message or "air" in message:
        return "maintenance"
    if "handuk" in message or "bersih" in message:
        return "housekeeping"
    return "customer_service"


async def create_ticket(message: str):
    db: Session = next(get_db())

    role = detect_role(message)
    staff = db.query(Staff).filter(Staff.role == role).first()

    ticket = Ticket(
        message=message,
        status="assigned" if staff else "created",
        assigned_staff_id=staff.id if staff else None,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "ticket_id": ticket.id,
        "status": ticket.status,
        "assigned_role": role,
        "assigned_staff": staff.name if staff else None,
    }
