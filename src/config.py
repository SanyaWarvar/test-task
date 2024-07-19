from pytz import timezone
from os import getenv
from dotenv import load_dotenv

load_dotenv()

CURRENCY_API = "https://cbr.ru/scripts/XML_daily.asp"
TIMEZONE = timezone('Europe/Moscow')
DATE_FORMAT = "%d.%m.%Y"

TOKEN_BOT_API = getenv("BOT_TOKEN")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")