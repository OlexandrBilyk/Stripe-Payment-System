from dotenv import load_dotenv
import os

load_dotenv()

STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
STRIPE_API_SECRET = os.getenv('STRIPE_SECRET_KEY')
DB_URL = os.getenv('DB_URL')
