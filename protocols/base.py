# ================================
# Base protocol definition
# ================================

# ================================
# Imports
# ================================
from abc import ABCMeta, abstractmethod

# =============================================
# Declare protocol types in a dictionary with
# the key as their IDs
# =============================================
PROTOCOLS = {}


class BaseProtocol(metaclass = ABCMeta):
  
  # =============================================
  # Constructor
  # =============================================
  def __init__(self, id):
    self.id = id

    # Set defaults to None
    self.hwID = None


  # =============================================
  # Each child needs to declare the following
  # properties
  # =============================================
  @property
  @abstractmethod
  def data(self):
    pass

  @property
  @abstractmethod
  def endpoint(self):
    pass


  # =============================================
  # Check that the data name/key exists in the 
  # definition.
  # =============================================
  def checkDataKey(self, key):
    return key in self.data


  # =============================================
  # Helper method to set a data value
  # =============================================
  def setValue(self, key, val):
    # Check that the data key exists
    if (not self.checkDataKey(key)):
      raise ValueError("{key} does not exist in packet data".format(key = key))

    # Check that the passed value has the expected type
    if (self.data[key]["type"] != type(val)):
      raise TypeError("Value is of type {val_type}. Expected {exp_type}.".format(val_type = type(val), exp_type = self.data[key]["type"]))

    self.data[key]["value"] = val


  # ==================================================
  # toJSON - Convert the datapacket to JSON that
  #          can be interpreted by the API
  # ==================================================
  def toJSON(self):
    json = {}
    
    # Make sure that the device ID is set
    if (self.hwID is None):
      raise ValueError("No device hardware ID is set.")

    json["device"] = {
      "hwID" : self.hwID
    }

    # Update the data in the JSON field accordingly
    self.packJSONData(json)

    return json
  
  
  @abstractmethod
  def packJSONData(self, json):
    pass


  # ==================================================
  # Construct the string for the unpack function
  # ==================================================
  def getUnpackStr(self):
    # < - Little endian
    # B - Unsigned char (ID)
    unpack_str = "<B"

    for key in self.data:
      unpack_str += getTypeStr(self.data[key]["type"])

    return unpack_str


# ==================================================
# Helper function to generate the chars associated
# with the type
# ==================================================
def getTypeStr(t):
  if (t == float): return "f"