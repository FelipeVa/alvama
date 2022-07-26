import json
import sys
from src.classes.alvama import Alvama
from src.helpers import json_loader


def main():
    json_arg = sys.argv[1] if len(sys.argv) > 1 else False
    data = json.loads(json_arg) if json_arg else json_loader("data_2")
    alvama = Alvama(data).make().solve()

    # Alvama at this point is resolved.
    # We can now get the solution and print it.
    # Also, he print the solution in a specific format.
    # For the alvama server.
    response = alvama.to_json()

    return print(json.dumps(response))


if __name__ == '__main__':
    main()

# sum{ i, j } Kjk*Yijk*Xijk >= di;  for i
# sum{ i } Xijk <= Njk; for j, for k
