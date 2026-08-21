from fastapi import HTTPException, Request, status, Depends
from app.core import JWT_SECRET_KEY, JWT_ALGORITHM
from app.db import get_db
from app.models import Customer, Cart, CartItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from jwt import PyJWTError
import jwt
from datetime import datetime, timezone, timedelta


def encode_token(data: dict, type: str, exp: int):
    payload = data.copy()
    payload['type'] = type
    payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(minutes=exp)

    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    try:
        paylod = jwt.decode(jwt=token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        return paylod
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )


async def verify_user(req: Request, db: AsyncSession = Depends(get_db)):
    access_token = req.cookies.get('access_token')

    creditials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    if access_token:
        payload = verify_token(access_token)

        customer_id = payload.get('id')

        if not customer_id: raise creditials_exception

        customer = (
            await db.execute(
                select(Customer)
                .where(Customer.id == customer_id)
                .options(
                    selectinload(Customer.cart)
                    .selectinload(Cart.cart_items)
                    .selectinload(CartItem.product),
                    
                    selectinload(Customer.orders),

                )
            )
        ).scalar_one_or_none()

        if not customer: raise creditials_exception

        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token'
        )