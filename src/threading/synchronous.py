import requests
import time

from prettytable import PrettyTable
from secret import TOKEN


def get_historical_rates(date):
    URL = "https://openexchangerates.org/api/historical/"
    HEADERS = {"Authorization": f"Token {TOKEN}"}
    responce = requests.get(URL + date + ".json", headers=HEADERS)
    responce.raise_for_status()
    result = r = responce.json()["rates"]
    # table = PrettyTable()
    # table.field_names = ["Date", "USD", "GBP", "EUR", "RUB"]
    # table.add_row([date, r["USD"], r["GBP"], r["EUR"], r["RUB"]])
    # print(table)
    return result

def main():
    dates = ["2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]
    table = PrettyTable()
    table.field_names = ["Date", "USD", "GBP", "EUR", "RUB"]
    for date in dates:
        r = get_historical_rates(date)
        table.add_row([date, r["USD"], r["GBP"], r["EUR"], r["RUB"]])
    print(table)

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time() - s
    print("Time:", e)