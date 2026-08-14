from dotenv import load_dotenv
import os

load_dotenv()
DEBUG = os.getenv('DEBUG')

FRONTEND_URL = os.getenv('FRONTEND_URL')

SESSION_SECRET_KEY=os.getenv('SESSION_SECRET_KEY')

STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
STRIPE_API_SECRET = os.getenv('STRIPE_SECRET_KEY')

DB_URL = os.getenv('DB_URL')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')