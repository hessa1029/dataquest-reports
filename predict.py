import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

stocks = pd.read_csv('sphist.csv')

stocks['Date'] = pd.to_datetime(stocks['Date'], infer_datetime_format=True)
stocks.sort_values(by='Date', ascending=True, inplace=True)

mean_5day = stocks['Close'].rolling(window=5).mean().shift(1)
mean_1year = stocks['Close'].rolling(window=365).mean().shift(1)
std_5day = stocks['Close'].rolling(window=5).std().shift(1)
vol_5day = stocks['Volume'].rolling(window=5).mean().shift(1)
vol_1year = stocks['Volume'].rolling(window=5).mean().shift(1)

stocks['rolling_mean_5day'] = mean_5day
stocks['rolling_mean_1year'] = mean_1year
stocks['rolling_std_5day'] = std_5day
stocks['rolling_vol_5day'] = vol_5day
stocks['rolling_vol_1year'] = vol_1year

stocks = stocks[stocks['Date'] > datetime(year=1951, month=1, day=3)]
stocks.dropna(axis=0, inplace=True)
train = stocks[stocks['Date'] < datetime(year=2013, month=1, day=1)]
test = stocks[stocks['Date'] >= datetime(year=2013, month=1, day=1)]


X_train, y_train = train.drop(columns=['Close', 'High', 'Low', 'Open', 'Volume', 'Adj Close', 'Date']), train['Close']
X_test, y_test = test.drop(columns=['Close', 'High', 'Low', 'Open', 'Volume', 'Adj Close', 'Date']), test['Close']

lr = LinearRegression()
lr.fit(X_train, y_train)
predictions = lr.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(mae)
print(lr.score(X_train, y_train))