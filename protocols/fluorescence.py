# =============================================
# Temperature protocol class
# =============================================

# ============================
# Imports
# ============================
from .measurement import Measurement
from .base        import PROTOCOLS


class Fluorescence(Measurement):

  data = {
    "value" : {
      "type"      : float,
      "precision" : 6
    }
  }

  name      = "Fluorescence"
  sensor_ID = 3


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__()



# =============================================
# Add Temperature to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[5] = Fluorescence