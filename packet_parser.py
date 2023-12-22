# ================================================
# Parser class to decode and reformat the packets
# as JSON objects.
# ================================================


class PacketParser:

  def __init__(self, packet_queue):
    self.PACKET_QUEUE = packet_queue