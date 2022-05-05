import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import inspect
import os


def load_data(stock_symbols):
    """
    Loads data into pandas dataframes
    :param stock_symbols: [str]
    :return: [[str, dataframe]], where:
        - str is the stock symbol
        - dataframe is a pandas dataframe containing the corresponding stock data
    """

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
            dtype=None,
            usecols=(0, 1, 2, 3, 4, 5),
            names="Date,Low,Open,Volume,High,Close",
            converters={0: str2date}
        )

        df = pd.DataFrame(stock)

        dataframes.append([symbol, df])

    return dataframes


def compare_stocks(stock_symbols, start_date=None, tick_spacing=None):
    """
    Plots chart with closing prices of the stocks.
    :param stock_symbols: [str], list of stock symbols
    :param start_date: str, date from which plotting will be done, with format of ""%d-%m-%Y"
    :param tick_spacing: int, tick spacing for the Y axis
    """
    dataframes = load_data(stock_symbols)

    for df in dataframes:
        # filter if start_date is specifies
        if start_date is not None:
            start_date: datetime.datetime.strptime(start_date, "%d-%m-%Y")
            df[1] = df[1][df[1]["Date"] > start_date]

    # plot stocks
    fig, ax = plt.subplots()
    ax.grid(True)
    fig.set_dpi(200)
    fig.set_size_inches(20, 10)

    for df in dataframes:
        dates = df[1].iloc[:, 0]
        prices = df[1].iloc[:, 1]

        ax.plot(dates, prices, label=df[0])

    # set tick spacing for Y axis, if specified
    if tick_spacing is not None and type(tick_spacing) == int:
        plt.gca().yaxis.set_major_locator(plt.MultipleLocator(tick_spacing))

    # draw plot
    plt.xlabel("Date")
    plt.ylabel("Stock Prices (USD)")
    plt.legend()
    plt.show()


def donut():
    """
    Plots a donut chart with the first 10 companies by market cap.
    """
    files = [f.strip(".csv") for f in os.listdir("./data") if os.path.isfile(os.path.join("./data", f))]

    # get last closing price for each stock
    data = []
    for symbol in files:
        stock = np.genfromtxt(
            fname="./data/{}.csv".format(symbol),
            delimiter=",",
            skip_header=1,
            dtype=None,
            usecols=(5),
            names="Close",
        )

        df = pd.DataFrame(stock).iloc[-1].astype(float).round(1)

        if not pd.isna(df["Close"]):
            if symbol != "BRK-A":
                # outlier
                data.append([symbol, df["Close"].astype(int)])

    # sort by stock prices
    data.sort(key=lambda x: x[1], reverse=True)

    # select only first 10 companies
    data = data[0:10]

    # plot
    plt.figure(dpi=200)
    plt.pie([e[1] for e in data], labels=[e[0] for e in data], autopct='%1.1f%%', startangle=90,
            textprops=dict(fontsize=6))
    plt.axis('equal')
    plt.title("Top 10 Stocks by Market Price", loc="left")
    plt.show()


def candlestick(symbol, start_date, end_date):
    """
    Plots a candlestick chart for the given stock symbol.
    :param symbol: company symbol for which to plot the chart
    :param start_date: start date of the plot
    :param end_date: end date of the plot
    """
    str2date = lambda x: datetime.datetime.strptime(x.decode("utf-8"), "%d-%m-%Y")
    stock = np.genfromtxt(
        fname="./data/{}.csv".format(symbol.upper()),
        delimiter=",",
        skip_header=1,
        dtype=None,
        usecols=(0, 1, 2, 4, 5),
        names="Date,Low,Open,High,Close",
        converters={0: str2date}
    )

    df = pd.DataFrame(stock)

    # restrict to one week of the start_date
    start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
    end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y")

    # extract prices for the given week
    mask_dates = (df['Date'] > start_date) & (df['Date'] <= end_date)
    df = df[mask_dates]

    # create figure
    plt.figure()
    plt.figure().set_dpi(200)
    plt.figure().set_size_inches(20, 10)
    plt.grid(True, axis="y")
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(20))

    # define width of candlestick elements
    width = .4
    width2 = .05

    # define up and down prices
    up = df[df["Close"] >= df["Open"]]
    down = df[df["Close"] < df["Open"]]

    # plot up prices
    plt.bar(up["Date"], up["Close"] - up["Open"], width, bottom=up["Open"], color="green")
    plt.bar(up["Date"], up["High"] - up["Close"], width2, bottom=up["Close"], color="green")
    plt.bar(up["Date"], up["Low"] - up["Open"], width2, bottom=up["Open"], color="green")

    # plot down prices
    plt.bar(down["Date"], down["Close"] - down["Open"], width, bottom=down["Open"], color="red")
    plt.bar(down["Date"], down["High"] - down["Open"], width2, bottom=down["Open"], color="red")
    plt.bar(down["Date"], down["Low"] - down["Close"], width2, bottom=down["Close"], color="red")

    # rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    # display candlestick chart
    plt.show()


if __name__ == "__main__":
    compare_stocks(["goog", "amzn"], tick_spacing=200, start_date="01-01-2020")
    donut()
    candlestick("amzn", "04-06-2020", "01-07-2020")
