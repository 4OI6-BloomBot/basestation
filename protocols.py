# 
# Define the protocols
# 

# ======================
# Data structure:
# ======================
# name: Name of datatype
# id:   Protocol ID number
# data: List of all data sections of the packet
#     name: Name of data
#     type: Datatype
PROTOCOLS = [
  {
    "name" : "location",
    "id"   : 1,
    "data" : [
      {
        "name" : "latitude",
        "type" : float
      },
      {
        "name" : "longitude",
        "type" : float
      }
    ]
  }
]