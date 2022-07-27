from src.classes.holt import Holt


def main():
    moving_average = Holt([21.443,
                           45.687,
                           55.533,
                           60.816,
                           67.327,
                           77.398,
                           85.132,
                           93.311,
                           105.959,
                           122.497,
                           136.467,
                           149.066,
                           156.464,
                           183.799,
                           199.656,
                           220.355,
                           265.719,
                           135.037], smoothing_level=None, smoothing_trend=None, optimized=True).solve()

    print('MSE', moving_average.get_mean_squared_error())
    print('Forecast', moving_average.get_next_period_forecast())
    print('Values', moving_average.get_values())


if __name__ == '__main__':
    main()
