# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import date, datetime

# from app.db import get_db
# from app.models.ticket import Ticket
# from app.models.staff import Staff
# from app.models.staff_attendance import StaffAttendance
# from app.server.auth import get_current_auth


# router = APIRouter()

# def detect_role(message: str) -> str:
#     message = message.lower()

#     maintenance_keywords = [
#         "ac", "listrik", "air", "kulkas", "lemari es",
#         "bocor", "mati", "rusak", "lampu"
#     ]

#     housekeeping_keywords = [
#         "handuk", "bersih", "kotor", "sprei",
#         "selimut", "bed", "lantai", "sampah"
#     ]

#     if any(k in message for k in maintenance_keywords):
#         return "maintenance"

#     if any(k in message for k in housekeeping_keywords):
#         return "housekeeping"

#     return "customer_service"


# def find_available_staff(db: Session, role: str):
#     return (
#         db.query(Staff)
#         .join(StaffAttendance, StaffAttendance.staff_id == Staff.id)
#         .filter(
#             Staff.role == role,
#             StaffAttendance.date == date.today(),
#             StaffAttendance.is_present == True
#         )
#         .first()
#     )

# # ======================
# # START TICKET
# # ======================
# @router.post("/tickets/{ticket_id}/start")
# def start_ticket(ticket_id: int, db: Session = Depends(get_db)):
#     ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

#     if not ticket:
#         raise HTTPException(status_code=404, detail="ticket not found")

#     if ticket.started_at is not None:
#         raise HTTPException(status_code=400, detail="ticket already started")

#     if ticket.done_at is not None:
#         raise HTTPException(status_code=400, detail="ticket already done")

#     ticket.status = "in_progress"
#     ticket.started_at = datetime.utcnow()

#     db.commit()
#     db.refresh(ticket)

#     return {
#         "ticket_id": ticket.id,
#         "status": ticket.status,
#         "started_at": ticket.started_at
#     }


# # ======================
# # CREATE TICKET
# # ======================
# @router.post("/tickets")
# def create_ticket(message: str, db: Session = Depends(get_db)):
#     role = detect_role(message)

#     staff = find_available_staff(db, role)

#     ticket = Ticket(
#         message=message,
#         status="assigned" if staff else "unassigned",
#         assigned_staff_id=staff.id if staff else None
#     )

#     db.add(ticket)
#     db.commit()
#     db.refresh(ticket)

#     return {
#         "ticket_id": ticket.id,
#         "status": ticket.status,
#         "assigned_role": role,
#         "assigned_staff": staff.name if staff else None
#     }

# # ======================
# # DONE TICKET
# # ======================
# @router.post("/tickets/{ticket_id}/done")
# def done_ticket(ticket_id: int, db: Session = Depends(get_db)):
#     ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

#     if not ticket:
#         raise HTTPException(status_code=404, detail="ticket not found")

#     if ticket.status != "in_progress":
#         raise HTTPException(
#             status_code=400,
#             detail=f"ticket status must be in_progress, current: {ticket.status}"
#         )

#     ticket.status = "done"
#     ticket.done_at = datetime.utcnow()

#     db.commit()
#     db.refresh(ticket)

#     return {
#         "ticket_id": ticket.id,
#         "status": ticket.status,
#         "done_at": ticket.done_at
#     }

# @router.get("/tickets")
# def list_tickets(db: Session = Depends(get_db)):
#     tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
#     return [
#         {
#             "id": t.id,
#             "message": t.message,
#             "status": t.status,
#             "assigned_staff_id": t.assigned_staff_id,
#             "created_at": t.created_at,
#             "started_at": t.started_at,
#             "done_at": t.done_at,
#         }
#         for t in tickets
#     ]

# @router.post("/tickets/{ticket_id}/start")
# def start_ticket(ticket_id: int, db: Session = Depends(get_db)):
#     ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")

#     ticket.status = "started"
#     ticket.started_at = datetime.utcnow()
#     db.commit()
#     db.refresh(ticket)

#     return {
#         "ticket_id": ticket.id,
#         "status": ticket.status,
#         "started_at": ticket.started_at,
#     }

# @router.post("/tickets/{ticket_id}/done")
# def finish_ticket(ticket_id: int, db: Session = Depends(get_db)):
#     ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")

#     ticket.status = "done"
#     ticket.done_at = datetime.utcnow()
#     db.commit()
#     db.refresh(ticket)

#     return {
#         "ticket_id": ticket.id,
#         "status": ticket.status,
#         "done_at": ticket.done_at,
#     }
         

# # ======================
# # GET ALL TICKETS
# # ======================
# @router.get("/tickets")
# def get_tickets(db: Session = Depends(get_db)):
#     return db.query(Ticket).all()


# # ======================
# # GET TICKET BY ID
# # ======================
# @router.get("/tickets/{ticket_id}")
# def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
#     ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
#     # if not ticket:
#     #     return {"error": "ticket not found"}
#     if not ticket:
#         raise HTTPException(status_code=404, detail="ticket not found")
#     return ticket


# # ======================
# # GET TICKETS BY STAFF
# # ======================
# @router.get("/staff/{staff_id}/tickets")
# def get_tickets_by_staff(staff_id: int, db: Session = Depends(get_db)):
#     return db.query(Ticket).filter(
#         Ticket.assigned_staff_id == staff_id
#     ).all()

# from app.server.auth import get_current_auth
# from fastapi import Depends

# @router.get("/auth-test")
# def auth_test(auth = Depends(get_current_auth)):
#     return {
#         "status": "ok",
#         "auth": auth
#     }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, datetime
from pydantic import BaseModel

from app.db import get_db
from app.models.ticket import Ticket
from app.models.staff import Staff
from app.models.staff_attendance import StaffAttendance
from app.models.audit_log import AuditLog
from app.server.auth import get_current_auth

