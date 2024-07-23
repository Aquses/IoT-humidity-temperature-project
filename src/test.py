import machine
import time

pin = machine.Pin(29, machine.Pin.OUT)  # Replace with your actual pin number
pin.value(1)  # Set the pin high
time.sleep(1)
pin.value(0) 