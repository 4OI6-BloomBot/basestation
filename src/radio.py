# =========================================================
# Radio class to manage interfacing with the NRF24 module
# =========================================================

# ================================================
# Imports
# ================================================
from random import normalvariate
import struct
import sys, time
import pigpio
from   nrf24  import *

class Radio:

  # ================================================
  # Constructor
  # ================================================
  def __init__(self, packet_queue, gpio_port = 8888):
    self.RX_ADDRESS      = "1SNSR"    # TODO: For just Rx we can leave this to match the Tx for now. For bidirectional we need to revisit how to structure the addr.
    self.TX_ADDRESS      = "2SNSR"    
    self.GPIO_PORT    = gpio_port
    self.PACKET_QUEUE = packet_queue

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
    
    self.radio.set_address_bytes(len(self.RX_ADDRESS))
    self.radio.set_address_bytes(len(self.TX_ADDRESS))


  # ==================================================
  # listen - Loop to listen for packets from the Tx
  # ==================================================
  def listen(self):
    # Open connection
    self.radio.open_reading_pipe(RF24_RX_ADDR.P1, self.RX_ADDRESS)

    # Temp/debug
    self.radio.show_registers()

    try:
      print(f'Receive from {self.RX_ADDRESS}')

      while True:

          # Go through each message that is available to parse
          while self.radio.data_ready():
            pipe    = self.radio.data_pipe()    # Pipe is useful if we need to differentiate senders (up to 5)
            payload = self.radio.get_payload()

            # Only process the data if it properly exists
            if (len(payload) > 0):
              self.PACKET_QUEUE.append(payload)
              # self.parseData(payload)

          # Sleep 100 ms.
          time.sleep(0.1)

    except:
      print("[ERROR] Exception thrown in Rx loop") # TODO: Make error verbose
      self.radio.power_down()
      self.gpio.stop()

  def send(self):
    self.radio.open_writing_pipe(self.TX_ADDRESS)

    # Display the content of NRF24L01 device registers.
    self.radio.show_registers()

    count = 0
    print(f'Send to {self.TX_ADDRESS}')
    try:
        while True:

            # Emulate that we read temperature and humidity from a sensor, for example
            # a DHT22 sensor.  Add a little random variation so we can see that values
            # sent/received fluctuate a bit.
            temperature = normalvariate(23.0, 0.5)
            humidity = normalvariate(62.0, 0.5)
            print(f'Sensor values: temperature={temperature}, humidity={humidity}')

            # Pack temperature and humidity into a byte buffer (payload) using a protocol 
            # signature of 0x01 so that the receiver knows that the bytes we are sending 
            # are a temperature and a humidity (see "simple-receiver.py").
            payload = struct.pack("<Bff", 0x01, temperature, humidity)

            # Send the payload to the address specified above.
            self.radio.reset_packages_lost()
            self.radio.send(payload)
            try:
                self.radio.wait_until_sent()
                
            except TimeoutError:
                print("Timeout waiting for transmission to complete.")
                time.sleep(10)
                continue
            
            if self.radio.get_packages_lost() == 0:
                print(f"Success: lost={self.radio.get_packages_lost()}, retries={self.radio.get_retries()}")
            else:
                print(f"Error: lost={self.radio.get_packages_lost()}, retries={self.radio.get_retries()}")

            # Wait 10 seconds before sending the next reading.
            time.sleep(10)

    except:
        print("[ERROR] Exception thrown in Tx loop") # TODO: Make error verbose
        self.radio.power_down()
        self.gpio.stop()

