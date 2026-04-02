from fastapi import APIRouter, Depends
from db.token_schema import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login():
    pass
