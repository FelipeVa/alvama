from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, PULP_CBC_CMD, LpStatus, value
from src.helpers import get_total_cycles, get_total_cost_bus_per_day
import time


class Alvama:
    problem: LpProblem = {}
    time = 0.0

    def __init__(self, data):
        self.data = data
        self.routes = self.data['routes']
        self.buses = self.data['buses']
        self.total_routes = [i for i in range(len(self.routes))]
        self.total_buses = [i for i in range(len(self.buses))]
        self.total_capacities = [i for j in range(len(self.buses)) for i in range(len(self.buses[j]['capacities']))]

    def make(self):
        self.set_problem()

        x = LpVariable.dicts('X', (
            self.total_routes,
            self.total_buses,
            self.total_capacities
        ), 0, None, LpInteger)

        self.set_objective(lpSum(
            [x[i][j][k] * get_total_cost_bus_per_day(
                self.buses[j]['cost_per_km'],
                self.routes[i]['length'],
                self.routes[i]['cycle_time']
            )
             for i in range(len(self.routes)) for j in range(len(self.buses)) for k in
             range(len(self.buses[j]['capacities']))]))

        self.set_constraints(x)

        return self

    def set_objective(self, objective):
        self.problem += objective

    def set_constraints(self, x):
        for j in range(len(self.buses)):
            for k in range(len(self.buses[j]['capacities'])):
                self.problem += lpSum([x[i][j][k] for i in range(len(self.routes))]) <= int(
                    self.buses[j]['capacities'][k]['available'])

        for i in range(len(self.routes)):
            self.problem += lpSum(
                [int(self.buses[j]['capacities'][k]['capacity']) * get_total_cycles(self.routes[i]['cycle_time']) *
                 x[i][j][k] for
                 j in
                 range(len(self.buses)) for k in range(len(self.buses[j]['capacities']))]) >= int(
                self.routes[i]['demand'])

        return self

    def solve(self, message=False):
        self.time = time.time()
        self.problem.solve(PULP_CBC_CMD(msg=message))
        self.time = time.time() - self.time

        return self

    def get_status(self):
        return LpStatus[self.problem.status]

    def get_objective(self):
        return value(self.problem.objective)

    def get_variables(self):
        return self.problem.variables()

    def set_problem(self):
        self.problem = LpProblem("Minimize_the_number_of_buses", LpMinimize)

    def get_problem(self):
        return self.problem

    def to_json(self):
        buses_group = []

        for variable in self.get_variables():
            if variable.varValue != 0:
                variable_value = variable.varValue
                bus_group_split = variable.name.split('_')
                route = self.routes[int(bus_group_split[1])]
                bus = self.buses[int(bus_group_split[2])]
                capacity = bus['capacities'][int(bus_group_split[3])]

                # This format is for the alvama server.
                # So we just return resources id's
                buses_group.append({
                    'route_id': route['id'] if 'id' in route else route['name'],
                    'bus_id': bus['id'] if 'id' in bus else bus['name'],
                    'capacity_id': capacity['id'] if 'id' in capacity else capacity['name'],
                    'amount': int(variable_value),
                })

        return {
            'status': self.get_status(),
            'objective': round(self.get_objective(), 2),
            'time': round(self.time, 4),
            'results': buses_group
        }
