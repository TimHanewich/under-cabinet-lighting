import time
import machine
import colors
import neopixel
import tools
import WeightedAverageCalculator

# SETTINGS
DEAD_BATTERY_VOLTAGE:float = 6.1 # voltage of a double-18650 (in series) battery pack that is determined to be dead. Once it hits, the program will stop.

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

# set up ADC pin for battery voltage reading via voltage divider
vbat_adc = machine.ADC(machine.Pin(26, machine.Pin.IN))
vbat_wac:WeightedAverageCalculator.WeightedAverageCalculator = WeightedAverageCalculator.WeightedAverageCalculator(0.95)

# set up PotReader
pr:tools.PotReader = tools.PotReader(28)

# set up button
button = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)

# set up neopixels
nm:neopixel.NeopixelManager = neopixel.NeopixelManager(neopixel.Neopixel(15, 0, 0, "GRB"))

# infinite loop!
button_last_read_as_depressed:bool = False
while True:

    # sample vbat ADC reading, but using weighted average calculator
    vbat_reading:int = vbat_adc.read_u16()
    vbat_reading_smoothed:float = vbat_wac.feed(float(vbat_reading))

    # convert ADC reading on battery to a voltage
    full:tuple[int, float] = (50710, 2.62) # full, when on same power source
    dead:tuple[int, float] = (38715, 1.98) # depleted, when on same power source
    PercentOfRange:float = (vbat_reading_smoothed - dead[0]) / (full[0] - dead[0])
    volts:float = dead[1] + (PercentOfRange * (full[1] - dead[1]))

    # scale upward to remove divider
    volts = volts / 0.32

    # if volts are below threshold, mark battery as dead
    if volts <= DEAD_BATTERY_VOLTAGE:

        print("Battery voltage of " + str(volts) + " detected, which is below the dead battery voltage of " + str(DEAD_BATTERY_VOLTAGE) + "! Proceeding to shut down...")
        
        # Dead battery pattern on neopixels
        print("Displaying dead battery indicator (first pixel is red)...")
        nm.fill((0, 0, 0))
        nm.set_pixel(0, (10, 0, 0)) # set first pixel as red
        nm.show()

        # break out of while loop (abort this whole program now that we are dead!)
        print("Bye bye!")
        break
        

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