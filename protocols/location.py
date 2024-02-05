# =============================================
# Location protocol class
# =============================================

# ============================
# Imports
# ============================
from .base import BaseProtocol, PROTOCOLS


class Location(BaseProtocol):

  # =============================================
  # Declare the data structure for the protocol
  # =============================================
  data = {
    "latitude" : {
      "type"      : float,
      "precision" : 6
    },
    "longitude" : {
      "type"      : float,
      "precision" : 6
    }
  }

  endpoint = "location"
  name     = "Location"


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__(1)


  # =============================================
  # Unpack the individual values into the JSON 
  # object. Check that the value has been set
  # before parsing
  # =============================================
  def packJSONData(self, json):
    for key in self.data:
      if ("value" not in self.data[key]):
        raise ValueError("Value not provided for {name}".format(name = key))
      else:
        json[key] = self.data[key]["value"]


  # ==================================================
  # Returns a list containing all values of the packet
  # ==================================================
  def getValuesList(self):
    values = []

    for key in self.data:
      if ("value" not in self.data[key]):
        raise ValueError("Value not provided for {name}".format(name = key))
      else:
        values.append(self.data[key]["value"])
    
    return values


# =============================================
# Add Location to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[1] = Location