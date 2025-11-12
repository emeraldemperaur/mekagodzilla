# Mercurius API Database Models
from pydantic import EmailStr
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Text
import datetime as dt
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(4096), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="admin", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now(dt.timezone.utc), nullable=False)
    artifacts: Mapped[list["Artifact"]] = relationship("Artifact", back_populates="owner", cascade="all, delete-orphan")

class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), unique=False, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now(dt.UTC), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    owner: Mapped[User] = relationship("User", back_populates="artifacts")