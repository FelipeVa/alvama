import pandas as pd
import numpy as np
from src.interfaces.forecast_interface import ForecastInterface
from sklearn.metrics import mean_squared_error


class MovingAverage(ForecastInterface):
    mean_squared_error = 0
    next_period_forecast = 0
    values = []

    def __init__(self, data, window_size=3):
        self.data = data
        self.window_size = window_size

    def solve(self):
        data = self.data
        window_size = self.window_size

        # Create a new entry to calculate the forecast for n + 1 period
        data.append(0)

        # Convert array of integers to pandas series
        numbers_series = pd.Series(data)

        # Get the window of series
        # of observations of specified window size
        moving_averages = numbers_series.rolling(window_size).mean().shift(1)

        # Convert pandas series back to list
        self.values = moving_averages.dropna().tolist()

        # Remove null entries from the list
        self.mean_squared_error = mean_squared_error(data[window_size:-1], self.values[:-1])
        self.next_period_forecast = self.values[-1]

        return self

    def get_mean_squared_error(self):
        return self.mean_squared_error

    def get_next_period_forecast(self):
        return self.next_period_forecast

    def get_values(self):
        return self.values

    def get_data(self):
        return self.data
