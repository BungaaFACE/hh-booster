import re
import asyncio
from loguru import logger
from pprint import pprint
from datetime import date, datetime, time
from telethon import events, TelegramClient

from config import API_ID, API_HASH, HH_CHANNEL_ID, TIME_PATTERN, COOLDOWN_HOURS, MSK_TIMEZONE
from utils import is_hh_bot, check_suggested_time


account_bot = TelegramClient('account_login', API_ID, API_HASH,
                             device_model="Linux 5.15.0", system_version="Ubuntu 22").start()


@account_bot.on(events.NewMessage(func=is_hh_bot))
async def handler(event: events.CallbackQuery.Event):
    # pprint(event.message.__dict__)
    '''
    Примеры ответов:
    Пока рано поднимать резюме — с последнего раза не прошло 4 часа. Давайте я сделаю это за вас в 18:55 (МСК)?

    Ваши резюме поднялись в поиске в 10:35 (МСК).
    ⏳ Поднять снова через 4 часа?
    '''
    message_text = event.message.message
    if 'Давайте я сделаю это за вас в' in message_text or \
            'Поднять снова через' in message_text:

        match = re.search(TIME_PATTERN, message_text)
        hours, minutes = map(int, match.groups())
        time_in_message = time(hour=hours, minute=minutes)

        if 'Поднять снова через' in message_text:
            suggested_boost_time = (datetime.combine(date.today(), time_in_message) + COOLDOWN_HOURS).time()

        elif 'Давайте я сделаю это за вас в' in message_text:
            suggested_boost_time = time_in_message

        if check_suggested_time(suggested_boost_time):
            logger.info(f'Поднимаю резюме в {suggested_boost_time} (МСК)')
            await event.respond('Поднять')


async def main(bot: TelegramClient):
    await bot.send_message(HH_CHANNEL_ID, '/start')
    while True:
        if check_suggested_time(datetime.now(MSK_TIMEZONE).time()):
            await bot.send_message(HH_CHANNEL_ID, 'Главное меню')
            await asyncio.sleep(3)
            await bot.send_message(HH_CHANNEL_ID, 'В начало')
            await asyncio.sleep(3)
            await bot.send_message(HH_CHANNEL_ID, 'Поднять резюме в поиске')
            break

        await asyncio.sleep(30)


if __name__ == '__main__':
    account_bot.loop.run_until_complete(main(account_bot))
    account_bot.run_until_disconnected()
