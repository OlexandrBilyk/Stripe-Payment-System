from fastapi import APIRouter, Depends, Request, HTTPException, Body
from app.models import Customer, Order, Payment, Product
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import stripe
from app.core import STRIPE_WEBHOOK_SECRET


router = APIRouter()


@router.post('/order')
async def order(product_id: int = Body(...), db: AsyncSession = Depends(get_db)):
    product = (await db.execute(select(Product).where(Product.id == product_id))).scalars().first()

    if product:
        payment_intent = stripe.PaymentIntent.create(
            amount=product.price * 100,
            currency='usd',
        )

        new_order = Order(
            name=product.name,
            customer_id=1
        )

        new_payment = Payment(
            order=new_order,            
            stripe_id=payment_intent.id,
            status=payment_intent.status,
        )

        db.add(new_order)
        db.add(new_payment)
        
        await db.flush()

        res = {
            'id': payment_intent.id,
            'status': payment_intent.status,
            'client_secret': payment_intent.client_secret
        }

        return res


@router.post('/webhook')
async def webhook(req: Request, db: AsyncSession = Depends(get_db)):
    payload = await req.body()

    signature = req.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=STRIPE_WEBHOOK_SECRET
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid payload"
        )
    except stripe.SignatureVerificationError:
        raise HTTPException(
            status_code=400,
            detail="Invalid signature"
        )


    event_type = event['type']

    if event_type == 'payment_intent.succeeded':
        payment_intent = event['data']['object']

        stripe_id = payment_intent['id']

        payment = (await db.execute(select(Payment).options(selectinload(Payment.order)).where(Payment.stripe_id == stripe_id))).scalars().first()

        if payment:
            payment.status = 'succeeded'

            payment.order.status = 'paid'



    return {"received": True}