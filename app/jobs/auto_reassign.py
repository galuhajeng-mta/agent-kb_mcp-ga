from datetime import date
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.staff import Staff
from app.models.staff_attendance import StaffAttendance
from app.models.audit_log import AuditLog


def auto_reassign_tickets(db: Session):
    today = date.today()

    # 1. ambil ticket yang belum selesai & punya staff
    tickets = (
        db.query(Ticket)
        .filter(
            Ticket.status != "done",
            Ticket.assigned_staff_id.isnot(None)
        )
        .all()
    )

    for ticket in tickets:
        staff_id = ticket.assigned_staff_id

        # 2. cek apakah staff hadir hari ini
        is_present = (
            db.query(StaffAttendance)
            .filter(
                StaffAttendance.staff_id == staff_id,
                StaffAttendance.date == today,
                StaffAttendance.is_present.is_(True)
            )
            .first()
        )

        if is_present:
            continue  # staff masuk → skip

        # 3. cari staff pengganti (role sama & hadir)
        old_staff = db.query(Staff).filter(Staff.id == staff_id).first()

        replacement = (
            db.query(Staff)
            .join(StaffAttendance, StaffAttendance.staff_id == Staff.id)
            .filter(
                Staff.role == old_staff.role,
                StaffAttendance.date == today,
                StaffAttendance.is_present.is_(True)
            )
            .first()
        )

        old_staff_id = ticket.assigned_staff_id

        if replacement:
            ticket.assigned_staff_id = replacement.id
            ticket.status = "assigned"
        else:
            ticket.assigned_staff_id = None
            ticket.status = "unassigned"

        # 4. audit log
        audit = AuditLog(
            actor_id=0,  # system
            actor_role="system",
            action="auto_reassign_due_to_absence",
            ticket_id=ticket.id,
            from_staff_id=old_staff_id,
            to_staff_id=replacement.id if replacement else None,
        )

        db.add(audit)

    db.commit()
