from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import uuid

Base = declarative_base()

class TimestampMixin:
    """Mixin that adds timestamp columns to models"""
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc),
        server_default=text("TIMEZONE('utc', NOW())")
    )
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=text("TIMEZONE('utc', NOW())")
    )

class BaseModel(Base, TimestampMixin):
    """Base model with UUID primary key and timestamps"""
    __abstract__ = True
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        nullable=False
    )
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name) 
            for column in self.__table__.columns
        }
    
    @classmethod
    def get_by_id(cls, session: Session, id: uuid.UUID):
        """Get record by UUID"""
        return session.query(cls).filter(cls.id == id).first()
    
    def save(self, session: Session):
        """Save the model to database"""
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
