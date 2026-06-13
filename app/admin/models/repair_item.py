from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import ForeignKey
from typing import Optional
from app.utils import db
from .base import BaseModel

class RepairItem(BaseModel):
    __tablename__ = "repair_item"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    repair_order_id: Mapped[Optional[int]] = mapped_column(ForeignKey("repair_order.id", ondelete="CASCADE"), nullable=False)
    
    item_type: Mapped[Optional[str]] # 'PART' or 'LABOR'
    name: Mapped[str]
    quantity: Mapped[Optional[int]]
    unit_price: Mapped[Optional[int]]
    
    repair_order = relationship("RepairOrder", back_populates="items")

    @property
    def total_price(self):
        q = self.quantity or 1
        p = self.unit_price or 0
        return q * p
        
    @property
    def item_type_label(self):
        from app.utils.constants import RepairItemType
        if not self.item_type:
            return ""
        try:
            return RepairItemType[self.item_type.upper()].value
        except (KeyError, AttributeError):
            return self.item_type
