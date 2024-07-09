## Specifications
- Target length: 18 inches long (1.5 ft)
- On the [150/LEDs per strand (30 pixels/meter)](https://a.co/d/074xPUYj), that is 15 pixels.
- On the [300/LEDs per strand (60 pixels/meter)](https://a.co/d/06SNFuth), that is 30 pixels.

## Design
The design will include the following:
- Battery Pack w/ two 18650 batteries, in a series
- Voltage divider on perfboard
- LM2596 Buck Converter (5V)
- Raspberry Pi Pico
- A 1.5ft strand (15 pixels) of the [150 LEDs/16.4 ft](https://a.co/d/0i7U9awN) density
- Controls
    - **Master power on/off switch**
        - Based on my motorcycle strobe design, a cut with a radius of 21mm will hold it securely
    - **Button** for changing pattern/color (see [this article](https://www.hackster.io/Ramji_Patel/raspberry-pi-pico-and-button-321059) on how to do this)
        - Specifying `Pin.PULL_UP` when creating the `machine.Pin` instance seems to be important. For example: `button = Pin(22, Pin.IN, Pin.PULL_UP)`
    - **Auxilary Potentiometer** potentiometer that can be used as decided (i.e. controlling brightness, color temperature and other things)
        - a 7.5mm hole allows the potentiometer to fit through perfectly.
        - You can easily use plyers to pull off that metal bit that prevents it from being flush against.