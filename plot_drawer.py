import matplotlib.pyplot as plt
import numpy as np


def create_plot(rates_currency_1, code_currency_1, rates_currency_2, code_currency_2):
    x_val_usd = [rate[0] for rate in rates_currency_1]
    y_val_usd = [rate[1] for rate in rates_currency_1]
    x_val_eur = [rate[0] for rate in rates_currency_2]
    y_val_eur = [rate[1] for rate in rates_currency_2]

    plt.plot(x_val_usd, y_val_usd)
    plt.plot(x_val_eur, y_val_eur)
    plt.xticks(rotation=50)
    plt.xticks(ticks=np.arange(0, len(x_val_usd), step=len(x_val_usd) / 9))

    plt.xlabel("Date")
    plt.ylabel("Exchange rate")

    plt.legend([code_currency_1, code_currency_2])

    plt.show()
