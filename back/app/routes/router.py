from fastapi import APIRouter
from .checkout import router as checkout_router

router = APIRouter()

router.include_router(
    checkout_router, 
    prefix='/checkout'
)

