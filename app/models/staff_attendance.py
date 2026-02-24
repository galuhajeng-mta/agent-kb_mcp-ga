from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from app.models.base import Base

class StaffAttendance(Base):
    __tablename__ = "staff_attendance"

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, default=True)
