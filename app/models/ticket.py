from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
# from datetime import datetime
from app.models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    status = Column(String, nullable=False, default="assigned")
    assigned_staff_id = Column(Integer, ForeignKey("staff.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=False), default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=False), nullable=True)
    done_at = Column(DateTime(timezone=False), nullable=True)
 
    def __repr__(self):
        return f"<Ticket id={self.id} status={self.status}>"