import machine
import ssd1306
import time
import neopixel

# set up ADC
adc = machine.ADC(machine.Pin(26, machine.Pin.IN))

# set up OLED
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
print(i2c.scan())
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up neopixel
pixels = neopixel.NeopixelManager(neopixel.Neopixel(15, 0, 22, "GRB"))

def burst_sample(duration:float = 1.0, samples:int = 100) -> int:
    """Takes average of analog reading over short period of time."""
    delay:float = duration / samples
    total:int = 0
    for _ in range(samples):
        total = total + adc.read_u16()
        time.sleep(delay)
    return int(round(total / samples, 0))

battery_dead:bool = False
started_at = time.ticks_ms()
stopped_at = None
while True:

    # estimate the total current being drawn from the neopixels using the NeopixelManagers!
    current_ma:float = pixels.current
    
    # sample the raw ADC reading of the battery
    val:int = burst_sample()

    # "add back" ADC points to accomodate for the voltage sag due to the current consumption of the neopixels!
    adc_drop_per_ma:float = 4.7040504848760 # determined this through observations (see readme!)
    val = val + int(adc_drop_per_ma * current_ma) # add back!

    # based on the sample reading, try to calculate volts
    full:tuple[int, float] = (50710, 2.62) # full, when on same power source
    dead:tuple[int, float] = (38715, 1.98) # depleted, when on same power source
    PercentOfRange:float = (val - dead[0]) / (full[0] - dead[0])
    volts:float = dead[1] + (PercentOfRange * (full[1] - dead[1]))

    # but now scale upward to remove the divider
    volts_scaled:float = volts / 0.32
    print("Volts of battery pack: " + str(volts_scaled))


    # if the volts are below a certain amount, mark battery as dead
    if battery_dead == False:
        if volts_scaled <= 3.1:
            print("Marking battery as dead!")
            battery_dead = True
            stopped_at = time.ticks_ms()

    # handle battery alive/dead situation
    if battery_dead == False:
        print("Battery is not dead! Showing full brightness.")
        pixels.fill((255, 255, 255))
        pixels.show()

        # display
        oled.fill(0)
        oled.text(str(val), 0, 0)
        oled.text(str(round(volts, 2)) + "v ADC", 0, 12)
        oled.text(str(round(volts_scaled, 2)) + "v", 0, 24)
        oled.show()

    else:
        print("Battery is dead! Turning off.")
        pixels.fill((0, 0, 0))
        pixels.show()

        # seconds
        seconds_lasted:int = int((stopped_at - started_at) / 1000)

        # display
        oled.fill(0)
        oled.text(str(val), 0, 0)
        oled.text(str(round(volts, 2)) + "v ADC", 0, 12)
        oled.text(str(round(volts_scaled, 2)) + "v", 0, 24)
        oled.text(str(seconds_lasted) + " seconds", 0, 36)
        oled.show()

    # sleep
    time.sleep(1.0)
