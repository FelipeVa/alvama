import json
import typer
from src.classes.alvama import Alvama
from src.classes.holt import Holt
from src.classes.moving_average import MovingAverage
from src.classes.simple_exponential_smoothing import SimpleExponentialSmoothing
import time


def main(tool: str, payload: str):
    time_start = time.time()

    if tool == 'alvama':
        alvama = Alvama(json.loads(payload)).make().solve()
        response = alvama.to_json()

    elif tool == 'forecast':
        data = list(map(lambda x: x['value'], json.loads(payload)['items']))
        moving_average = MovingAverage(data).solve()
        simple_exponential_smoothing = SimpleExponentialSmoothing(data).solve()
        holt = Holt(data).solve()

        forecasts = {
            'holt': holt.to_dict(),
            'moving_average': moving_average.to_dict(),
            'simple_exponential_smoothing': simple_exponential_smoothing.to_dict()
        }

        mean_squared_errors_values = list(map(lambda x: x['mean_squared_error'], forecasts.values()))
        mean_squared_errors_keys = list(forecasts.keys())

        min_mean_squared = mean_squared_errors_keys[mean_squared_errors_values.index(min(mean_squared_errors_values))]

        response = forecasts[min_mean_squared]

    else:
        raise f"Unknown tool: {tool}"

    response.update({
        'time': round(time.time() - time_start, 4),
    })

    return print(json.dumps(response))


if __name__ == '__main__':
    typer.run(main)
