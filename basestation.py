# =======================
# Entry to basestation
# =======================

# Imports
import threading
from   radio         import Radio
from   packet_parser import PacketParser

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


# TODO: Should be in a separate thread and push results to a queue
#       A second thread can then pull from the queue to send data
#       to the server.
rxThread     = threading.Thread(target=radio.listen)
parserThread = threading.Thread(target=parser.monitorRxQueue)
txThread     = threading.Thread(target=radio.send)

rxThread.start()
parserThread.start()
txThread.start()

