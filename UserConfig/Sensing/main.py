# standard imports
from time import sleep
from signal import pause

# installed inports
from gpiozero import Button

# local imports
from utilities.mqtt_out import publish

# Assumes sensors have NPN NO style outputs,
# ie output connection is normally high impedance but becomes connected to ground when sensor triggered.

# Define on what pin numbers the sensors are connected to the Raspberry Pi
# BCM pin numbering scheme
MyButtons = [Button(pin_number) for pin_number in [5,6,19,26]]

# Also select one to also act as the trigger
CounterTrigger = Button(13)

# When this button is held for 0.5s, publish a count of how many buttons are currently pressed
CounterTrigger.hold_time = 0.5

def on_trigger_hold():
    publish( {"machine": "MachineNameHere"} | {"buttons_pressed" : sum([button.value for button in MyButtons])} )

CounterTrigger.when_held = on_trigger_hold

# Keep this script running whenever the solution is up
pause()
