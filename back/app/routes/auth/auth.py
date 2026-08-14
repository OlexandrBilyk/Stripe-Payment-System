from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.core import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, FRONTEND_URL
from app.db import get_db
from app.models import Customer, OAuthAccount, Cart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.auth import encode_token, verify_user, verify_token
from app.services.cookies import set_cookies

router = APIRouter()
oauth: OAuth = OAuth()

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account"
    }
)


@router.get('/google/login')
async def google_login(req: Request):
    redirect_url = req.url_for('google_callback')

    return await oauth.google.authorize_redirect(req, redirect_url)


@router.get('/google/callback')
async def google_callback(req: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(req)

    user_info: dict = token.get('userinfo')

    if user_info:
        email = user_info.get('email')
        name = user_info.get('name')
        provider_id = user_info.get('sub')

        customer = (await db.execute(select(Customer).where(Customer.email == email))).scalar_one_or_none()

        if not customer:
            customer = Customer(
                name=name,
                email=email,
            )

            oauth_account = OAuthAccount(
                provider='google',
                provider_id=provider_id,
                customer=customer
            )

            cart = Cart(
                customer=customer
            )

            db.add(customer)
            db.add(oauth_account)
            db.add(cart)

            await db.flush()


        payload = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }

        access_token = encode_token(payload, 'access', 10)
        refresh_token = encode_token(payload, 'refresh', 60 * 24)

        res = RedirectResponse(url=FRONTEND_URL)

        set_cookies(res, access_token, refresh_token)

        return res