import os
from dotenv import load_dotenv

if os.getenv('RUNNING_IN_DOCKER'):
	load_dotenv('.env.docker')
else:
	load_dotenv('.env.local')

APPLICATION_SECRET_KEY = os.getenv('DB_URI')
DB_URI = os.getenv('DB_URI')
PROXY_HTTPS = os.getenv('PROXY_HTTPS')
PROXY_HTTP = os.getenv('PROXY_HTTP')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
BACKEND_DIR = os.getenv('BACKEND_DIR')
PROJECT_PATHS= os.getenv('PROJECT_PATHS')
GOOGLE_APP_PW = os.getenv('GOOGLE_APP_PW')
GOOGLE_SENDER_EMAIL = os.getenv('GOOGLE_SENDER_EMAIL')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
