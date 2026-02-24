from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base

class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)
