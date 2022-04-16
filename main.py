import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import inspect
import os

def compare_stocks(stock_symbols, start_date=None, tick_spacing=None):
    func_name = inspect.stack()[0][3]

    # check if input is list
    if type(stock_symbols) != list:
        raise TypeError("[{}]: expected list of strings as input".format(func_name))

    # check if all symbols are valid
    for symbol in stock_symbols:
        symbol = symbol.upper()
        if not os.path.isfile("./data/{}.csv".format(symbol)):
            raise ValueError("[{}]: {} stock symbol not found".format(func_name, symbol))

    # lambda function to convert np string to datetime
    str2date = lambda x: datetime.datetime.strptime(x.decode("utf-8"), "%d-%m-%Y")

    # load data in pandas dataframes
    dataframes = []
    for symbol in stock_symbols:
        symbol = symbol.upper()
        stock = np.genfromtxt(
            fname="./data/{}.csv".format(symbol),
            delimiter=",",
            skip_header=1,
            usecols=(0, 5),
            dtype=None,
            converters={0: str2date}
        )

        df = pd.DataFrame(stock)

        # filter if start_date is specifies
        if start_date != None:
            start_date : datetime.datetime.strptime(start_date, "%d-%m-%Y")
            df = df[df['f0'] > start_date]

        dataframes.append((symbol, df))

    # plot stocks
    fig, ax = plt.subplots()
    ax.grid(True)
    fig.set_dpi(200)
    fig.set_size_inches(20, 10)
    for df in dataframes:
        dates = df[1].iloc[:, 0]
        prices = df[1].iloc[:, 1]

        ax.plot(dates, prices, label = df[0])

    # set tick spacing for Y axis if specified
    if tick_spacing != None and type(tick_spacing) == int:
        plt.gca().yaxis.set_major_locator(plt.MultipleLocator(tick_spacing))

    # draw plot
    plt.xlabel("Date")
    plt.ylabel("Stock Prices (USD)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    compare_stocks(["goog", "amzn"], tick_spacing=100, start_date="01-01-2020")