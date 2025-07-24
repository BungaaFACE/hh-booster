from datetime import date, datetime, time, timedelta
from telethon import utils

from config import HH_BOT_USERNAME, TARGET_TIME, PROH_BOOST_TIME_START, PROH_BOOST_TIME_END, MSK_TIMEZONE


def is_hh_bot(event):
    '''
    Filter for message handler. Filtering only HH bot.
    '''
    return event.chat.username == HH_BOT_USERNAME


def check_suggested_time(sugg_time=None):
    '''
    If target time provided checks whether to boost or not
    '''
    if TARGET_TIME:
        if not sugg_time:
            sugg_time = datetime.now(MSK_TIMEZONE).time()

        if PROH_BOOST_TIME_START < sugg_time < PROH_BOOST_TIME_END:
            return False
    return True


def get_sleep_time():
    datetime_now = datetime.now()
    datetime_target = datetime.combine(date.today(), TARGET_TIME)

    if TARGET_TIME < datetime_now.time():
        datetime_target += timedelta(days=1)

    return (datetime_target - datetime_now).total_seconds()
