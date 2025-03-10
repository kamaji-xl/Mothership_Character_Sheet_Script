import zmq
from constants import *


def socket_stuff(port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")

    return socket


def get_char_stats(name, roll_type):
    request_json = {
        "command": "get_stats",
        "name": name,
        "type": roll_type
    }
    print("\nSending request to the Pyhedral server:")
    for key, value in request_json.items():
        print(f"\t{key}: {value}")
    response = send_and_recv(request_json)
    print(f"\nReceived response from the Pyhedral server:")
    for key, value in response.items():
        if key == "stats":
            print(f"\t{key}: {len(value)}")
        else:
            print(f"\t{key}: {value}")
    return response["stats"]


def make_roll(count, sides, name, roll_type, target=0):
    request_json = {
        "command": "roll",
        "count": count,
        "sides": sides,
        "name": name,
        "type": roll_type,
        "target": target
    }

    response = send_and_recv(request_json)
    return response["results"]


def send_and_recv(req):
    socket = socket_stuff(PYHEDRAL_PORT)
    socket.send_json(req)
    response = socket.recv_json()

    return response


if __name__ == "__main__":
    master_socket = socket_stuff(PYHEDRAL_PORT)
