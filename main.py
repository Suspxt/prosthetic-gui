import socket
import csv
from controller import Controller

settings = []
with open('config.csv', 'r') as config_csv:
    config_reader = csv.reader(config_csv)
    config_reader.__next__()
    for setting in config_reader:
        settings.append(setting)

"""
Server Stuff
https://www.youtube.com/watch?v=Lbfe3-v7yE0
https://www.youtube.com/watch?v=8A4dqoGL62E
Notes
A socket is an endpoint
"""
TCP_IP = '127.0.0.1'
TCP_PORT = 7777
HEADER_SIZE = 5

print("IP: ", TCP_IP)
print("Port: ", TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPV4, SOCK_STREAM for TCP
s.bind((TCP_IP, TCP_PORT)) # localhost, port
s.listen(1) # Queue of 1

client_s, address = s.accept()
print(f"Established connection to {address}.")
client_s.send(bytes("Connected to prosthetic-gui.", "utf-8"))

# TODO: Make a script reader

# TODO: Controller initialization
controller = Controller(settings)
# controller.view.main() UNCOMMENT LATER

msg = ""


# todo ensure messages from michael are in following format: "#___m#___s"; m for motor, s for sensor
def process(message):
    """
    Sends to the controller as many full data points from MESSAGE as contained in
    MESSAGE, then returns the remaining incomplete chunk of the message.
    """
    while 's' in message:
        controller.process_readings(message[:message.find('s') + 1])
        message = message[message.find('s') + 1:]
    return message


while True:
    header = client_s.recv(HEADER_SIZE)
    if not header:
        print("Connection lost.")
        break
    print(header) # TODO remove later
    buffer = 0 # todo

    chunk = client_s.recv(buffer)
    if not chunk:
        print("Connection lost.")
        break
    msg += chunk.decode(encoding="utf-8")
    msg = process(msg)

client_s.close()
