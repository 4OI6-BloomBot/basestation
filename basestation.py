# =======================
# Entry to basestation
# =======================

# Imports
import threading
from   radio import Radio

# =============
# Global vars:
#==============
packet_queue = []


# Create a radio object and start a loop to listen for data
rx = Radio(packet_queue)

# TODO: Should be in a separate thread and push results to a queue
#       A second thread can then pull from the queue to send data
#       to the server.
rx.listen()
