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
        pkt      = self.SERVER_QUEUE.pop(0)
        response = self.sendData(pkt)

        # Update the location handler if it was a location pkt
        if (LocationHandler.isLocationPkt(pkt)):
          self.location.addLocation(pkt.hwID, pkt.locationID, response)


  # ======================================================
  # getAPIURL - Accessor method to make sure that the API
  #             URL is formatted correctly.
  # ======================================================
  def getAPIURL(self):
    url = self.API_ADDR
    
    # Need to ensure that there is a trailing / in the URL
    if (url[len(url) - 1] != '/'):
      url += "/"

    return url


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
    url     = self.getAPIURL() + pkt.endpoint
    
    # Need to ensure that there is a trailing / in the URL
    if (url[len(url) - 1] != '/'):
      url += "/"

    # Send POST request
    response = requests.post(url, json = json, headers = headers)
    

    return response
  

  # =====================================================
  # getConfig - Queries the server for the device config
  # =====================================================
  def getConfig(self, hwID):

    # Create the endpoint URL
    url = self.getAPIURL() + "config/" + hwID

    # Query the server
    response = requests.get(url)
    data     = response.json()

    # If there is an error response
    if (response.status_code != 200):
      print("ERROR")

    return