# ================================================
# Middleware to manage communication with the
# server.
# ================================================

# ==============
# Imports
# ==============
import requests, os, time
from   .location_handler  import LocationHandler
from   protocols.config   import Config
from   wasabi             import msg

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

    # Display information to the console at startup
    msg.info("BloomBot server API endpoint: " + self.getAPIURL())


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
          

        # Print the results
        if (not response.ok):
          msg.fail(f"Received response code {response.status_code} from the server when sending {pkt.name} packet from BloomBot {pkt.hwID}!")
        else:
          msg.good(f"Successfully sent {pkt.name} from BloomBot {pkt.hwID} to server.")


  # =======================================================
  # pollConfig - Poll the server for configurations.
  #              TODO: This is a bit messy right now, 
  #                    Shouldn't keep sending configs
  #                    Relying on the location map works
  #                    but is not ideal.
  # =======================================================
  def pollConfig(self):
    while(True):
      for hwID in self.location.map:
        self.getConfig(hwID)
      
      # Wait before polling again
      time.sleep(30)


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
    if (not response.ok):
      msg.fail("Received response code {} from the server when polling for configurations!".format(response.status_code))
      return
    
    msg.info(f"Received config for BloomBot {hwID} from the server.")

    # Create a new Config packet and add it to the queue
    config      = Config()
    config.hwID = hwID
    config.parseJSON(data)

    self.SERVER_RX_QUEUE.append(config)