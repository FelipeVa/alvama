class ForecastInterface:
    def solve(self) -> 'ForecastInterface':
        raise NotImplementedError

    def get_mean_squared_error(self) -> float:
        raise NotImplementedError

    def get_next_period_forecast(self) -> float:
        raise NotImplementedError

    def get_values(self) -> list:
        raise NotImplementedError

    def get_data(self) -> list:
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError
