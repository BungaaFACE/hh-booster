from datetime import date, datetime, timedelta
from loguru import logger as loguru_logger
import logging
import sys

from config import HH_BOT_USERNAME, TARGET_TIME, PROH_BOOST_TIME_START, PROH_BOOST_TIME_END, MSK_TIMEZONE


async def is_hh_bot(event):
    '''
    Filter for message handler. Filtering only HH bot.
    '''
    chat = await event.get_chat()
    try:
        return chat.username == HH_BOT_USERNAME
    except AttributeError:
        return False


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
    datetime_now = datetime.now(MSK_TIMEZONE)
    datetime_target = datetime.combine(date.today(), TARGET_TIME, MSK_TIMEZONE)

    if TARGET_TIME < datetime_now.time():
        datetime_target += timedelta(days=1)

    return (datetime_target - datetime_now).total_seconds()


def configure_logger():

    class InterceptHandler(logging.Handler):
        '''Rerouting default logging to loguru'''

        def emit(self, record):
            logger_opt = loguru_logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelname, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logging.getLogger(__name__)

    loguru_logger.remove()  # Remove default loguru handler
    log_format = "{time} | {level} | {file} | {line} | {function} | {message} | {extra}"

    # File handler
    loguru_logger.add(f'/data/logs/hh-booster.log',
                      format=log_format,
                      level="INFO",
                      rotation='20 MB',
                      retention='3 days',
                      enqueue=True)

    loguru_logger.add(sys.stdout,
                      format=log_format,
                      level="INFO",
                      enqueue=True)

    return loguru_logger
