from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, value, lpSum
import json


def json_loader(file_name):
    file = f"data/{file_name}.json"

    with open(file) as json_file:
        data = json.loads(json_file.read())
        return data


def main():
    # alkheder model here
    total_count_of_paths = 3
    total_buses_brands_by_manufacturer = 2
    total_buses_brands_count_by_capacity = 2

    # load data from json file
    data = json_loader("data")

    # Routes information
    routes = data['routes']

    # Buses information
    buses = data['buses']

    cycles_per_day = [(i, j, k) for i in range(len(routes)) for j in range(len(buses)) for k in
                      range(len(buses[j]['capacities']))]
    total_routes = [i for i in range(len(routes))]
    total_buses = [i for i in range(len(buses))]
    total_capacities = [i for j in range(len(buses)) for i in range(len(buses[j]['capacities']))]

    Y = LpVariable.dicts('Cycles_per_day', (total_routes, total_buses, total_capacities), 0, None, LpInteger)
    c = LpVariable.dicts('Cycle_cost', (total_routes, total_buses, total_capacities), 0, None, LpInteger)

    print(Y[0][0][0])
    brands = list(map(lambda x: x['brand'], buses))
    capacity_per_bus = list(map(lambda x: x['capacities'], buses))

    # bus_capacity = makeDict([brands], capacity_per_bus, 0)

    # print(bus_capacity)

    problem = LpProblem("Minimize_the_number_of_buses", LpMinimize)
    problem += lpSum(
        [[Y[i][j][k] * (20 / routes[i]['cycle_time']) for i in range(len(routes))] for j in range(len(buses)) for k in
         range(len(buses[j]['capacities']))]) + lpSum(
        [[c[i][j][k] * buses[j]['costs']['per_km'] * routes[i]['length'] for i in range(len(routes))] for j in
         range(len(buses)) for k in
         range(len(buses[j]['capacities']))])

    # problem += Y[1][1][1] * 20
    #
    # for i in range(len(routes)):
    #     problem += lpSum(routes[i]['cycle_time']) <= 20


    # The problem data is written to an .lp file
    problem.writeLP("alvama.lp")

    # The problem is solved using PuLP's choice of Solver
    problem.solve()

    # The status of the solution is printed to the screen
    for v in problem.variables():
        print(v.name, "=", v.varValue)

    # Se imprime el status del problema
    print("Status:", LpStatus[problem.status])

    # Se imprime la funciónobjetivo
    print("funcion_objetivo", value(problem.objective))


if __name__ == '__main__':
    main()

# Volvo ( j = 1 ); Mercedes ( j = 2 ); Daewoo ( j = 3 );
# Volvo ( k = 1 ); Mercedes ( k = 1 , k = 2 ); Daewoo ( k = 1, k = 2 );
