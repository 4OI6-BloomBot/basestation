# =============================================
# Location protocol class
# =============================================

# ============================
# Imports
# ============================
from base import BaseProtocol, PROTOCOLS


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


# =============================================
# Add Location to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[1] = Location