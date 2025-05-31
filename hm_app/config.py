import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


ACCESS_TOKEN_EXPIRE_MINUTES = 40
REFRESH_TOKEN_EXPIRE_DAYS = 30
ALGORITHM = 'HS256'