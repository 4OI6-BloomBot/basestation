# ================================================
# Parser class to decode and reformat the packets
# as JSON objects.
# ================================================

# ==============
# Imports
# ==============
import struct, threading
from   protocols.base import PROTOCOLS, NUM_SPECIAL_KEYS
from   wasabi         import msg


class PacketParser:

  # ================================================== 
  # Constructor - Requires access to the radio and 
  #               server shared queues to convert
  #               between formats.
  # ==================================================
  def __init__(self, radio_rx_queue, radio_tx_queue, server_rx_queue, server_tx_queue):
    # From Radio to Server
    self.RADIO_RX_QUEUE  = radio_rx_queue
    self.SERVER_TX_QUEUE = server_tx_queue

    # From Server to Radio
    self.SERVER_RX_QUEUE = server_rx_queue
    self.RADIO_TX_QUEUE  = radio_tx_queue



  # ======================================================
  # startQueueMonitoring - Starts threads for each of the 
  #                        queues.
  # ======================================================
  def startQueueMonitoring(self):
    server_rx = threading.Thread(target = self.monitorServerRxQueue)
    radio_rx  = threading.Thread(target = self.monitorRadioRxQueue)

    server_rx.start()
    radio_rx.start()


  # ==================================================
  # monitorServerRxQueue - Monitor the server Rx queue 
  #                        for new entries and parse
  #                        them.
  # ==================================================
  def monitorServerRxQueue(self):
    while (True):
      if len(self.SERVER_RX_QUEUE) > 0:
        result = self.packPacket(self.SERVER_RX_QUEUE.pop(0))

        # Only process the result if it succeed
        if result is not None:
          self.RADIO_TX_QUEUE.append(result)



  # ==================================================
  # monitorRadioRxQueue - Monitor the radio Rx queue  
  #                       for new entries and parse
  #                       them.
  # ==================================================
  def monitorRadioRxQueue(self):
    while (True):
      if len(self.RADIO_RX_QUEUE) > 0:
        result = self.parsePacket(self.RADIO_RX_QUEUE.pop(0))

        # Only process the result if it succeed
        if result is not None:
          self.SERVER_TX_QUEUE.append(result)



  # ==================================================
  # parsePacket - Parse a given packet and match it to
  #               a protocol.
  # ==================================================
  def parsePacket(self, packet):

    # Find the protocol in the map
    protocol_id = packet[0]
    if (protocol_id not in PROTOCOLS):
      raise ValueError("[ERROR] Could not find protocol with id={id}".format(id = protocol_id))
      

    # Create a new instance of the protocol
    protocol = PROTOCOLS[protocol_id]()

    # Pull the values from the sent data and check if the data is valid.
    values   = struct.unpack(protocol.getBytePackStr(), packet)

    # Check if the number of values matches what is expected for the datatype
    value_cnt, expected_cnt = len(protocol.data.keys()), len(values) - NUM_SPECIAL_KEYS
    if (value_cnt != expected_cnt):
      raise ValueError("Mismatch between the number of values in the protocol (%d) and packet (%d)" % (value_cnt, expected_cnt))


    msg.good("Received packet from BloomBot: Protocol ID: {p_id} | hwID: {hwID}".format(p_id = values[0], hwID = values[1]))

    # Store the parsed values back into the protocol struct
    # Store the special values
    protocol.hwID       = values[1]
    protocol.locationID = values[2]
    protocol.timestamp  = values[3]

    # Store each of the data values
    for i, key in enumerate(protocol.data.keys()):
      protocol.setValue(values[i + NUM_SPECIAL_KEYS], key)


    return protocol



  # ==================================================
  # packPacket - Create a bytestring with the given
  #              packet in prep for transmission.
  # ==================================================
  def packPacket(self, packet):
    data = []
    
    # Check that the required data exists
    if (packet.hwID is None):
      raise ValueError("No device hardware ID is set.")
    
    if (packet.id is None):
      raise ValueError("No protocol ID is set")

    # Add the protocol type (ID) and HW ID 
    data.append(packet.id)
    data.append(packet.hwID)
    
    # Add the remaining data to the packet
    data += packet.getValuesList()
    
    # Pack the data
    return struct.pack(packet.getBytePackStr(isRx = False), *data)
