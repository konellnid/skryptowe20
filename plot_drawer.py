import matplotlib.pyplot as plt
import numpy as np


def create_plot_from_database(database_data, code_currency_original, code_currency_from_exchange):
    # database_data: (date, exchange_rate, sum)
    x_val = [row[0] for row in database_data]
    y_val_original = [row[2] for row in database_data]
    y_val_exchanged = [row[2] * row[1] for row in database_data]

    plt.figure(figsize=(20, 10))
    plt.plot(x_val, y_val_original)
    plt.plot(x_val, y_val_exchanged)
    plt.xticks(rotation=50)
    plt.xticks(ticks=np.arange(0, len(x_val), step=len(x_val) / 9))

    plt.title("Total price each day")
    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend([code_currency_original, code_currency_from_exchange])

    plt.savefig("prices.svg")
    plt.show()


def create_plot_from_exchange_rates(rates_currency_1, code_currency_1, rates_currency_2, code_currency_2):
    x_val = [rate[0] for rate in rates_currency_1]
    y_val_usd = [rate[1] for rate in rates_currency_1]
    y_val_eur = [rate[1] for rate in rates_currency_2]

    plt.plot(x_val, y_val_usd)
    plt.plot(x_val, y_val_eur)
    plt.xticks(rotation=50)
    plt.xticks(ticks=np.arange(0, len(x_val), step=len(x_val) / 9))

    plt.title("Exchange rate for each available day")
    plt.xlabel("Date")
    plt.ylabel("Exchange rate")

    plt.legend([code_currency_1, code_currency_2])

    plt.savefig("exchange_rates.svg")
    plt.show()