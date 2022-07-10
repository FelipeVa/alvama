from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, value, lpSum, LpInteger, makeDict
import json


def json_loader(file_name):
    file = f"data/{file_name}.json"

    with open(file) as json_file:
        data = json.loads(json_file.read())
        return data


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

    print(len(total_routes), len(total_buses), len(total_capacities))
    X = LpVariable.dicts('Total_bus', (total_routes, total_buses, total_capacities), 0, None, LpInteger)

    problem = LpProblem("Minimize_the_number_of_buses", LpMinimize)

    """ Funcion objetivo del modelo
    Esta funcion es la que se va a minimizar con el objetivo de obtener un numero de buses optimo
    Ademas de que se va a minimizar el costo total
    
    Min Z = sum((for each route i) (for each bus j) (for each capacity k) c[i][j][k] * Y[i][j][k] * X[i][j][k])
    
    
    """

    # Funcion objetivo X[i][j][k] Y[i][j][k] * c[i][j][k]
    problem += lpSum([X[i][j][k] * round(20 * 60 / routes[i]['cycle_time']) * (buses[j]['costs']['per_km'] * routes[i]['length'] * 2) for i in range(len(routes)) for j in range(len(buses)) for k in range(len(buses[j]['capacities']))]), 'Numero de buses '

    # sum{ i } Xijk <= Njk; for j, for k

    for j in range(len(buses)):
        for k in range(len(buses[j]['capacities'])):
            problem += lpSum([X[i][j][k] for i in range(len(routes))]) <= buses[j]['capacities'][k]['available']

    # sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
    for i in range(len(routes)):
        problem += lpSum([buses[j]['capacities'][k]['capacity'] * round(20 * 60 / routes[i]['cycle_time']) * X[i][j][k] for j in range(len(buses)) for k in range(len(buses[j]['capacities']))]) >= routes[i]['demand']

    # The problem data is written to an .lp file
    problem.writeLP("alvama.lp")

    # The problem is solved using PuLP's choice of Solver
    problem.solve()

    # The status of the solution is printed to the screen
    sumT = 0

    for v in problem.variables():
        print(v.name, "=", v.varValue)
        sumT += v.varValue

    print("Total: ", sumT)

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
