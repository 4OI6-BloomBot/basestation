# =============================================
# Measurement protocol class
# The measurement protocol should not be used
# on its own. Instead, specific sensors should
# extend it.
# =============================================

# ============================
# Imports
# ============================
from abc   import ABCMeta, abstractmethod
from .base import BaseProtocol


class Measurement(BaseProtocol, metaclass = ABCMeta):

  # Set endpoint but leave others abstracted
  endpoint = "measurement"

  # Add sensor ID field to match with server declaration
  @property
  @abstractmethod
  def sensor_ID(self):
    pass


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__(2)


  # =============================================
  # Translate single value entry
  # =============================================
  def setValue(self, val, key = "value"):
    BaseProtocol.setValue(self, val, key)

  # =============================================
  # Unpack the value into the JSON object.
  # Check that the value has been set before
  # parsing
  # =============================================
  def packJSONData(self, json):
    if ("value" not in self.data):
      raise ValueError("Value not provided for {name}".format(name = self.name))
    else:
      json["value"] = self.data["value"]["value"]