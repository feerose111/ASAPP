from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.user import User
from utils.security import verify_password
from fastapi import HTTPException


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user by email and password"""

        # Fetch user from database
        stmt = select(User).where(User.email == email)  # type: ignore
        result = await self.session.execute(stmt)
        user = result.scalar()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Check if user is active
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")

        return user

    async def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        stmt = select(User).where(User.email == email)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_by_id(self, user_id: str) -> User:
        """Get user by ID"""
        stmt = select(User).where(User.id == user_id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar()