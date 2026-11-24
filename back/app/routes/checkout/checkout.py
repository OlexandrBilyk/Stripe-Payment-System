from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.models import Customer, Order, OrderItem, Payment, Product, Cart, CartItem, OrderStatus, PaymentStatus
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import stripe
from stripe import StripeClient
from app.core import STRIPE_WEBHOOK_SECRET, STRIPE_API_SECRET
from app.services.auth import verify_user

router = APIRouter()

stripe_client = StripeClient(STRIPE_API_SECRET)


@router.post('/order')
async def order(
    db: AsyncSession = Depends(get_db),
    customer: Customer = Depends(verify_user)
):

    items = customer.cart.cart_items

    if items:
        new_order = Order(
            customer_id=customer.id
        )

        all_price = 0

        for item in items:
            order_item = OrderItem(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            new_order.order_items.append(
                order_item
            )

            all_price += (item.product.price * item.quantity)



        payment_intent = stripe_client.v1.payment_intents.create({
                'amount': all_price,
                'currency':'usd'
        })

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
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cart is empty'
        )


@router.post('/webhook')
async def webhook(
    req: Request, 
    db: AsyncSession = Depends(get_db),
):
    payload = await req.body()

    signature = req.headers.get('STRIPE_SIGNATURE')

    try:
        event = stripe_client.construct_event(
            payload=payload,
            sig_header=signature,
            secret=STRIPE_WEBHOOK_SECRET
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=400,
            detail="Invalid signature"
        )


    event_dict = event.to_dict()

    if event_dict['type'] == 'payment_intent.succeeded':
        payment_intent = event_dict['data']['object']

        stripe_id = payment_intent['id']

        payment = (
            await db.execute(
                select(Payment)
                .options(
                    selectinload(Payment.order)
                )
                .where(Payment.stripe_id == stripe_id)
            )
        ).scalar_one_or_none()

        if payment:
            payment.status = PaymentStatus.SUCCEEDED

            payment.order.status = OrderStatus.PAID

            cart = payment.order.customer.cart

            for item in cart.cart_items:
                await db.delete(item)

                
    elif event_dict['type'] == 'payment_intent.payment_failed':
        payment_intent = event_dict['data']['object']

        stripe_id = payment_intent['id']

        payment = (await db.execute(select(Payment).options(selectinload(Payment.order)).where(Payment.stripe_id == stripe_id))).scalar_one_or_none()

        if payment:
            payment.status = payment_intent['status']

            payment.order.status = OrderStatus.PENDING


    return {"received": True}