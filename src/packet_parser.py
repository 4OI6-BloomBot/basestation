# ================================================
# Parser class to decode and reformat the packets
# as JSON objects.
# ================================================

# ==============
# Imports
# ==============
import struct
from   src.protocols import PROTOCOLS, getTypeStr


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
      protocol = PROTOCOLS[protocol_id]
    else:
      print("[ERROR] Could not find protocol") # TODO: Make more verbose


    # Construct the string for the unpack function
    unpack_str = "<B"
    for data in protocol["data"]:
      unpack_str += getTypeStr(data["type"])

    # Unpack the binary data:
    #   < - Little endian
    #   B - unsigned char
    #   f - float (x2)
    values = struct.unpack(unpack_str, packet)
    print(f'Protocol: {values[0]}, temperature: {values[1]}, humidity: {values[2]}')

    # Store the parsed values back into the protocol struct
    for i in range(1, len(values)):
      protocol["data"][i - 1]["value"] = values[i]

    return protocol
    

