# This is sample code from one of the prototypes
# The device requires analog, digital, pulse and basic input,
# as well as libraries related to time
# and the board itself
import board
import busio
import neopixel
import time
import pulseio
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
# The buzzer is the alarm
buzzer_pin = board.D13
# Set the tone frequency in Hz
tone = 4200
# The sound is a wave
buzzer = pulseio.PWMOut(buzzer_pin, variable_frequency=True)
# The board ships with a native, incredibly bright LED
# The led needs to be turned off on startup, it turns on in case of error
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
# UART is the serial device, in this case an XBee 3
uart = busio.UART(board.TX, board.RX, baudrate=57600)
# Initialize the two buttons used
button = DigitalInOut(board.D11)
button.direction = Direction.INPUT
button.pull = Pull.DOWN
buttonB = DigitalInOut(board.D12)
buttonB.direction = Direction.INPUT
buttonB.pull = Pull.DOWN
# There is also an installed led used to give information on battery life
led2 = DigitalInOut(board.D10)
led2.direction = Direction.OUTPUT
# On startup the native led is turned off
led[0] = (0, 0, 0)
# The battery has a bin on the board
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
# Define the function used to calculate the voltage coming from the battery
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
# When connected to a console, the device outputs debugging information
# at points throughout the code
print("setup successful")
while True:
    # Upon pressing the red button, the device sends out a
    # signal and also turns on the speaker
    if button.value:
        print("pressed")
        uart.write('a')
        buzzer.frequency = tone
        buzzer.duty_cycle = 2**15
        print("done")
    time.sleep(2)
    # Upon pressing the other button, the device
    # turns off the speaker if it is on, and also
    # checks the battery, and displays charge status
    if buttonB.value:
        # Turn off the speaker
        buzzer.duty_cycle = 0
        # Call the voltage function
        battery_voltage = get_voltage(vbat_voltage)
        print("VBat voltage: {:.2f}".format(battery_voltage))
        # 3.30V is near the failure voltage, it was chosen as the point
        # When the user should choose to charge the battery
        if battery_voltage > 3.30:
            # If the battery is charged enough,
            # The light is constant for 2 seconds
            led2.value = True
            time.sleep(2.0)
            led2.value = False
        if battery_voltage <= 3.30:
            x = 0
            # If the battery is not charged enough the light will flash
            while x < 8:
                led2.value = True
                time.sleep(.2)
                led2.value = False
                time.sleep(.2)
                x = x + 1
    # The device searches for a signal in the queue
    data = uart.read(1)  # read a byte
    # Initialize a variable to hold what the signal information put in a string
    datastr = None
    # If something has been read, and is in the binary form,
    # which is how the XBee transmits data,
    # it reads it into a string
    if data is not None:
        datastr = ''.join([chr(b) for b in data])
        print(datastr, end="")
    # If the data is in the correct form, the device turns on the speaker to
    # notify the user that someone is in distress
    # This device is filtering for and sending on a network set to the 'a'
    # character, that is adjustable however
    # To have this device span multiple networks, it could have:
    # uart.write('a')
    # uart.write('b'), thereby sending both signals and
    # If datastr is 'a' or datastr is 'b' thereby looking for both networks
    if datastr is 'a':  # Data was received
        print("Read something")
        print(data)
        buzzer.frequency = tone
        buzzer.duty_cycle = 2**15
        time.sleep(4.0)
        buzzer.duty_cycle = 0
