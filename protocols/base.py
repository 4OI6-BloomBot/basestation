# ================================
# Base protocol definition
# ================================

# ================================
# Imports
# ================================
import math
from   abc import ABCMeta, abstractmethod

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

  @property
  @abstractmethod
  def name(self):
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


    # Apply the set precision to the data
    self.applyPrecision()

    # Update the data in the JSON field accordingly
    self.packJSONData(json)
  

    return json
  
  
  # ==================================================
  # Method implemented by children to handle adding their
  # data to the JSON obj
  # ==================================================
  @abstractmethod
  def packJSONData(self, json):
    pass


  # ==================================================
  # Construct the string for the unpack function
  # ==================================================
  def getUnpackStr(self):
    # < - Little endian
    # B - Unsigned char (ID)
    # B - Unsigned char (hwID)
    unpack_str = "<BB"

    for key in self.data:
      unpack_str += getTypeStr(self.data[key]["type"])

    return unpack_str


  # ==================================================
  # If the value and precision keys are set, apply
  # the rounding to the value
  # ==================================================
  def applyPrecision(self):
    for key in self.data:
      if (self.data[key].keys() >= {"precision", "value"}):
          
          # Python's round function only accounts for the number of decimal points. The server needs a consistent total number
          # of digits. Therefore subtract the int portion from the precision to get the number of digits we need to round.
          # TODO: This would affect the precision of some values. Can likely ignore since our equip is not sensitive
          #       enough for 10^-6/5 or what have you
          rounding_digits = self.data[key]["precision"] - int(math.ceil(math.log10(abs(self.data[key]["value"]))))
          
          self.data[key]["value"] = round(self.data[key]["value"], rounding_digits)



# ==================================================
# Helper function to generate the chars associated
# with the type
# ==================================================
def getTypeStr(t):
  if (t == float): return "f"