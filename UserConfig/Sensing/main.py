"""main.py that prepares the Sensing service module for Count Monitoring.

All configuration is done in the Settings section.
Assumes sensors have pulls external to the GPIO interface.
"""

## -- Imports ---------------------------------------------------------------------

# Standard imports
import time

# Installed inports
#none used directly, but smbus2 is used by sequent_16inputs

# Local imports
from utilities.mqtt_out import publish
from hardware.ICs.sequent_16inputs import Sequent16inputsHAT

## --------------------------------------------------------------------------------




## -- Settings  -------------------------------------------------------------------

# Data tags
machine_name = "Machine_Name_Here"

# Timing
trigger_hold_time = 0.5 # seconds the trigger has to be held to initiate the count

# Pinout
input_interface = Sequent16inputsHAT(0)
trigger_channel = 1
count_channels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

# Wiring polarity
active_state = 0

# Describe events by the number of sensors that were active when the trigger sensor was held
events = {
    1: "Undefined",
    2: "Undefined",
    3: "Fancoil_600",
    4: "Fancoil_600",
    5: "Fancoil_900",
    6: "Fancoil_900",
    7: "Fancoil_1200",
    8: "Fancoil_1200",
    9: "Fancoil_1500",
    10: "Fancoil_1500",
    11: "Fancoil_1800",
    12: "Fancoil_1800",
    13: "Fancoil_2050",
}

## --------------------------------------------------------------------------------




## -- Main Loop -------------------------------------------------------------------

while True:

    start_time = time.time()

    while input_interface.read_single_channel(trigger_channel) == active_state:

        if time.time() > (start_time + trigger_hold_time):

            buttons_pressed = input_interface.read_multiple_channels(count_channels).count(active_state)
            publish( {
                "machine"         : machine_name,
                "buttons_pressed" : buttons_pressed,
                "event"           : events[buttons_pressed],
                } )

            while input_interface.read_single_channel(trigger_channel) == active_state:
                pass            # Wait for the trigger to be released
            break               # Exit the while input_interface... loop and restart the main loop

## --------------------------------------------------------------------------------
