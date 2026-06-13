from datetime import datetime
from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import ForeignKey, or_
from app.utils import db
from .base import BaseModel


class RepairOrder(BaseModel):
    __tablename__ = "repair_order"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"), nullable=True)
    car_id: Mapped[Optional[int]] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"), nullable=True)
    
    date_in: Mapped[Optional[str]]
    date_out: Mapped[Optional[str]]
    odometer: Mapped[Optional[int]]
    status: Mapped[Optional[str]]
    symptoms: Mapped[Optional[str]]
    note: Mapped[Optional[str]]
    
    # Quan hệ
    customer = relationship("Customer", back_populates="repair_orders")
    car = relationship("Car", back_populates="repair_orders")
    items = relationship("RepairItem", back_populates="repair_order", cascade="all, delete-orphan")

    created_at: Mapped[str] = mapped_column(default=datetime.utcnow)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items if item.total_price)

    @property
    def status_label(self):
        from app.utils.constants import RepairStatus
        if not self.status:
            return ""
        try:
            return RepairStatus[self.status.upper()].value
        except (KeyError, AttributeError):
            from flask_babel import lazy_gettext as _
            status_map = {
                "pending": _("Pending"),
                "in_progress": _("In Progress"),
                "done": _("Done"),
                "cancelled": _("Cancelled")
            }
            return status_map.get(self.status.lower(), self.status)

    def __repr__(self):
        return f"<RepairOrder {self.id}>"

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, qid):
        return cls.query.get(qid)

    @classmethod
    def search(cls, query):
        # Join may be needed if we want to search by customer name or car license
        from .customer import Customer
        from .car import Car
        return cls.query.outerjoin(Customer).outerjoin(Car).filter(
            or_(
                cls.status.ilike(f"%{query}%"),
                cls.symptoms.ilike(f"%{query}%"),
                Customer.name.ilike(f"%{query}%"),
                Car.license_plate_no.ilike(f"%{query}%"),
                Car.vin.ilike(f"%{query}%"),
            )
        ).all()
