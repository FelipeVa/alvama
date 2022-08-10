import pandas as pd
from sklearn.metrics import mean_squared_error
from src.interfaces.forecast_interface import ForecastInterface


class MovingAverage(ForecastInterface):
    mean_squared_error = 0
    next_period_forecast = 0
    values = []

    def __init__(self, data, window_size=3, forecast_period=1):
        self.data = data
        self.window_size = window_size
        self.forecast_period = forecast_period

    def solve(self):
        last_mean_squared_error = None
        range_value = 13 if len(self.data) > 12 else 1

        for i in range(1, range_value, 1):
            data = self.data.copy()

            # Create a new entry to calculate the forecast for n + 1 period
            for j in range(self.forecast_period):
                data.append(0)

            # Convert array of integers to pandas series
            numbers_series = pd.Series(data)

            # Get the window of series
            # of observations of specified window size
            moving_averages = numbers_series.rolling(i).mean().shift(1)
            values = moving_averages.dropna().tolist()

            # Calculate the mean squared error
            if last_mean_squared_error is None:
                self.values = moving_averages.dropna().tolist()
                self.mean_squared_error = mean_squared_error(data[i:-1], self.values[:-1])
                self.next_period_forecast = self.values[-1]
                last_mean_squared_error = self.mean_squared_error
            elif mean_squared_error(data[i:-1], values[:-1]) < last_mean_squared_error:
                self.values = moving_averages.dropna().tolist()
                self.mean_squared_error = mean_squared_error(data[i:-1], self.values[:-1])
                self.next_period_forecast = self.values[-1]
                last_mean_squared_error = self.mean_squared_error

        return self

    def get_mean_squared_error(self):
        return self.mean_squared_error

    def get_next_period_forecast(self):
        return self.next_period_forecast

    def get_values(self):
        return self.values

    def get_data(self):
        return self.data

    def to_dict(self):
        return {
            'method': 'Moving Average',
            'mean_squared_error': round(self.get_mean_squared_error(), 4),
            'next_period_forecast': round(self.get_next_period_forecast()),
            'values': self.get_values()
        }
