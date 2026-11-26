from fastapi import APIRouter, Depends, HTTPException, status
from app.db import get_db
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import  Product


router = APIRouter()


@router.get('/product')
async def get_products(
    db: AsyncSession = Depends(get_db),
):
    products = (await db.execute(select(Product))).scalars().all()

    if products:
        return products
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No products were found'
        )


@router.get('/product/{id}')
async def get_product_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    product = (await db.execute(select(Product).where(Product.id == id))).scalar_one_or_none()

    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product not found'
        )