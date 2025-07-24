from telethon import utils

from config import HH_CHANNEL_ID, TARGET_TIME, PROH_BOOST_TIME_START, PROH_BOOST_TIME_END


def is_hh_bot(event):
    '''
    Filter for message handler. Filtering only HH bot.
    '''
    real_id, peer_type = utils.resolve_id(event.chat_id)
    return real_id == HH_CHANNEL_ID


def check_suggested_time(sugg_time):
    '''
    If target time provided checks whether to boost or not
    '''
    if TARGET_TIME:
        if PROH_BOOST_TIME_START < sugg_time < PROH_BOOST_TIME_END:
            return False
    return True
