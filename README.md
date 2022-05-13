# data-viz-project

Data visualization project for stock market data.

### About

The [data](./data/) directory contains the dataset downloaded from [Kaggle](https://www.kaggle.com/datasets/paultimothymooney/stock-market-data). We are only using S&P 500 data, in CSV format.

The [requirements](./requirements.txt) contains the Python packages that need to be installed before running the actual script. It is recommended to use a virtual environment:
```
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Then, the [main Python script](./main.py) can be run:
```
$ python3 main.py
```

An interactive [Jupyter Notebook](./DataVisualization.ipynb) is also included.

An [R Markdown](./VisualisingAAPLStockPrices.Rmd) is also available, along with [its HTML output](./VisualisingAAPLStockPrices.html).
