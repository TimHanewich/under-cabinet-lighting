import colors
import neopixel
import machine
import time


def warmth(percent:float) -> tuple[int, int, int]:
    warm:tuple[int, int, int] = (255, 131, 0)
    cold:tuple[int, int, int] = (195, 209, 255)
    return colors.gradient_point(warm, cold, percent)

pixels = neopixel.NeopixelManager(neopixel.Neopixel(11, 0, 22, "GRB"))
adc = machine.ADC(machine.Pin(26))

while True:
    val = adc.read_u16()
    color:tuple[int, int, int] = warmth(val / 65535)
    pixels.fill(color)
    pixels.show()
    time.sleep(0.25)