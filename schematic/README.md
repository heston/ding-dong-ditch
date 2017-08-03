Hardware Interface
==================

Traditional wired doorbells are interesting analog circuits. Interfacing one to a digital
microprocessor requires several steps.

How A Wired Doorbell Works
--------------------------

There are a few types of wired doorbell setups, but in general, they all have the
following components:

1. Low-voltage transformer (12-24VAC).
2. Button (either lighted, or not).
3. Chime. This is made up of a solenoid, a spring, and two sounding elements
   (tubes, plates, bells, etc.).

The simplest case involves an unlighted button. When the button is pressed, the circuit
is completed, activating the solenoid. The pin in the solenoid strikes one of the
sounding elements, making a "DING" sound. When the button is released, the circuit is
broken, and the solenoid is no longer powered. The spring pushes the pin in the opposite
direction, striking the second sounding element, making a "DONG" sound. The pin then
returns to the neutral position.

If the button is lighted, this gets a little more complex. In this case, the circuit is
always on. The light in the button acts as a resistor, limiting the current through the
circuit. Although current is always flowing through the solenoid, it is too low to
activate it. When the button is pressed, the resistor is bypassed, allowing a much larger
current to flow. This then activates the solenoid, as in the case above.

The schematic provided will work for either a lighted or unlighted button. In either
case, components will need to be selected for the voltage of the system.

Most doorbells have voltages in the range of 12-24VAC. The best way to find out is with a
multimeter. If you know where your doorbell transformer is, the voltage may be stamped on
the side.
