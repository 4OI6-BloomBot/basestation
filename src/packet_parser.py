# ================================================
# Parser class to decode and reformat the packets
# as JSON objects.
# ================================================

# ==============
# Imports
# ==============
import struct
from   protocols.base import PROTOCOLS, NUM_SPECIAL_KEYS


class PacketParser:

  # ================================================== 
  # Constructor - Requires a shared queue that is 
  #               populated with received packets.
  # ==================================================
  def __init__(self, packet_queue, data_queue):
    self.PACKET_QUEUE = packet_queue
    self.DATA_QUEUE   = data_queue


  # ==================================================
  # monitorQueue - Monitor the queue for new entries
  #                and parse them.
  # ==================================================
  def monitorRxQueue(self):
    while (True):
      if len(self.PACKET_QUEUE) > 0:
        result = self.parsePacket(self.PACKET_QUEUE.pop())

        # Only process the result if it succeed
        if result is not None:
          self.DATA_QUEUE.append(result)


  # ==================================================
  # parseData - Parse a given packet and match it to
  #             a protocol.
  # ==================================================
  def parsePacket(self, packet):

    protocol_id = packet[0]

    # Find the protocol in the map
    if (protocol_id in PROTOCOLS):
      protocol = PROTOCOLS[protocol_id]()
    else:
      raise ValueError("[ERROR] Could not find protocol with id={id}".format(id = protocol_id))


    values = struct.unpack(protocol.getUnpackStr(), packet)

    # Check if the number of values matches what is expected for the datatype
    if (len(protocol.data.keys()) != len(values) - NUM_SPECIAL_KEYS):
      raise ValueError("Mismatch between the number of values in the protocol ({keys}) and packet ({pkt})".format(
                        keys = len(protocol.data.keys()), 
                        pkt  = len(values) - 1
                      ))


    print("[INFO] Received packet: Protocol ID: {p_id} | hwID: {hwID}".format(p_id = values[0], hwID = values[1]))

    # Store the parsed values back into the protocol struct
    for i, key in enumerate(protocol.data.keys()):
      protocol.setValue(key, values[i + NUM_SPECIAL_KEYS])


    return protocol
    

