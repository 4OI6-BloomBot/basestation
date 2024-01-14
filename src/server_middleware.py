# ================================================
# Middleware to manage communication with the
# server.
# ================================================

# ==============
# Imports
# ==============
import requests

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
    json = self.createJSON(data)
    print("TODO: Send data to server.")


  # ==================================================
  # createJSON - Convert the datapacket to JSON that
  #              can be interpreted by the API
  # ==================================================
  def createJSON(self, pkt):
    json = {}
    
    # TODO: Need to pull the device information from the HW
    #       Packet parser needs to be updated to account for this.
    json["device"] = {
      "hwID" : "123"
    }

    # Unpack the individual values into the JSON object
    for val in pkt["data"]:
      json[val["name"]] = val["value"]

    return json