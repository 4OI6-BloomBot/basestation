# 
# Define the protocols
# 

# ======================
# Data structure:
# ======================
# (Key is tied to the protocol id)
# name: Name of datatype
# id:   Protocol ID number
# data: List of all data sections of the packet
#     name: Name of data
#     type: Datatype
from abc import ABCMeta, abstractmethod


# =============================================
# Protocol base class.
# TODO: Needs an endpoint field for the API
# =============================================
class Protocol(metaclass=ABCMeta):
  
  # =============================================
  # Constructor
  # =============================================
  def __init__(self, id):
    self.id = id

    # Set defaults to None
    self.hwID = None


  # =============================================
  # Each child needs to declare the data object
  # =============================================
  @property
  @abstractmethod
  def data(self):
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


    # Unpack the individual values into the JSON object
    # Check that the value has been set before parsing
    for key in self.data:
      if ("value" not in self.data[key]):
        raise ValueError("Value not provided for {name}".format(name = key))
      else:
        json[key] = self.data[key]["value"]

    return json


# =============================================
# Location protocol class
# =============================================
class Location(Protocol):

  # =============================================
  # Declare the data structure for the protocol
  # =============================================
  data = {
    "latitude" : {
      "type" : float
    },
    "longitude" : {
      "type" : float
    }
  }

  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__(1)


# =============================================
# Declare protocol types in a dictionary with
# the key as their IDs
# =============================================
PROTOCOLS = {
  1 : Location
} 


# Helper fn
def getTypeStr(t):
  if (t == float): return "f"