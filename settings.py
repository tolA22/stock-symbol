import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
FINNHUB_BASE_URL = os.environ.get('FINNHUB_BASE_URL')
