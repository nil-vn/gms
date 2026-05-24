from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.utils import db
from .base import BaseModel

class TransactionFile(BaseModel):
    __tablename__ = "transaction_file"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transaction.id", ondelete="CASCADE"), nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    original_name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(default=datetime.utcnow)

    transaction = relationship("Transaction", back_populates="files")

    def __repr__(self):
        return f"<TransactionFile {self.id} for Transaction {self.transaction_id}>"
