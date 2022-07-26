import json
import sys
import time
from src.classes.alvama import Alvama
from src.helpers import json_loader


def main():
    start_time = time.time()
    json_arg = sys.argv[1] if len(sys.argv) > 1 else False
    data = json.loads(json_arg) if json_arg else json_loader("data_2")
    alvama = Alvama(data).make().solve()

    # Alvama at this point is resolved.
    # We can now get the solution and print it.
    # Also, he print the solution in a specific format.
    # For the alvama server.
    buses_group = []

    for variable in alvama.get_variables():
        if variable.varValue != 0:
            value = variable.varValue
            bus_group_split = variable.name.split('_')
            route = alvama.routes[int(bus_group_split[1])]
            bus = alvama.buses[int(bus_group_split[2])]
            capacity = bus['capacities'][int(bus_group_split[3])]

            # This format is for the alvama server.
            # So we just return resources id's
            if json_arg:
                buses_group.append({
                    'route_id': route['id'],
                    'bus_id': bus['id'],
                    'capacity_id': capacity['id'],
                    'amount': int(value),
                })
            # This format is for the local solution.
            else:
                buses_group.append({
                    'route': route['name'],
                    'bus': bus['name'],
                    'capacity': capacity['name'],
                    'amount': int(value)
                })

    response = {
        'status': alvama.get_status(),
        'objective': round(alvama.get_objective(), 2),
        'time': round(time.time() - start_time, 2),
        'results': buses_group
    }

    return print(json.dumps(response))


if __name__ == '__main__':
    main()

# sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
# sum{ i } Xijk <= Njk; for j, for k
