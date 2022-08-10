from src.classes.simple_exponential_smoothing import SimpleExponentialSmoothing


def main():
    moving_average = SimpleExponentialSmoothing([21.443,
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
                                                 135.037], smoothing_level=None, optimized=True).solve()

    print(moving_average.to_dict())


if __name__ == '__main__':
    main()
