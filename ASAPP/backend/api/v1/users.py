from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.user_schema import UserRegisterRequest
from db.pg_db_conn import get_db
from services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserRegisterRequest)
async def register_user(request: UserRegisterRequest,
    session: AsyncSession = Depends(get_db)):

    service = UserService(session)
    try:
        user = await service.create_user(
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to create user")
