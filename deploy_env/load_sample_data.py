import asyncio
from uuid import uuid4
from datetime import datetime
from foodshareapp.db.models.user import insert_user, get_user_by_email
from foodshareapp.db.utils import db
from foodshareapp.app.api.services.crypto import gen_salt, hash_password
from pydantic import EmailStr


async def check_existing_data():
    """Check if data already exists in the database."""
    user = await get_user_by_email("user1@example.com")
    return user is not None


async def generate_sample_users():
    """Creates sample users if they don't already exist."""
    if await check_existing_data():
        print("⚠️ Sample data already exists, skipping insert.")
        return

    users = [
        {
            "uuid": uuid4(),
            "email": EmailStr(f"user{i}@example.com"),
            "username": f"user{i}",
            "firstname": f"First{i}",
            "lastname": f"Last{i}",
            "salt": gen_salt(),
            "password": hash_password(f"password{i}", gen_salt()),
            "last_login": datetime.utcnow(),
        }
        for i in range(1, 6)
    ]

    async with db.transaction():
        for user in users:
            await insert_user(user)

    print("✅ Sample data loaded successfully!")


async def main():
    await db.connect()
    await generate_sample_users()
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
