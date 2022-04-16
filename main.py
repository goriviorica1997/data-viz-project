import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

str2date = lambda x: datetime.datetime.strptime(x.decode("utf-8"), '%d-%m-%Y')
stock = np.genfromtxt(
    fname="./data/AAPL.csv",
    delimiter=",",
    skip_header=1,
    usecols=(0, 5),
    dtype=None,
    converters= {0: str2date}
)

df = pd.DataFrame(stock)
dates = df.iloc[:, 0]
closing_prices = df.iloc[:, 1]

fig, ax = plt.subplots()
ax.plot(dates, closing_prices)
ax.set(xlabel='Year', ylabel='Closing Price (USD)',
       title='AAPL Chart')
ax.grid()
plt.show()

print(dates)