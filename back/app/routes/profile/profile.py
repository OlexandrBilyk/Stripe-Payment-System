from fastapi import APIRouter, HTTPException, Depends, status, Body
from fastapi.responses import JSONResponse
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Cart, CartItem, Customer, Product
from app.services.auth import verify_user
from app.services.security import verify_password, hash_password
from app.schemas.customer import CustromerResponse, CartItemCreate, CartResponse, ChangePassword

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


@router.post('/add-password')
async def add_password(
    new_password: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    customer: Customer = Depends(verify_user)
):
    if customer.password: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with such a password already exists'
        )

    new_hashed_password = hash_password(new_password)

    customer.password = new_hashed_password

    await db.flush()


    res = JSONResponse(
        content={
            'message': 'Added password successful'
        },
        status_code=status.HTTP_200_OK
    )

    return res
    


@router.post('/change-password')
async def change_password(
    data: ChangePassword,
    db: AsyncSession = Depends(get_db),
    customer: Customer = Depends(verify_user)
):
    if not customer.password: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User does not have a password'
        )
    
    is_password = verify_password(data.old_password, customer.password) 

    if is_password:
        new_hashed_password = hash_password(data.new_password)

        customer.password = new_hashed_password

        await db.flush()

        res = JSONResponse(
            content={
                'message': 'Changed password successful'
            },
            status_code=status.HTTP_200_OK
        )

        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Old password is incorrect'
        )
