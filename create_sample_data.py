
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal, engine
from app.models.user import User
from app.models.record import Record
from app.services.user_service import create_user
from app.schemas.user import UserCreate
from app.services.record_service import create_record
from app.schemas.record import RecordCreate
from sqlalchemy import text
from datetime import date, timedelta

def main():
    db = SessionLocal()
    try:
        # Create 100+ sample users (large dataset)
        roles = ['viewer'] * 40 + ['analyst'] * 35 + ['admin'] * 25
        import random
        import string
        def random_email():
            name = ''.join(random.choices(string.ascii_lowercase, k=8))
            return f'{name}@{random.choice(["test.com", "finance.com", "user.com"])}'
        
        users = []
        for role in roles:
            email = random_email()
            users.append(UserCreate(email=email, role=role))
        
        user_ids = []
        for u in users:
            try:
                user = create_user(db, u)
                user_ids.append(user.id)
                print(f'Created {u.email[:20]}... ({role}) ID: {user.id}')
            except Exception:
                # Skip dupe
                pass

        # Sample records
        records = [
            RecordCreate(amount=5000.0, type='income', category='Salary', date=date.today(), notes='Monthly salary'),
            RecordCreate(amount=1200.0, type='expense', category='Rent', date=date.today(), notes='Apartment rent'),
            RecordCreate(amount=300.0, type='expense', category='Groceries', date=date.today() - timedelta(days=3), notes='Weekly shopping'),
            RecordCreate(amount=1500.0, type='income', category='Freelance', date=date.today() - timedelta(days=10), notes='Project payment'),
        ]
        for i, r in enumerate(records):
            create_record(db, r, user_ids[i % len(user_ids)])
            print(f'Created record: ${r.amount} {r.type} - {r.category}')

        print('\nSample data created! Open dashboard to view.')
    finally:
        db.close()

if __name__ == '__main__':
    main()

