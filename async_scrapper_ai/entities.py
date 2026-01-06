
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from database import Base

class ModelUsage(Base):
    __tablename__ = "model_usage"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    ip = Column(String)
    model = Column(String, nullable=False)
    req_tokens = Column(Integer, nullable=False)
    res_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelTrace(Base):
    __tablename__ = "model_trace"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, ForeignKey("model_usage.request_id"), unique=True, nullable=False)
    source_url = Column(String)
    prompt = Column(Text, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


