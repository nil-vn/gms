from main import _app
from app.utils.db import db
from app.admin.models import Car, Transaction
from app.utils.constants import CarSituation, TransactionStatus

def fix_db():
    with _app.app_context():
        # Fix Car Situation mapping
        # Maps value (English string) back to Name (e.g. 'REFURBISHED')
        car_val_to_name = {s.value: s.name for s in CarSituation}
        cars = Car.query.all()
        for car in cars:
            # If car_situation in DB matches one of the values, swap it to name
            if car.car_situation in car_val_to_name:
                car.car_situation = car_val_to_name[car.car_situation]
        
        # Also fix Transaction Status
        tx_val_to_name = {s.value: s.name for s in TransactionStatus}
        txs = Transaction.query.all()
        for tx in txs:
            if tx.status in tx_val_to_name:
                tx.status = tx_val_to_name[tx.status]

        db.session.commit()
        print("Fixed enums in DB")

if __name__ == '__main__':
    fix_db()
