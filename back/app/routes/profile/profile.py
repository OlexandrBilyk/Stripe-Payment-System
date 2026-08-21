from fastapi import APIRouter, HTTPException, Depends, status
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Cart, CartItem, Customer, Product
from app.services.auth import verify_user
from app.schemas.customer import CustromerResponse, CartItemCreate, CartResponse

router = APIRouter()


@router.get('/profile', response_model=CustromerResponse)
async def get_profile(
    db: AsyncSession = Depends(get_db),
    customer: Customer = Depends(verify_user),
):
    return customer 


@router.post('/cart', response_model=CartResponse)
async def add_cart_item(
    data: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    customer: Customer = Depends(verify_user),
):
    product = (
        await db.execute(
            select(Product)
            .where(Product.id == data.product_id)
        )
    ).scalar_one_or_none()

    if product:
        new_cart_item = CartItem(
            cart=customer.cart,
            product=product,
            quantity=data.quantity
        )

        db.add(new_cart_item)

        await db.flush()

        return customer.cart
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )