# =======================
# Entry to basestation
# =======================

# =======================
# Imports
# =======================
import threading, os
from   dotenv import load_dotenv

# ==================================================
# Load the environment variables from the .env file
# Needs to be done prior to loading other source
# files due to their potential dependance on vars
# ==================================================
load_dotenv()

# Load other source files
from src.radio             import Radio
from src.packet_parser     import PacketParser
from src.server_middleware import ServerMiddleware

# Import the individual protocols
from protocols.location    import Location
from protocols.temperature import Temperature
from protocols.config      import Config


# ========================================================
# Global vars:
# ========================================================
#   radio_rx_queue:   Used to queue the received packets
#                     from the radio module.
#   server_tx_queue:  Used to queue the parsed data
#                     from the radio packets
# ========================================================
radio_rx_queue  = []
radio_tx_queue  = []
server_rx_queue = [] 
server_tx_queue = []

# Create the classes and pass them their respective queues
if ("NO_RADIO" not in os.environ):
  radio  = Radio(radio_rx_queue, radio_tx_queue)

parser = PacketParser(radio_rx_queue, radio_tx_queue, server_rx_queue, server_tx_queue)
server = ServerMiddleware(server_tx_queue, server_rx_queue)


# ==============================
# Create and start threads
# ==============================
if ("NO_RADIO" not in os.environ):
  rxThread = threading.Thread(target = radio.listen)
  txThread = threading.Thread(target = radio.monitorTxQueue)

serverTxThread = threading.Thread(target = server.monitorTxQueue)
serverRxThread = threading.Thread(target = server.pollConfig)


if ("NO_RADIO" not in os.environ):
  rxThread.start()
  txThread.start()
  
parser.startQueueMonitoring()
serverTxThread.start()
serverRxThread.start()


# TODO: Add way to gracefully stop