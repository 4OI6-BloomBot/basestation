# ================================================
# Middleware to manage communication with the
# server.
# ================================================

# ==============
# Imports
# ==============
import requests, os
from   .location_handler  import LocationHandler
from   protocols.config import Config

class ServerMiddleware():

  API_ADDR = os.getenv("API_ADDR")

  # ================================================== 
  # Constructor - Requires a shared queue that is 
  #               populated with parsed packets
  # ==================================================
  def __init__(self, server_tx_queue, server_rx_queue):
    self.SERVER_TX_QUEUE = server_tx_queue
    self.SERVER_RX_QUEUE = server_rx_queue
    self.location        = LocationHandler()


  # ==================================================
  # monitorTxQueue - Monitor the Tx queue for new 
  #                  entries and parse them.
  # ==================================================
  def monitorTxQueue(self):
    while(True):
      if len(self.SERVER_TX_QUEUE) > 0:
        pkt      = self.SERVER_TX_QUEUE.pop(0)
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
    url = self.getAPIURL() + "config/" + str(hwID)

    # Query the server
    response = requests.get(url)
    data     = response.json()

    # If there is an error response
    # TODO: Handle and make verbose.
    if (response.status_code != 200):
      print("ERROR")
      return

    # Create a new Config packet and add it to the queue
    config      = Config()
    config.hwID = hwID
    config.parseJSON(data)

    self.SERVER_RX_QUEUE.append(config)