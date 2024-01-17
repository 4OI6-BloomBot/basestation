# =========================================
# Location handler
# Stores locations from the HW by ID and
# corresponds them to entries in the 
# server.
# =========================================

# ================================
# Imports
# ================================

class LocationHandler():

  # ========================================================
  # Constructor
  # ========================================================
  def __init__(self, server_middleware):
    # Dictionary to map HW locationIDs to IDs in the server
    self.map    = {}
    self.server = server_middleware


  # ========================================================
  # getServerID - Checks if the ID has been registered and
  #               returns the ID of the obj in the server.
  # ========================================================
  def getServerID(self, hwID):
    if hwID in self.map:
      return self.map[hwID]
    
  
  # ========================================================
  # addLocation - Registers the location with the server
  #               and adds the ID of the object to the map.
  # ========================================================
  def addLocation(self, location):
    response = self.server.sendData(location)
    
    if (response.status_code == 201):
      response_data                 = response.json()
      self.map[location.locationID] = response_data["id"]