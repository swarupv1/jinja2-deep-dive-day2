import json


def pp(data):
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    with open("nb_device.json") as fin:
        nb_device = json.load(fin)

    print("Loaded JSON data into 'nb_device' variable.\n")
    print("You can use 'pp(nb_device)' to display all of the data.")
