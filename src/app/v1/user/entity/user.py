from datetime import datetime

import ulid  # type: ignore
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.utils.consts import SocialProvider, UserRole
from src.config.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(
        String(26), nullable=False, unique=True, default=lambda: str(ulid.new())  # ULID는 26자 문자열  # ULID 생성
    )
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(13), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    profile_image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    social_provider: Mapped[SocialProvider | None] = mapped_column(
        Enum(SocialProvider, name="social_provider_enum", create_type=False), nullable=True
    )
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role_enum", create_type=False), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    deactivated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_privacy_accepted: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # one-to-one 관계
    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")
    tag = relationship("Tag", back_populates="user", uselist=False, cascade="all, delete-orphan")
