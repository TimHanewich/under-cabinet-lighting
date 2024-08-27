# Under Cabinet Lighting
A very simple under-cabinet lighting system.

## Components
The design includes the following:
- Battery Pack w/ two 18650 batteries, in a series
- Voltage divider on perfboard
- LM2596 Buck Converter (set to step down to 5V)
- Raspberry Pi Pico
- A 1.5ft strand (30 pixels) of the [300 LEDs/16.4 ft](https://a.co/d/06SNFuth) density
- Controls
    - **Master power on/off switch**
    - **Tactile Button** for changing pattern/color
    - **Auxilary Potentiometer** potentiometer that can be used as decided (i.e. controlling brightness, color temperature and other things). You can easily use plyers to pull off that metal bit that prevents it from being flush against.

## Wiring
![wiring](https://i.imgur.com/RFXitxp.png)

The wiring diagram above can also be opened in [draw.io](https://draw.io) with the [schematic file](./schematic.drawio) provided in this repo.

## Assembly
I've provided the designs for the 3D-printed parts via Thingiverse [here](https://www.thingiverse.com/thing:6745264). It is basically just a box with a top and bottom piece, the bottom piece containing holes to mount the physical controls in.

I used a small tactile push button, soldered to a perf board, as the button. I then used small M2 screws to mount this perf board to the small openings in the `bottom.stl` model (I trust you will see where that is).

## Specifications
- Target length: 18 inches long (1.5 ft)
- On the [150/LEDs per strand (30 pixels/meter)](https://a.co/d/074xPUYj), that is 15 pixels.
- On the [300/LEDs per strand (60 pixels/meter)](https://a.co/d/06SNFuth), that is 30 pixels.

## Helpful Resources
- [This artile](https://www.hackster.io/Ramji_Patel/raspberry-pi-pico-and-button-321059) describes how a tactile push button can be set up.
