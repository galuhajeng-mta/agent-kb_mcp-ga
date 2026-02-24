from app.api.v1.routers.ticket import create_ticket, list_tickets as get_tickets, get_ticket, done_ticket
from app.db import get_db
from sqlalchemy.orm import Session

# NOTE: skill harus async
async def create_ticket_skill(message: str):
    db: Session = next(get_db())
    return create_ticket(message=message, db=db)


async def list_tickets_skill():
    db: Session = next(get_db())
    return get_tickets(db=db)


async def get_ticket_skill(ticket_id: int):
    db: Session = next(get_db())
    return get_ticket(ticket_id=ticket_id, db=db)

async def done_ticket_skill(ticket_id: int):
    db: Session = next(get_db())
    return done_ticket(ticket_id=ticket_id, db=db)


