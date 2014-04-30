import socket

LOOP_TIME = .01 #seconds is 10 milliseconds
WIDTH = 800 #meters
HEIGHT = 600 #meters
RADIUS = 5 #meters
IT_CIRCLE_DIVISOR = 5
SPEED = 5 #meters per tick

# Rules Constants
N_PLAYERS = 2
TAG_BACK_DELAY = int(5/LOOP_TIME)

# Network Constants
HOST = '10.33.119.92' # Vitchyr's Gateway
#HOST = "10.32.216.142" #Justin
PORT = 12120

# Socket Constants
S_TIMEOUT = 5.0
S_LEVEL = socket.SOL_SOCKET
S_OPTNAME = socket.SO_REUSEADDR
S_VALUE = 1
S_FAMILY = socket.AF_INET
S_TYPE = socket.SOCK_STREAM
