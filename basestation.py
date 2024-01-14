# =======================
# Entry to basestation
# =======================

# =======================
# Imports
# =======================
import threading
from   src.radio             import Radio
from   src.packet_parser     import PacketParser
from   src.server_middleware import ServerMiddleware

# Import the individual protocols
from protocols import Location


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


# Create a radio object and start a loop to listen for data
radio  = Radio(packet_queue)
parser = PacketParser(packet_queue, data_queue)
server = ServerMiddleware(data_queue)


# TODO: Should be in a separate thread and push results to a queue
#       A second thread can then pull from the queue to send data
#       to the server.
rxThread     = threading.Thread(target=radio.listen)
txThread     = threading.Thread(target=radio.send)
parserThread = threading.Thread(target=parser.monitorRxQueue)
serverThread = threading.Thread(target=server.monitorServerQueue)

rxThread.start()
parserThread.start()
serverThread.start()
# txThread.start()