import json
import os
import sys
import time
from pathlib import Path

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, PULP_CBC_CMD, value, LpStatus


def json_loader(file_name):
    file = Path(os.path.join(os.path.dirname(__file__), f"data/{file_name}.json"))

    with open(file) as json_file:
        data = json.loads(json_file.read())
        return data


def get_total_cycles(cycle_time):
    return round(20 * 60 / int(cycle_time))


def get_cycle_cost(cost_per_km, length):
    return float(cost_per_km) * float(length) * 2


def get_total_cost_bus_per_day(cost_per_km, length, cycle_cost):
    return get_total_cycles(cycle_cost) * get_cycle_cost(cost_per_km, length)


def main():
    start_time = time.time()
    json_arg = sys.argv[1] if len(sys.argv) > 1 else False
    # load data from json file
    data = json.loads(json_arg) if json_arg else json_loader("data_2")

    # Routes information
    routes = data['routes']

    # Buses information
    buses = data['buses']

    total_routes = [i for i in range(len(routes))]
    total_buses = [i for i in range(len(buses))]
    total_capacities = [i for j in range(len(buses)) for i in range(len(buses[j]['capacities']))]

    X = LpVariable.dicts('Total_bus', (total_routes, total_buses, total_capacities), 0, None, LpInteger)

    problem = LpProblem("Minimize_the_number_of_buses", LpMinimize)

    """ Funcion objetivo del modelo
    Tiene como objetivo minimizar los costes totales, ademas de minimizar el numero de buses que se utilizan
    
    Min Z = sum((for each route i) (for each bus j) (for each capacity k) c[i][j][k] * Y[i][j][k] * X[i][j][k])
    """

    # Funcion objetivo X[i][j][k] Y[i][j][k] * c[i][j][k]
    problem += lpSum(
        [X[i][j][k] * get_total_cost_bus_per_day(buses[j]['cost_per_km'], routes[i]['length'],
                                                 routes[i]['cycle_time'])
         for i in range(len(routes)) for j in range(len(buses)) for k in
         range(len(buses[j]['capacities']))]), 'Numero de buses '

    # sum{ i } Xijk <= Njk; for j, for k

    for j in range(len(buses)):
        for k in range(len(buses[j]['capacities'])):
            problem += lpSum([X[i][j][k] for i in range(len(routes))]) <= int(buses[j]['capacities'][k]['available'])

    # sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
    for i in range(len(routes)):
        problem += lpSum(
            [int(buses[j]['capacities'][k]['capacity']) * get_total_cycles(routes[i]['cycle_time']) * X[i][j][k] for j in
             range(len(buses)) for k in range(len(buses[j]['capacities']))]) >= int(routes[i]['demand'])

    # The problem is solved using PuLP's choice of Solver
    problem.solve(PULP_CBC_CMD(msg=False))

    # The status of the solution is printed to the screen
    buses_count = 0
    buses_group = []

    for v in problem.variables():
        if v.varValue != 0:
            bus_group_split = v.name.split('_')
            route = routes[int(bus_group_split[2])]
            bus = buses[int(bus_group_split[3])]
            capacity = bus['capacities'][int(bus_group_split[4])]

            if json_arg:
                buses_group.append({
                    'route_id': route['id'],
                    'bus_id': bus['id'],
                    'capacity_id': capacity['id'],
                    'amount': v.varValue,
                })
            else:
                buses_group.append({
                    'route': int(bus_group_split[2]) + 1,
                    'type': int(bus_group_split[3]) + 1,
                    'capacity': int(bus_group_split[4]) + 1,
                    'amount': v.varValue
                })

        buses_count += v.varValue

    response = {
        'status': LpStatus[problem.status],
        'objective': round(value(problem.objective), 4),
        'time': round(time.time() - start_time, 4),
        'results': buses_group
    }

    return print(json.dumps(response))


if __name__ == '__main__':
    main()

# Volvo ( j = 1 ); Mercedes ( j = 2 ); Daewoo ( j = 3 );
# Volvo ( k = 1 ); Mercedes ( k = 1 , k = 2 ); Daewoo ( k = 1, k = 2 );
# sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
# sum{ i } Xijk <= Njk; for j, for k
#
