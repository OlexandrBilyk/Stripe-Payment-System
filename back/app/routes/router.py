from fastapi import APIRouter
from .checkout import router as checkout_router
from .auth import router as auth_router
from .profile import router as profile_router

router = APIRouter()

router.include_router(
    checkout_router, 
    prefix='/checkout',
    tags=['Checkout']
)

router.include_router(
    auth_router, 
    prefix='/auth',
    tags=['Auth']
)

router.include_router(
    profile_router, 
    prefix='/profile',
    tags=['Profile']
)

