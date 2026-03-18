from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base


class Wallet(Base):

    __tablename__ = "wallets"

    wallet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    balance: Mapped[int] = mapped_column(default=0)
