import os
import random
from datetime import datetime, timedelta
from main import _app
from app.utils.db import db
from app.admin.models import Customer, Car, Transaction, User
from app.admin.models.transaction_item import TransactionItem
from app.utils.constants import CarSituation, TransactionStatus

def drop_all():
    print("Clearing old sample data...")
    TransactionItem.query.delete()
    Transaction.query.delete()
    Car.query.delete()
    Customer.query.delete()
    db.session.commit()

def generate_sample_data():
    with _app.app_context():
        # drop_all() # Enable this if we want to reset DB entirely, but let's just append for now.

        print("Generating Customers...")
        customers = []
        lead_sources = ["Facebook", "Website", "Referral", "Walk-in", "Other"]
        for i in range(1, 16):
            c = Customer(
                name=f"Customer {i}",
                phone=f"09012345{i:02d}",
                address=f"123 Street {i}, City",
                lead_source=random.choice(lead_sources),
                birth_day=datetime(1980 + i, (i % 12) + 1, (i % 28) + 1).strftime('%m/%d/%Y'),
                gender=random.choice(["Male", "Female"])
            )
            customers.append(c)
            db.session.add(c)
        db.session.commit()

        print("Generating Cars...")
        cars = []
        situations = list(CarSituation)
        branches = ["Toyota", "Honda", "Ford", "Mazda", "Kia", "Mercedes", "BMW"]
        models = ["Sedan", "SUV", "Hatchback", "Pickup"]
        colors = ["White", "Black", "Silver", "Red", "Blue"]

        for i in range(1, 31):
            car = Car(
                name=f"{random.choice(branches)} {random.choice(models)} 20{random.randint(15, 23)}",
                branch=random.choice(branches),
                model=random.choice(models),
                vin=f"VIN{random.randint(100000, 999999)}XXX",
                color=random.choice(colors),
                imported_date=(datetime.utcnow() - timedelta(days=random.randint(10, 200))).strftime('%m/%d/%Y'),
                year_of_manufacture=f"20{random.randint(15, 23)}",
                car_situation=random.choice(situations).value,
                purchase_price=random.randint(200, 800) * 1000000,
                selling_price=random.randint(300, 1000) * 1000000,
                note="Sample car generated"
            )
            cars.append(car)
            db.session.add(car)
        db.session.commit()

        print("Generating Transactions...")
        now = datetime.utcnow()
        transactions = []
        
        # We need data for the last 6 months for the chart
        for i in range(25):
            c = random.choice(customers)
            car = random.choice(cars)
            
            # Random date within last 180 days
            days_ago = random.randint(1, 175)
            trans_date = now - timedelta(days=days_ago)

            status = random.choice(list(TransactionStatus))
            selling_price = car.selling_price if getattr(car, 'selling_price', None) else random.randint(300, 1000) * 1000000
            
            deposit = 0
            if status == TransactionStatus.DEPOSITED:
                deposit = int(selling_price * 0.1)  # 10% deposit
            elif status == TransactionStatus.PAID:
                deposit = 0 # As requested, if Paid -> 0 or None

            t = Transaction(
                customer_id=c.id,
                purchase_date=trans_date.strftime("%m/%d/%Y"),
                selling_price=selling_price,
                deposit_amount=deposit,
                status=status.value,
                note=f"Sample transaction {i+1}",
                created_at=trans_date
            )
            t.cars.append(car)
            db.session.add(t)
            transactions.append(t)
        db.session.commit()

        print("Generating Transaction Items...")
        items = ["Dashcam", "Floor mats", "Tinted Window", "Ceramic Coating", "Insurance"]
        for t in transactions:
            # Randomly add 0 to 3 items
            num_items = random.randint(0, 3)
            for _ in range(num_items):
                item_name = random.choice(items)
                item_price = random.randint(1, 10) * 500000
                ti = TransactionItem(
                    transaction_id=t.id,
                    name=item_name,
                    price=item_price
                )
                db.session.add(ti)
        db.session.commit()

        print("Successfully generated Sample Data!")

if __name__ == "__main__":
    generate_sample_data()
