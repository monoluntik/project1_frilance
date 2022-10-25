import requests
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes, Message
from datetime import datetime
from loguru import logger

# ids = [956247373, 5361912709, 967329896]
ids = [967329896,]

headers = {
    'authority': 'api2.bybit.com',
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    'cookie': '_by_l_g_d=8d58cf55-741c-8ebd-9ce1-c8a4b22f7a40; _gcl_au=1.1.393726344.1661473879; _ym_uid=1661473879315761481; _ym_d=1661473879; _ga=GA1.2.10597552.1661473879; tmr_lvid=f5d05d766da337d86f583a862febc086; tmr_lvidTS=1661473879144; _fbp=fb.1.1661473879753.1940246881; permutive-id=30107233-2948-4d3e-a0c5-6946f2aee277; _clck=1dvy2fw|1|f4o|0; tmr_reqNum=14; _abck=997012C67DE9A34EFBFC79CBA87E58C7~0~YAAQLrIpF2PeSeWDAQAAhycJ9gjHiIjRnaIqkyxTuYHaFyep4nxZFjQOf6zrhlpjavfOAC2As3h67G+cLkSCOYj/LEp+3B0rDB1P57rF90VY3RGXsdSArfGb+eHSwxPzikQFkWyRlRUjZHLvvNxU5dvC/VWcSRr9H+BjyBg2wryuKiNGOV14VZW/li5QolXi6pcRP/nwcxmvtNREpVU8zm71Uf/GLJLRIfH/pjNU/B0WBZOShw+WJQ6QnHMU4fJsoQo/WJ93z/hH/kmL115vbt4KhrD2k/661NuUvkY6d816fTo4CU6lxxzHzl7iv1TiD+i2+SUlzVQDHyOCnjeJUKSSIuomGN4Ko2C2lNA3v976ytHwvsby2zfA5izFTV4Wsy/WOIUfBzoFpbRd5qGq/UFC90Lzi8o=~-1~-1~-1; bm_sz=152A3EE7C9F691C13DD7E0224AFD261B~YAAQLrIpF2beSeWDAQAAhycJ9hHLshqnhumHlZfAw0Dc+tAX7pxAEXoanF80TUX+TlqPzQgQXmvTyUPgqgGnBrhlNDjbxqkG1ZOEVDBr0lJT6T5xl6y5JSQu5fQRPSMjAHoe5P0s3I+XdXGFLo+4M/nsvK7Z/Z75clxPyk0sRLBFgLBnERIYC/X+FU5VmyES1/pOqHCmtwhvJW4NiRejrfjtBb0Fy8FGSzuCuXhpBzJGx8wHXPAMGkFH/mH66y+1rMSjD+I4GZbVnCexOCe9YhDGdQoe8851RFOoDntUOIzqQQ==~3425841~4342834; BYBIT_REG_REF_prod={"lang":"ru-RU","g":"8d58cf55-741c-8ebd-9ce1-c8a4b22f7a40","medium":"direct","url":"https://www.bybit.com/copyTrade/trade-center/detail?leaderMark=%2Bex6jF14FU%2FvN0wwkuYIAQ%3D%3D"}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2220386526%22%2C%22first_id%22%3A%22182d78f62e024a-087f43369239bb8-56510c16-1296000-182d78f62e115f8%22%2C%22props%22%3A%7B%22_a_u_v%22%3A%220.0.5%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyZDc4ZjYyZTAyNGEtMDg3ZjQzMzY5MjM5YmI4LTU2NTEwYzE2LTEyOTYwMDAtMTgyZDc4ZjYyZTExNWY4IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjAzODY1MjYifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2220386526%22%7D%2C%22%24device_id%22%3A%22182d78f62e024a-087f43369239bb8-56510c16-1296000-182d78f62e115f8%22%7D; ak_bmsc=D7393F5DBAF0819DBF182454CD023C8A~000000000000000000000000000000~YAAQLrIpF8LeSeWDAQAANS8J9hHwx+y9t598TI7QihtpaY2wB/IiubxLsrUIex8/IoWIg+qjB+L3pryNs0Yy13R4OCfeIckXmxGmP4yT8i4YL45h6ubCSrbPI1Cz2cpg3NNqjlBphfGetDTDI9nQqwYLvs+XL5cezwpRMa1ejT2tIxwvzZuy0f5bwxT2cnSULrKgoBSZ3/qzE7RBxoKqa4cx+1C5BfqL7oYkQ7Dfu3MLPSmL7uQ/j6MNnwkXwBm09X6g3ICU12RrKMuHvp5x/PtKyAc9WLaCPUNoPBwUpBKw62nu+Vt9oMP2iHvhNIqi+3yZOrD/f+E0VmJ1hrbytHlSqHli7GuU6IrvKQ1Y1a7sXPK6jAmxz38KdyQU6aRG1zP0cFWEpNRPGjK3heJz1CLldcEVuadJmnBpDapiU7aGTfNYXQlX1peOpqu62YDpwH7RaC4FPE/sPZIp1tT5VrglbYvyM3SY8R9gOJPzK6/J7YrIIejUSWvW; b_t_c_k=; bm_sv=848ED00BFBE4EA48AD954D9D2FC6352C~YAAQPbIpF0EOqOSDAQAAPJkS9hEFY04YY3xhdqCZCV70uJC0DR3iMIKgwQcoo85toUsdFXKN/1ls1BgAYgLFnGwWVevAgNK5OSDZqHG2UKPE8FFqUfb2fSnB8s0bb6mDOrsESTupZgtlb+FCn/DjmiFA77KhFNFvgvKGf3Nny9nTt5Wc7OZFnI6TsdLkvo30Fq0WlgzeMcTezytg5/qF2QPiZuMXlRBkMm62w62QBEEULuJGgRcRAexKGAMXEUh0~1',
    'lang': 'en-us',
    'origin': 'https://www.bybit.com',
    'platform': 'pc',
    'referer': 'https://www.bybit.com/',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'traceparent': '00-1e54d3d43ca9b7de08f0381790072132-635df2e6f3f471bb-01',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

API_TOKEN = '5780619352:AAGrfx176OTCR1GgqDi7Grfu7kTpL7BPldw'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

line = 0

async def thread_parse(leader_mark, username, ts):
    params = {
        'timeStamp': ts,
        'leaderMark': str(leader_mark),
    }

    response = requests.get('https://api2.bybit.com/fapi/beehive/public/v1/common/order/list-detail', params=params, headers=headers)
    for column in response.json()['result']['data']:
        try:
            pl = read_light_bd()
            if column['createdAtE3'] not in pl:
                if column['side'] == 'Sell':
                    x = int(column['leverageE2']) / 100
                    x = int(x)
                    symbol_without_usdt = column['symbol'].split('USDT')[0]
                    symbol_default = column['symbol']
                    symbol_with_usdt = symbol_without_usdt + '/' + 'USDT'
                    marge = int(column['orderCostE8']) / 100000000
                    marge = int(marge)
                    for id_ in ids:
                        await bot.send_message(id_, '*' + str(username).strip() + '*' + '\n\n' + 'open ✅' + '\n\n' + f'Short X{x} [{symbol_with_usdt}](https://www.bybit.com/trade/usdt/{symbol_default})' + '\n' + f'Margin {marge} USDT', parse_mode="Markdown", disable_web_page_preview=True)
                elif column['side'] == 'Buy':
                    x = int(column['leverageE2']) / 100
                    x = int(x)
                    symbol_without_usdt = column['symbol'].split('USDT')[0]
                    symbol_default = column['symbol']
                    symbol_with_usdt = symbol_without_usdt + '/' + 'USDT'
                    marge = int(column['orderCostE8']) / 100000000
                    marge = int(marge)
                    for id_ in ids:
                        await bot.send_message(id_, '*' + str(username).strip() + '*' + '\n\n' + 'open ✅' + '\n\n' + f'Long X{x} [{symbol_with_usdt}](https://www.bybit.com/trade/usdt/{symbol_default})' + '\n' + f'Margin {marge} USDT', parse_mode="Markdown", disable_web_page_preview=True)

                await write_light_bd(column['createdAtE3'])
            else:
                logger.info("Ищу новую сделку...")
        except Exception as E:
            logger.info(E)
            pass
async def read_light_bd():
    with open('light_bd.txt', 'r') as read:
        return read.read()

async def write_light_bd(ate3):
    with open('light_bd.txt', 'a') as write:
        write.write(str(ate3) + '\n')

async def read_usernames():
    global line
    try:
        with open('bybit_usernames.txt', 'r') as read:
            read_lines = read.readlines()[line]
    except:
        line = 0
        with open('bybit_usernames.txt', 'r') as read:
            read_lines = read.readlines()[line]

    leader_mark = read_lines.split('|')[0]
    username = read_lines.split('|')[1]

    line += 1

    return leader_mark, username
        

async def main_parse():
    while True:
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        ts = str(ts).replace('.', '')
        leader_mark, username = await read_usernames()
        await thread_parse(leader_mark, username, ts)

        params = {
            'timeStamp': ts,
            'page': '1',
            'pageSize': '8',
            'leaderMark': str(leader_mark),
        }

        response = requests.get('https://api2.bybit.com/fapi/beehive/public/v1/common/leader-history', params=params, headers=headers)
        for column in response.json()['result']['data']:
            try:
                pl = read_light_bd()
                if column['startedTimeE3'] not in pl:
                    if column['side'] == 'Sell':
                        x = int(column['leverageE2']) / 100
                        x = int(x)
                        symbol_without_usdt = column['symbol'].split('USDT')[0]
                        symbol_default = column['symbol']
                        symbol_with_usdt = symbol_without_usdt + '/' + 'USDT'
                        marge = int(column['orderCostE8']) / 100000000
                        marge = int(marge)
                        for id_ in ids:
                            await bot.send_message(id_, '*' + str(username).strip() + '*' + '\n\n' + 'close ❌' + '\n\n' + f'Short X{x} [{symbol_with_usdt}](https://www.bybit.com/trade/usdt/{symbol_default})' + '\n' + f'Margin {marge} USDT', parse_mode="Markdown", disable_web_page_preview=True)
                    elif column['side'] == 'Buy':
                        x = int(column['leverageE2']) / 100
                        x = int(x)
                        symbol_without_usdt = column['symbol'].split('USDT')[0]
                        symbol_default = column['symbol']
                        symbol_with_usdt = symbol_without_usdt + '/' + 'USDT'
                        marge = int(column['orderCostE8']) / 100000000
                        marge = int(marge)
                        for id_ in ids:
                            await bot.send_message(id_, '*' + str(username).strip() + '*' + '\n\n' + 'close ❌' + '\n\n' + f'Long X{x} [{symbol_with_usdt}](https://www.bybit.com/trade/usdt/{symbol_default})' + '\n' + f'Margin {marge} USDT', parse_mode="Markdown", disable_web_page_preview=True)
                
                    await write_light_bd(column['startedTimeE3'])
                else:
                    logger.info("Ищу новую сделку...")
            except Exception as E:
                logger.info(E)
                pass

asyncio.run(main_parse())
