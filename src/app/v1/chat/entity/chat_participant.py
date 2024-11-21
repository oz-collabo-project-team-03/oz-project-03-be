from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rooms.id"), nullable=False)