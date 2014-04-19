import socket

LOOP_TIME = .025 #seconds is 10 milliseconds
WIDTH = 1200 #meters
HEIGHT = 800 #meters
RADIUS = 10 #meters
IT_CIRCLE_DIVISOR = 5
SPEED = 10 #meters per tick

# Rules Constants
N_PLAYERS = 2
TAG_BACK_DELAY = int(5/LOOP_TIME)

# Network Constants
HOST = '10.32.153.89' # Vitchyr's Gateway
#HOST = "10.32.216.142" #Justin
PORT = 12121

# Socket Constants
S_TIMEOUT = 5.0
S_LEVEL = socket.SOL_TCP
S_OPTNAME = socket.TCP_NODELAY
S_VALUE = 1
S_FAMILY = socket.AF_INET
S_TYPE = socket.SOCK_STREAM
