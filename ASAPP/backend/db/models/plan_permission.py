from enum import Enum as PyEnum
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base


class RoleEnum(PyEnum):
    ADMIN = "admin"  # Full access
    EDITOR = "editor"  # Can create/edit own plans and tasks
    VIEWER = "viewer"  # Read-only access


class PlanPermission(Base):
    __tablename__ = "plan_permissions"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID, ForeignKey("plans.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.VIEWER)
    granted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plan_permissions")
    plan = relationship("Plan", back_populates="permissions")