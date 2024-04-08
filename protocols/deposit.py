# =============================================
# Temperature protocol class
# =============================================

# ============================
# Imports
# ============================
from .measurement import Measurement
from .base        import PROTOCOLS


class Deposit(Measurement):

  data = {
    "value" : {
      "type"      : float,
      "precision" : 6
    }
  }

  # Override endpoint
  endpoint  = "deposits"

  name      = "Deposit"
  sensor_ID = 0


  # =============================================
  # Constructor
  # ============================================= 
  def __init__(self):
    super().__init__()



# =============================================
# Add Temperature to protocol type dictionary
# TODO: Cleaner way to do this?
# =============================================
PROTOCOLS[6] = Deposit