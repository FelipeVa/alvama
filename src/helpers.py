import json
import os
from pathlib import Path


def json_loader(file_name):
    file = Path(os.path.join(f"./data/{file_name}.json"))

    with open(file) as json_file:
        data = json.loads(json_file.read())
        return data


def get_total_cycles(cycle_time):
    return round((8 * 60) / int(cycle_time))


def get_cycle_cost(cost_per_km, length):
    return float(cost_per_km) * float(length) * 2


def get_total_cost_bus_per_day(cost_per_km, length, cycle_time):
    return get_total_cycles(cycle_time) * get_cycle_cost(cost_per_km, length)


def map_dict(dictionary, f):
    return {k: f(v) for k, v in dictionary.items()}
