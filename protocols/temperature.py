# =============================================
# Temperature protocol class
# =============================================

# ============================
# Imports
# ============================
from .measurement import Measurement
from .base        import PROTOCOLS


class Temperature(Measurement):

  data = {
    "value" : {
      "type"      : float,
      "precision" : 6
    }
  }

  name      = "Temperature"
  sensor_ID = 1


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__()



# =============================================
# Add Temperature to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[3] = Temperature