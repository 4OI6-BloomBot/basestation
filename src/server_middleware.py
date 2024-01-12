# ================================================
# Middleware to manage communication with the
# server.
# ================================================

# ==============
# Imports
# ==============


class ServerMiddleware():

  # ================================================== 
  # Constructor - Requires a shared queue that is 
  #               populated with parsed packets
  # ==================================================
  def __init__(self, server_queue):
    self.SERVER_QUEUE = server_queue


  # ==================================================
  # monitorServerQueue - Monitor the queue for new 
  #                      entries and parse them.
  # ==================================================
  def monitorServerQueue(self):
    while(True):
      if len(self.SERVER_QUEUE) > 0:
        self.sendData(self.SERVER_QUEUE.pop())


  # ==================================================
  # sendData - Send the given packet to the server
  # ==================================================
  def sendData(self, data):
    print("TODO: Send data to server.")