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


  def listen(self):
    # Open connection
    self.radio.open_reading_pipe(RF24_RX_ADDR.P1, self.address)

    # Temp:
    self.radio.show_registers()


    # Enter a loop receiving data on the address specified.
    try:
      print(f'Receive from {self.ADDRESS}')

      while True:

          # As long as data is ready for processing, process it.
          while self.radio.data_ready():
              # Read pipe and payload for message.
              pipe    = self.radio.data_pipe()
              payload = self.radio.get_payload()

              # Resolve protocol number.
              protocol = payload[0] if len(payload) > 0 else -1

              hex = ':'.join(f'{i:02x}' for i in payload)

              # Show message received as hex.
              print(f" pipe: {pipe}, len: {len(payload)}, bytes: {hex}")

              # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
              # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
              if len(payload) == 9 and payload[0] == 0x01:
                  values = struct.unpack("<Bff", payload)
                  print(f'Protocol: {values[0]}, temperature: {values[1]}, humidity: {values[2]}')

          # Sleep 100 ms.
          time.sleep(0.1)
    except:
      self.radio.power_down()
      self.gpio.stop()
