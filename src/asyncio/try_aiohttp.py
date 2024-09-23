# def get_historical_rates(date):
#     URL = "https://openexchangerates.org/api/historical/"
#     HEADERS = {"Authorization": f"Token {TOKEN}"}
#     responce = requests.get(URL + date + ".json", headers=HEADERS)
#     responce.raise_for_status()
#     result = responce.json()["rates"]
#     return date, result

import asyncio
import time

import aiohttp
from prettytable import PrettyTable
from secret import TOKEN

table = PrettyTable()
table.field_names = ["Date", "USD", "GBP", "EUR", "RUB"]

URL = "https://openexchangerates.org/api/historical/"
HEADERS = {"Authorization": f"Token {TOKEN}"}
DATES = ["2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]


async def get_historical_rates(session: aiohttp.ClientSession, date: str):
    async with session.get(URL + date + ".json", headers=HEADERS) as response:
        result = (await response.json())["rates"]
        # present_result(date, result)
        return date, result


async def fetch_rates(session, place):
    return await get_historical_rates(session, place)

def present_result(date, result):
    # date, result = await result
    table.add_row([date, result["USD"], result["GBP"], result["EUR"], result["RUB"]])
    print("\033c")
    print(table)

async def main():
    async with aiohttp.ClientSession() as session:
        for result in await asyncio.gather(*[
            get_historical_rates(session, date)
            for date in DATES
        ]):
            present_result(*result)
            pass

if __name__ == "__main__":
    s = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    e = time.time() - s
    print(f"Time: {e:.2f}")