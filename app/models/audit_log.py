from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, nullable=False)      # siapa (staff_id / supervisor_id)
    actor_role = Column(String, nullable=False)     # supervisor / staff
    action = Column(String, nullable=False)         # reassign_ticket
    ticket_id = Column(Integer, nullable=False)

    from_staff_id = Column(Integer, nullable=True)
    to_staff_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
