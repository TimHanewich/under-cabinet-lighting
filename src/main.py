import time
import machine
import colors
import neopixel
import tools

# Mode Options
MODE_SOLID_A:int = 0 # Full "warm" color
MODE_SOLID_B:int = 1 
MODE_SOLID_C:int = 2
MODE_SOLID_D:int = 3 # Full "cold" color
MODE_RAINBOW:int = 4 # rainbow color

# What mode we are in
MODE:int = MODE_SOLID_A # default @ MODE_SOLID_A

def next_mode() -> None:
    """Increments the current mode to the next mode"""

    # declare globals we need to call to in this function
    global MODE_SOLID_A
    global MODE_SOLID_B
    global MODE_SOLID_C
    global MODE_SOLID_D
    global MODE_RAINBOW
    global MODE

    if MODE >= MODE_RAINBOW: # if we are on the last one (will need to change this if I add more modes)
        MODE = 0 # go back to the first mode (0)
    else: # if we are not on the last mode
        MODE = MODE + 1 # increment by 1 (to the next mode, they should be in order with no skips...)

# set up PotReader
pr:tools.PotReader = tools.PotReader(28)

# set up button
button = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)

# set up neopixels
nm:neopixel.NeopixelManager = neopixel.NeopixelManager(neopixel.Neopixel(15, 0, 0, "GRB"))

# infinite loop!
button_last_read_as_depressed:bool = False
while True:

    # handle button depressed
    if button_last_read_as_depressed: # if we are waiting for the button to be lifted
        if button.value() == 1: # it is back to being let go of, so increment
            next_mode()
            button_last_read_as_depressed = False
    else: # we are awaiting for it to be pressed again!
        if button.value() == 0: # 0 is pressed ("pulled down" to GND)
            button_last_read_as_depressed = True
    
    # Read pot
    pot_reading:float = pr.read()

    # display according to the mode and pot reading we are in!
    if MODE == MODE_SOLID_A: # full warm
        color:tuple[int, int, int] = tools.warmth(0.0)
        color = colors.brighten(color, pot_reading)
        nm.fill(color)
        nm.show()
    elif MODE == MODE_SOLID_B:
        color:tuple[int, int, int] = tools.warmth(0.333)
        color = colors.brighten(color, pot_reading)
        nm.fill(color)
        nm.show()
    elif MODE == MODE_SOLID_C:
        color:tuple[int, int, int] = tools.warmth(0.667)
        color = colors.brighten(color, pot_reading)
        nm.fill(color)
        nm.show()
    elif MODE == MODE_SOLID_D: # full cold
        color:tuple[int, int, int] = tools.warmth(1.0)
        color = colors.brighten(color, pot_reading)
        nm.fill(color)
        nm.show()
    elif MODE == MODE_RAINBOW:
        rainbow_slices:list[tuple[int, int, int]] = colors.spectrum_slices(15)
        for i in range(0, len(rainbow_slices)):
            icolor = rainbow_slices[i] # select
            icolor = colors.brighten(icolor, pot_reading) # brighten/dim according to pot reading
            nm.set_pixel(i, icolor)
        nm.show()

    # wait
    time.sleep(0.01)