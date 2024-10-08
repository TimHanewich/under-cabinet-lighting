import machine
import colors

class PotReader:
    
    def __init__(self, gp:int):
        self.adc = machine.ADC(machine.Pin(gp, machine.Pin.IN))

    def read(self) -> float:
        """Returns the reading on the potentiometer (knob) as a percentage between 0.0 and 1.0."""
        percentage:float = self.adc.read_u16() / 65535

        # scale percentage (account for dead zone on both ends)
        p_min:float = 0.01
        p_max:float = 0.99
        percentage = (percentage - p_min) / (p_max - p_min)
        percentage = max(min(percentage, 1.0), 0.0) # ensure within 1.0 and 0.0

        return 1.0 - percentage # flip it so it is the correct direction (turning to right is up, turning to left is down)
    
def warmth(percent:float) -> tuple[int, int, int]:
    """Returns an RGB color on a spectrum of color from cold to warm. 0.0 is warm, 1.0 is cold."""
    warm:tuple[int, int, int] = (255, 131, 0)
    cold:tuple[int, int, int] = (195, 209, 255)
    return colors.gradient_point(warm, cold, percent)