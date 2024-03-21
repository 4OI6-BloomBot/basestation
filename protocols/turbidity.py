# =============================================
# Temperature protocol class
# =============================================

# ============================
# Imports
# ============================
from .measurement import Measurement
from .base        import PROTOCOLS


class Turbidity(Measurement):

  data = {
    "value" : {
      "type"      : float,
      "precision" : 6
    }
  }

  name      = "Turbidity"
  sensor_ID = 2


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__()



# =============================================
# Add Temperature to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[4] = Turbidity