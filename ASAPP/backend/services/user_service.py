from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.user import User
from utils.security import get_password_hash

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str, full_name: str) -> User:

        # Check if user already exists
        stmt = select(User).filter(User.email == email) # type: ignore
        result = await self.session.execute(stmt)
        existing_user = result.scalar()

        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        # Hash password
        password_hash = get_password_hash(password)

        # Create user
        new_user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user