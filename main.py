from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, value, lpSum, LpInteger, makeDict, LpContinuous
from pandas import DataFrame
import json


def json_loader(file_name):
    file = f"data/{file_name}.json"

    with open(file) as json_file:
        data = json.loads(json_file.read())
        return data


def get_total_cycles(cycle_time):
    return round(20 * 60 / cycle_time)


def get_cycle_cost(cost_per_km, length):
    return cost_per_km * length * 2


def get_total_cost_bus_per_day(cost_per_km, length, cycle_cost):
    return get_total_cycles(cycle_cost) * get_cycle_cost(cost_per_km, length)


def main():
    # load data from json file
    data = json_loader("data")

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
        [X[i][j][k] * get_total_cost_bus_per_day(buses[j]['costs']['per_km'], routes[i]['length'], routes[i]['cycle_time'])
         for i in range(len(routes)) for j in range(len(buses)) for k in
         range(len(buses[j]['capacities']))]), 'Numero de buses '

    # sum{ i } Xijk <= Njk; for j, for k

    for j in range(len(buses)):
        for k in range(len(buses[j]['capacities'])):
            problem += lpSum([X[i][j][k] for i in range(len(routes))]) <= buses[j]['capacities'][k]['available']

    # sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
    for i in range(len(routes)):
        problem += lpSum(
            [buses[j]['capacities'][k]['capacity'] * get_total_cycles(routes[i]['cycle_time']) * X[i][j][k] for j in
             range(len(buses)) for k in range(len(buses[j]['capacities']))]) >= routes[i]['demand']

    # The problem data is written to an .lp file
    problem.writeLP("alvama.lp")

    # The problem is solved using PuLP's choice of Solver
    problem.solve()

    # The status of the solution is printed to the screen
    buses_count = 0
    buses_group = []

    for v in problem.variables():
        bus_group_split = v.name.split('_')

        if v.varValue != 0:
            buses_group.append({
                'route': int(bus_group_split[2]) + 1,
                'type': int(bus_group_split[3]) + 1,
                'capacity': int(bus_group_split[4]) + 1,
                'amount': v.varValue
            })

        buses_count += v.varValue

    buses_data_frame = DataFrame(data=buses_group).set_index('route')
    # buses_data_frame['sum'] = buses_data_frame[['A', 'B', 'C']].sum(axis=1)
    print("Total buses to be used: ", buses_count)
    print("Buses group: \n", buses_data_frame.sort_values(by='route'))
    # Se imprime el status del problema
    print("Status:", LpStatus[problem.status])

    # Se imprime la funciónobjetivo
    print("funcion_objetivo", value(problem.objective))


if __name__ == '__main__':
    main()

# Volvo ( j = 1 ); Mercedes ( j = 2 ); Daewoo ( j = 3 );
# Volvo ( k = 1 ); Mercedes ( k = 1 , k = 2 ); Daewoo ( k = 1, k = 2 );
# sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
# sum{ i } Xijk <= Njk; for j, for k
#
