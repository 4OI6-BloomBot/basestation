# ================================================
# Middleware to manage communication with the
# server.
# ================================================

# ==============
# Imports
# ==============
import requests, os
from   .location_handler import LocationHandler

class ServerMiddleware():

  API_ADDR = os.getenv("API_ADDR")

  # ================================================== 
  # Constructor - Requires a shared queue that is 
  #               populated with parsed packets
  # ==================================================
  def __init__(self, server_queue):
    self.SERVER_QUEUE = server_queue
    self.location     = LocationHandler()


  # ==================================================
  # monitorServerQueue - Monitor the queue for new 
  #                      entries and parse them.
  # ==================================================
  def monitorServerQueue(self):
    while(True):
      if len(self.SERVER_QUEUE) > 0:
        pkt      = self.SERVER_QUEUE.pop()
        response = self.sendData(pkt)

        # Update the location handler if it was a location pkt
        if (LocationHandler.isLocationPkt(pkt)):
          self.location.addLocation(pkt.locationID, response)


  # ==================================================
  # sendData - Send the given packet to the server
  # ==================================================
  def sendData(self, pkt):

    json = pkt.toJSON()

    # Add location data if available
    location_id = self.location.convertHWLocation(pkt)
    if (location_id):
      json["location"] = location_id

    # Construct POST data
    headers = {'Content-Type': 'application/json'}
    url     = ServerMiddleware.API_ADDR + pkt.endpoint
    
    # Need to ensure that there is a trailing / in the URL
    if (url[len(url) - 1] != '/'):
      url += "/"

    # Send POST request
    response = requests.post(url, json = json, headers = headers)
    

    return response