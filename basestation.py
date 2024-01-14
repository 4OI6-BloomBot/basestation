# =======================
# Entry to basestation
# =======================

# =======================
# Imports
# =======================
import threading
from   dotenv import load_dotenv

# ==================================================
# Load the environment variables from the .env file
# Needs to be done prior to loading other source
# files due to their potential dependance on vars
# ==================================================
load_dotenv()

# Load other source files
from   src.radio             import Radio
from   src.packet_parser     import PacketParser
from   src.server_middleware import ServerMiddleware

# Import the individual protocols
from protocols.location    import Location
from protocols.temperature import Temperature


# ==================================================
# Global vars:
# ==================================================
#   packet_queue: Used to queue the received packets
#                 from the radio module.
#   data_queue:   Used to queue the parsed data
#                 from the radio packets
# ==================================================
packet_queue = [] 
data_queue   = []

# Create the classes and pass them their respective queues
radio  = Radio(packet_queue)
parser = PacketParser(packet_queue, data_queue)
server = ServerMiddleware(data_queue)


# ==============================
# Create and start threads
# ==============================
rxThread     = threading.Thread(target=radio.listen)
txThread     = threading.Thread(target=radio.send)
parserThread = threading.Thread(target=parser.monitorRxQueue)
serverThread = threading.Thread(target=server.monitorServerQueue)

rxThread.start()
parserThread.start()
serverThread.start()
txThread.start()

# TODO: Add way to gracefully stop