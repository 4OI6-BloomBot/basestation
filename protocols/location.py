# =============================================
# Location protocol class
# =============================================

# ============================
# Imports
# ============================
from base import BaseProtocol


class Location(BaseProtocol):

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