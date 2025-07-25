from datetime import date, datetime, timedelta

from config import HH_BOT_USERNAME, TARGET_TIME, PROH_BOOST_TIME_START, PROH_BOOST_TIME_END, MSK_TIMEZONE


async def is_hh_bot(event):
    '''
    Filter for message handler. Filtering only HH bot.
    '''
    chat = await event.get_chat()
    return chat.username == HH_BOT_USERNAME


def check_suggested_time(sugg_time=None):
    '''
    If target time provided checks whether to boost or not
    '''
    if TARGET_TIME:
        if not sugg_time:
            sugg_time = datetime.now(MSK_TIMEZONE).time()

        # Вторым условием проверяем случай, когда PROH_BOOST_TIME_END в начале следующего дня
        if PROH_BOOST_TIME_START <= sugg_time <= PROH_BOOST_TIME_END or \
                PROH_BOOST_TIME_END < PROH_BOOST_TIME_START and PROH_BOOST_TIME_START <= sugg_time:
            return False
    return True


def get_sleep_time():
    datetime_now = datetime.now()
    datetime_target = datetime.combine(date.today(), TARGET_TIME)

    if TARGET_TIME < datetime_now.time():
        datetime_target += timedelta(days=1)

    return (datetime_target - datetime_now).total_seconds()
