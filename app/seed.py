import os
from dotenv import load_dotenv

from app.database import SessionLocal
from app.models import User
from app.core.password import hash_password

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def create_admin():
    db = SessionLocal()

    existing = db.query(User).filter(User.username == USERNAME).first()
    if existing:
        print("Admin already exists")
        return

    user = User(
        username=USERNAME,
        hashed_password=hash_password(PASSWORD)
    )

    db.add(user)
    db.commit()
    db.close()

    print("Admin created")


if __name__ == "__main__":
    create_admin()
