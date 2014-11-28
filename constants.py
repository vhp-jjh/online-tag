import socket
DEBUG = False

# Game Rules
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
# HOST = '98.159.211.222' # Vitchyr's Gateway
# HOST = "192.168.2.12" #Justin
# SERVER_ADDR = '192.168.15.14'
SERVER_ADDR = 'localhost'
SERVER_PORT = 12120

# Socket Constants
S_START_TIMEOUT = 10.0
S_TIMEOUT = 0.01
S_LEVEL = socket.SOL_SOCKET
S_OPTNAME = socket.SO_REUSEADDR
S_VALUE = 1
S_FAMILY = socket.AF_INET
S_TYPE = socket.SOCK_DGRAM
