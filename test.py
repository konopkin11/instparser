import asyncio
import random

import requests

list = []


async def get_json():
    # 3 асинхронных функции запускаются сразу
    task1 = asyncio.create_task(get_smth(5))
    task2 = asyncio.create_task(get_smth(2))
    task3 = asyncio.create_task(get_smth(3))
    # значения приходят по выполнению соответствующего таска
    # после того, что выше, потому что await task означает подожди
    # до выполнения таска или async'а выше и затем уже чото делай
    val1 = await task1
    list.append(val1)
    print(list)
    val2 = await task2
    list.append(val2)
    print(list)
    val3 = await task3
    list.append(val3)
    print(list)


async def get_smth(number):
    print(f'thread number {number} started')
    url = 'https://ru.wikipedia.org/wiki/Путин,_Владимир_Владимирович'
    r = requests.get(url=url)

    # типа тут ебать чото жоское высчитывается
    await asyncio.sleep(number)

    return {f'sleep_time({number})': r.status_code}


if __name__ == '__main__':
    asyncio.run(get_json())