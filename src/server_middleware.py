# ================================================
# Middleware to manage communication with the
# server.
# ================================================

# ==============
# Imports
# ==============
import requests

class ServerMiddleware():

  API_ADDR = "http://192.168.1.108:8080/api/"

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
  def sendData(self, protocol):

    # TODO: Need to parse hwID from packet.
    protocol.hwID = 123

    json = protocol.toJSON()
    
    # Construct POST data
    headers = {'Content-Type': 'application/json'}
    url     = ServerMiddleware.API_ADDR + protocol.endpoint
    
    # Need to ensure that there is a trailing / in the URL
    if (url[len(url) - 1] != '/'):
      url += "/"

    # Send POST request
    response = requests.post(url, json = json, headers = headers)
    
    # TODO: Handle response
    print(response)