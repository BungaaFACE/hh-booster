from datetime import datetime, timedelta, timezone, time, date
import dotenv
import os

MSK_TIMEZONE = timezone(timedelta(hours=3), "Moscow")
TIME_PATTERN = r'\b([01]?[0-9]|2[0-3]):([0-5][0-9])\b'
COOLDOWN_HOURS = timedelta(hours=4)

dotenv.load_dotenv('.env', override=True)

HH_CHANNEL_ID = int(os.getenv('HH_CHANNEL_ID', 827954988))
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

tt_hours, tt_minutes = map(int, os.getenv('TARGET_TIME', '09:00').split(':'))
TARGET_TIME = time(hour=tt_hours, minute=tt_minutes)
TARGET_TIME_DELTA = timedelta(minutes=int(os.getenv('TARGET_TIME_DELTA', '10')))


TARGET_DATETIME = datetime.combine(date.today(), TARGET_TIME)
PROH_BOOST_TIME_START = (TARGET_DATETIME - COOLDOWN_HOURS + TARGET_TIME_DELTA).time()
PROH_BOOST_TIME_END = (TARGET_DATETIME - TARGET_TIME_DELTA).time()
