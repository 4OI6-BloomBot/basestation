# =======================
# Entry to basestation
# =======================

# Imports
from radio import Radio

# Create a radio object and start a loop to listen for data
rx = Radio()

# TODO: Should be in a separate thread and push results to a queue
#       A second thread can then pull from the queue to send data
#       to the server.
rx.listen()
