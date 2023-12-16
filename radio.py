# =========================================================
# Radio class to manage interfacing with the NRF24 module
# =========================================================

# Imports
import sys
import pigpio
from   nrf24  import *

import struct #?
import time

class Radio:

  # ================================================
  # Constructor
  # ================================================
  def __init__(self, gpio_port = 8888):
    self.ADDRESS   = "1SNSR"    # TODO: For just Rx we can leave this to match the Tx for now. For bidirectional we need to revisit how to structure the addr.
    self.GPIO_PORT = gpio_port

    # Attempt to connect to the Pi GPIO daemon
    self.gpio = pigpio.pi("localhost", self.GPIO_PORT)
    
    if not self.gpio.connected:
      print("[ERROR] Could not connect to the GPIO daemon. Please make sure it is running.")
      sys.exit()

    # Create the NRF24 object
    self.radio = NRF24(self.gpio, 
                     ce           = 25,
                     payload_size = RF24_PAYLOAD.DYNAMIC,
                     channel      = 100,
                     data_rate    = RF24_DATA_RATE.RATE_250KBPS,
                     pa_level     = RF24_PA.MIN) # TODO: In production this should he high.
    
    self.radio.set_address_bytes(len(self.ADDRESS))


  # ==================================================
  # listen - Loop to listen for packets from the Tx
  # ==================================================
  def listen(self):
    # Open connection
    self.radio.open_reading_pipe(RF24_RX_ADDR.P1, self.ADDRESS)

    # Temp:
    self.radio.show_registers()


    # Enter a loop receiving data on the address specified.
    try:
      print(f'Receive from {self.ADDRESS}')

      while True:

          # Go through each message that is available to parse
          while self.radio.data_ready():
            pipe    = self.radio.data_pipe()    # Pipe is useful if we need to differentiate senders (up to 5)
            payload = self.radio.get_payload()

            # Only process the data if it properly exists
            if (len(payload) > 0):
              self.parseData(payload)

          # Sleep 100 ms.
          time.sleep(0.1)
    except:
      print("[ERROR] Exception thrown in Rx loop") # TODO: Make error verbose
      self.radio.power_down()
      self.gpio.stop()


  # ==================================================
  # parseData - Parse a given packet and match it to
  #             a protocol.
  # ==================================================
  def parseData(self, payload):

    protocol = payload[0]

    # TODO: This is the exisiting payload structure from the demo program.
    #       Need to work out a datastructure to maintain these.
    if len(payload) == 9 and payload[0] == 0x01:
      # Unpack the binary data:
      #   < - Little endian
      #   B - unsigned char
      #   f - float (x2)
      values = struct.unpack("<Bff", payload)
      print(f'Protocol: {values[0]}, temperature: {values[1]}, humidity: {values[2]}')