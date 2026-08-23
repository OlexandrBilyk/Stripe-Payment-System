from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from app.core import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, FRONTEND_URL
from app.db import get_db
from app.models import Customer, OAuthAccount, Cart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.auth import encode_token, verify_user, verify_token
from app.services.cookies import set_cookies
from app.services.security import hash_password, verify_password
from app.schemas.customer import CustomerCreate, CustromerResponse, CustomerLogin


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
async def google_login(
    req: Request
):
    redirect_url = req.url_for('google_callback')

    return await oauth.google.authorize_redirect(req, redirect_url)


@router.get('/google/callback')
async def google_callback(
    req: Request, 
    db: AsyncSession = Depends(get_db)
):
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


@router.post('/register')
async def register(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    data: dict = data.model_dump()

    password = data.get('password')    

    data.pop('password')

    hashed_password = hash_password(password)

    new_customer = Customer(
        **data,
        password=hashed_password
    )

    cart = Cart(
        customer=new_customer
    )

    db.add(new_customer)
    db.add(cart)

    await db.flush()

    payload = {
        'id': new_customer.id,
        'name': new_customer.name,
        'email': new_customer.email
    }
    
    access_token = encode_token(payload, 'access', 10)
    refresh_token = encode_token(payload, 'refresh', 60 * 24)

    res = JSONResponse(
        status_code=status.HTTP_200_OK,
        content='Register successful'
    )

    set_cookies(res, access_token, refresh_token)

    return res


@router.post('/login')
async def login(
    data: CustomerLogin, 
    db: AsyncSession = Depends(get_db)
):

    email = data.email
    password = data.password

    customer = (await db.execute(select(Customer).where(Customer.email == email))).scalar_one_or_none()

    if customer:
        is_valid = verify_password(password, customer.password)

        if is_valid:
            payload = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email
            }
            
            access_token = encode_token(payload, 'access', 10)
            refresh_token = encode_token(payload, 'refresh', 60 * 24)

            res = JSONResponse(
                status_code=status.HTTP_200_OK,
                content='Login successful'
            )

            set_cookies(res, access_token, refresh_token)

            return res
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect password'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )


@router.get('/logout')
async def logout():
    res = JSONResponse(
        status_code=status.HTTP_200_OK,
        content='Logout successful'
    )

    res.delete_cookie('access_token')
    res.delete_cookie('refresh_token')

    return res


@router.get('/refresh')
async def refresh(
    req: Request
):
    refresh = req.cookies.get('refresh_token')

    payload = verify_token(refresh)

    access_token = encode_token(payload, 'access', 10)
    refresh_token = encode_token(payload, 'refresh', 60 * 24)

    res = JSONResponse(
        status_code=status.HTTP_200_OK,
        content='Tokens refreshed successfully'
    )

    set_cookies(res, access_token, refresh_token)

    return res
  