router = APIRouter()
ROLE_SUPERVISOR = "supervisor"


# ======================
# SCHEMAS
# ======================
class ReassignRequest(BaseModel):
    staff_id: int


# ======================
# AUTH TEST
# ======================
@router.get("/auth-test")
def auth_test(auth=Depends(get_current_auth)):
    return {"status": "ok", "auth": auth}


# ======================
# UTIL
# ======================
def detect_role(message: str) -> str:
    message = message.lower()
    if any(k in message for k in ["ac", "listrik", "air", "kulkas", "lemari es", "bocor", "mati", "rusak", "lampu"]):
        return "maintenance"
    if any(k in message for k in ["handuk", "bersih", "kotor", "sprei", "selimut", "bed", "lantai", "sampah"]):
        return "housekeeping"
    return "customer_service"


def find_available_staff(db: Session, role: str):
    return (
        db.query(Staff)
        .join(StaffAttendance, StaffAttendance.staff_id == Staff.id)
        .filter(
            Staff.role == role,
            StaffAttendance.date == date.today(),
            StaffAttendance.is_present.is_(True),
        )
        .first()
    )


def get_staff_attendance_today(db: Session, staff_id: int):
    return (
        db.query(StaffAttendance)
        .filter(
            StaffAttendance.staff_id == staff_id,
            StaffAttendance.date == date.today(),
        )
        .first()
    )


# ======================
# CREATE TICKET (PUBLIC)
# ======================
@router.post("/tickets")
def create_ticket(message: str, db: Session = Depends(get_db)):
    role = detect_role(message)
    staff = find_available_staff(db, role)

    ticket = Ticket(
        message=message,
        status="assigned" if staff else "unassigned",
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


# ======================
# LIST TICKETS (RBAC)
# ======================
@router.get("/tickets")
def list_tickets(auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    query = db.query(Ticket).order_by(Ticket.created_at.desc())
    if auth["role"] != ROLE_SUPERVISOR:
        query = query.filter(Ticket.assigned_staff_id == auth["staff_id"])

    return query.all()


# ======================
# 🚨 NEEDS ATTENTION (SUPERVISOR)
# ======================
@router.get("/tickets/needs-attention")
def tickets_needing_attention(auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    if auth["role"] != ROLE_SUPERVISOR:
        raise HTTPException(403, "only supervisor")

    today = date.today()
    tickets = (
        db.query(Ticket)
        .outerjoin(
            StaffAttendance,
            and_(
                StaffAttendance.staff_id == Ticket.assigned_staff_id,
                StaffAttendance.date == today,
            ),
        )
        .filter(
            Ticket.status != "done",
            or_(
                Ticket.assigned_staff_id.is_(None),
                StaffAttendance.is_present.is_(False),
                StaffAttendance.id.is_(None),
            ),
        )
        .order_by(Ticket.created_at.asc())
        .all()
    )
    return tickets


# ======================
# 🧾 AUDIT LOG (SUPERVISOR)
# ======================
@router.get("/audit-logs")
def get_audit_logs(auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    if auth["role"] != ROLE_SUPERVISOR:
        raise HTTPException(403, "forbidden")

    return (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )


# ======================
# GET SINGLE TICKET (DINAMIS DI BAWAH!)
# ======================
@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "ticket not found")

    if auth["role"] != ROLE_SUPERVISOR and ticket.assigned_staff_id != auth["staff_id"]:
        raise HTTPException(403, "not your ticket")

    return ticket


# ======================
# START TICKET
# ======================
@router.post("/tickets/{ticket_id}/start")
def start_ticket(ticket_id: int, auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "ticket not found")

    if auth["role"] != ROLE_SUPERVISOR and ticket.assigned_staff_id != auth["staff_id"]:
        raise HTTPException(403, "not your ticket")

    if auth["role"] != ROLE_SUPERVISOR:
        attendance = get_staff_attendance_today(db, auth["staff_id"])
        if not attendance or not attendance.is_present:
            raise HTTPException(403, "staff not allowed today")

    if ticket.started_at:
        raise HTTPException(400, "ticket already started")

    ticket.status = "in_progress"
    ticket.started_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket


# ======================
# DONE TICKET
# ======================
@router.post("/tickets/{ticket_id}/done")
def done_ticket(ticket_id: int, auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "ticket not found")

    if auth["role"] != ROLE_SUPERVISOR and ticket.assigned_staff_id != auth["staff_id"]:
        raise HTTPException(403, "not your ticket")

    if ticket.status != "in_progress":
        raise HTTPException(400, "ticket must be in_progress")

    ticket.status = "done"
    ticket.done_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket


# ======================
# REASSIGN TICKET
# ======================
@router.post("/tickets/{ticket_id}/reassign")
def reassign_ticket(ticket_id: int, payload: ReassignRequest, auth=Depends(get_current_auth), db: Session = Depends(get_db)):
    if auth["role"] != ROLE_SUPERVISOR:
        raise HTTPException(403, "only supervisor")

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "ticket not found")

    attendance = get_staff_attendance_today(db, payload.staff_id)
    if not attendance or not attendance.is_present:
        raise HTTPException(400, "target staff not on duty")

    old_staff_id = ticket.assigned_staff_id
    ticket.assigned_staff_id = payload.staff_id
    ticket.status = "assigned"

    db.add(AuditLog(
        actor_id=auth["staff_id"],
        actor_role=auth["role"],
        action="reassign_ticket",
        ticket_id=ticket.id,
        from_staff_id=old_staff_id,
        to_staff_id=payload.staff_id,
    ))
    db.commit()
    db.refresh(ticket)
    return ticket
