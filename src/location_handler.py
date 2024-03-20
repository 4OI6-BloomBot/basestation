# =========================================
# Location handler
# Stores locations from the HW by ID and
# corresponds them to entries in the 
# server.
# =========================================

# ================================
# Imports
# ================================
from protocols.location import Location
from wasabi             import msg


class LocationHandler():

  # ========================================================
  # Constructor
  # ========================================================
  def __init__(self):
    # Dictionary to map HW locationIDs to IDs in the server
    self.map = {}


  # ========================================================
  # getServerID - Checks if the ID has been registered and
  #               returns the ID of the obj in the server.
  # ========================================================
  def getServerID(self, hwID, locationID):
    if (hwID not in self.map):
      return None
    
    if (locationID not in self.map[hwID]):
      return None
        
    return self.map[hwID][locationID]
    
    

  # ======================================================
  # If the protocol has a location ID set, update the 
  # ID in the pkt to the corresponding server ID.
  # ======================================================
  def convertHWLocation(self, pkt):
    # Do not convert the HW ID if the packet is a new location
    if (LocationHandler.isLocationPkt(pkt)):
      return None

    # TODO: if the basestation gets a location ID that isn't in the
    #       server it should probably re-queue the packet (?)
    if (pkt.locationID):
      return self.getServerID(pkt.hwID, pkt.locationID)
      
  

  # ========================================================
  # addLocation - Registers the location with the server
  #               and adds the ID of the object to the map.
  # ========================================================
  def addLocation(self, hwID, locationID, response): 

    if (response.status_code == 201):
      response_data = response.json()

      # Check if the device has been registered.
      if (hwID not in self.map):
        self.map[hwID] = {}
        msg.warn(f"First time seeing BloomBot {hwID}, adding to local record.")


      self.map[hwID][locationID] = response_data["id"]


  # ========================================================
  # isLocationPkt - Static helper method to check if the
  #                 packet is a location
  # ========================================================
  def isLocationPkt(pkt):
    return type(pkt) == Location