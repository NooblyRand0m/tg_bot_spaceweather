import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from space_weather import get_eclipse_data, get_solar_activity, get_geo_activity

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def check_kp_index():
    while True:
        kp_index = get_geo_activity()[0]
        if kp_index >= 5:
            await bot.send_message(chat_id='YOUR_CHAT_ID', text=f'Warning: KP index is {kp_index}!')
        await asyncio.sleep(21600)


async def check_solar_activity():
    while True:
        sunspot_class = sunspot_handler()[0]
        if sunspot_class.startswith('M') or sunspot_class.startswith('X'):
            await bot.send_message(chat_id='YOUR_CHAT_ID', text=f'Warning: sunspot class is {sunspot_class}!')
        await asyncio.sleep(21600)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('Hi! I am a space weather bot. Use /help to see what I can do.')


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    help_text = 'I can provide the following information:\n'
    help_text += '/eclipse - information about upcoming solar and lunar eclipses\n'
    help_text += '/sunspot - information about the latest solar flares\n'
    help_text += '/kp - information about the latest KP index\n'
    help_text += '/kp_notify - receive notifications when KP index is 5 or higher\n'
    help_text += '/flare_notify - receive notifications when solar flare of class M or X is detected\n'
    await message.reply(help_text)


@dp.message_handler(commands=['eclipse'])
async def eclipse_handler(message: types.Message):
    eclipse_data = get_eclipse_data()
    await message.reply(eclipse_data)


@dp.message_handler(commands=['sunspot'])
async def sunspot_handler(message: types.Message):
    solar_activity_data = get_solar_activity()
    message_sunspot = f'Latest flare of class {solar_activity_data[0]} occurred on {solar_activity_data[1]}'
    await message.reply(message_sunspot)


@dp.message_handler(commands=['kp'])
async def kp_handler(message: types.Message):
    kp_data = get_geo_activity()
    message_kp = f'KP index on {kp_data[1]} was {kp_data[0]}'
    await message.reply(message_kp)


@dp.message_handler(commands=['kp_notify'])
async def kp_notify_handler(message: types.Message):
    await message.reply('You will receive notifications when KP index is 5 or higher.')
    asyncio.ensure_future(check_kp_index())


@dp.message_handler(commands=['flare_notify'])
async def solar_activity_notify_handler(message: types.Message):
    await message.reply('You will receive notifications when solar flare of class M or X is detected.')
    asyncio.ensure_future(check_solar_activity())


if __name__ == '__main__':
    executor.start_polling(dp)
