from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

import time 

import requests
from prettytable import PrettyTable
from secret import TOKEN

POOL_SIZE = 4
DATES = ["2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]

table = PrettyTable()
table.field_names = ["Date", "USD", "GBP", "EUR", "RUB"]


def get_historical_rates(date):
    URL = "https://openexchangerates.org/api/historical/"
    HEADERS = {"Authorization": f"Token {TOKEN}"}
    responce = requests.get(URL + date + ".json", headers=HEADERS)
    responce.raise_for_status()
    result = responce.json()["rates"]
    return date, result


def present_result(date, result):
    table.add_row([date, result["USD"], result["GBP"], result["EUR"], result["RUB"]])



def main(use_threads=False):
    if use_threads:
        pool_cls = ThreadPool
    else:
        pool_cls = ProcessPool

    with pool_cls(POOL_SIZE) as pool:
        results = pool.map(get_historical_rates, DATES)

    for result in results:
        present_result(*result)

    print(table)


if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time() - s

    print()
    print(f"Time: {e:.2f}")
