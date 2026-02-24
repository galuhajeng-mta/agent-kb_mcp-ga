from sqlalchemy import Column, Integer, String
from .base import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
