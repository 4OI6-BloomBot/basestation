# =============================================
# Location protocol class
# =============================================

# ============================
# Imports
# ============================
from .base import BaseProtocol, PROTOCOLS


class Config(BaseProtocol):

  # =============================================
  # Declare the data structure for the protocol
  # =============================================
  data = {
    "id" : {
      "type": int
    },
    "tempThresh" : {
      "type"      : float,
      "precision" : 6
    },
    "deltaTempThresh" : {
      "type"      : float,
      "precision" : 6
    },
    "turbThresh" : {
      "type"      : float,
      "precision" : 6
    },
    "deltaTurbThresh" : {
      "type"      : float,
      "precision" : 6
    },
    "fluoroThresh" : {
      "type"      : float,
      "precision" : 6
    }
  }

  endpoint = "config"
  name     = "Config"


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__(1)


  # =============================================
  # Won't be used for the Config protocol
  # =============================================
  def packJSONData(self, json):
    pass


  def parseJSON(self, json):
    for key in json:
      if (key in self.data):
        self.setValue(json[key], key)

      # TODO: Should log params that are not in the param
      # raise ValueError("Parameter {p} does not exist in the Config protocol.".format(p = key))
        

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
# Add Config to protocol type dictionary
# =============================================
PROTOCOLS[1] = Config