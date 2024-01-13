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
PROTOCOLS = {}

# Location Protocol
PROTOCOLS[1] =  {
                  "name" : "location",
                  "id"   : 1,
                  "data" : [
                    {
                      "name" : "latitude",
                      "type" : float,
                    },
                    {
                      "name" : "longitude",
                      "type" : float
                    }
                  ]
                }

# TODO: Needs an endpoint field for the API

# Helper fn
def getTypeStr(t):
  if (t == float): return "f"