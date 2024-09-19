from threading import Thread
import time

from prettytable import PrettyTable
from secret import TOKEN
from synchronous import get_historical_rates


def main():
    threads = []
    dates = ["2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]
    table = PrettyTable()
    table.field_names = ["Date", "USD", "GBP", "EUR", "RUB"]
    for date in dates:
        thread = Thread(target=get_historical_rates, args=[date])
        thread.start()
        threads.append(thread)

    while threads:
        threads.pop().join()
        # table.add_row([date, r["USD"], r["GBP"], r["EUR"], r["RUB"]])

    print(table)

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time() - s
    print("Time:", e)