from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import stripe
from app.core import STRIPE_API_SECRET
from .routes.router import router

stripe.api_key = STRIPE_API_SECRET

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


app.include_router(router)
