import pandas as pd
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import SimpleExpSmoothing
from src.interfaces.forecast_interface import ForecastInterface


class SimpleExponentialSmoothing(ForecastInterface):
    mean_squared_error = 0
    next_period_forecast = 0
    values = []

    def __init__(self, data, forecast_period=1, smoothing_level=None, optimized=True):
        self.data = data
        self.smoothing_level = smoothing_level
        self.forecast_period = forecast_period
        self.optimized = optimized

    def solve(self):
        data = self.data
        simple_exponential_smoothing = SimpleExpSmoothing(data).fit(smoothing_level=self.smoothing_level,
                                                                    optimized=self.optimized)
        self.values = pd.concat([pd.Series(simple_exponential_smoothing.fittedvalues), pd.Series(simple_exponential_smoothing.forecast(self.forecast_period))]).tolist()

        # Set needed values
        self.mean_squared_error = mean_squared_error(data, self.values[:-1])
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

    def to_dict(self):
        return {
            'method': 'Simple Exponential Smoothing',
            'mean_squared_error': round(self.get_mean_squared_error(), 4),
            'next_period_forecast': round(self.get_next_period_forecast()),
            'values': self.get_values()
        }
