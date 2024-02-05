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
from src.radio             import Radio
from src.packet_parser     import PacketParser
from src.server_middleware import ServerMiddleware

# Import the individual protocols
from protocols.location    import Location
from protocols.temperature import Temperature


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
radio  = Radio(radio_rx_queue, radio_tx_queue)
parser = PacketParser(radio_rx_queue, radio_tx_queue, server_rx_queue, server_tx_queue)
server = ServerMiddleware(server_tx_queue)


# ==============================
# Create and start threads
# ==============================
rxThread     = threading.Thread(target=radio.listen)
txThread     = threading.Thread(target=radio.monitorTxQueue)
serverThread = threading.Thread(target=server.monitorServerQueue)

parser.startQueueMonitoring()
rxThread.start()
serverThread.start()
txThread.start()

# TODO: Add way to gracefully stop