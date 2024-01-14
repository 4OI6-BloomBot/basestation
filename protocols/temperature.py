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
    "type" : float
  }

  name = "Temperature"


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__()



# =============================================
# Add Temperature to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[2] = Temperature