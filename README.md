Ding Dong Ditch
===============

Ding Dong Ditch is a project to convert a traditional wired doorbell into a newfangled
"smart" doorbell, without changing the external appearance of the house.

Why?
----

Whenever someone rings my doorbell, a 16V AV circuit is connected, which powers an
electromagnet inside the doorbell chime. The chime prompts my dog to bark wildly, and
without fail, wakes my sleeping baby. This simply will not do.

Tools
-----

* Raspberry Pi (rev B) that I got for free at PyCon years ago.

* An ~~old~~ *traditional* wired doordell (powered by a 16V AC 10VA transformer).

* A [custom circuit](schematic) to hook up aforementioned power source to the Raspberry
  Pi's GPIO pins without frying the Pi (which accepts 3.3V DC).

* This Python app.

Approach
--------

1. Replace the chime with a custom circuit that can safely trigger a GPIO pin on a
   Raspberry Pi.

2. When the pin "pulls up," this fires off a request to Twilio.

3. Twilio calls a pre-determined set of numbers with a message that someone is at the 
   door.

Again, Why?
-----------

Sure, I could spend $300 on a fancy, Internet-of-things connected doorbell. But, I don't
want to do this for several reasons:

1. We already have a doorbell built into our front gate. It is literally part of the
   gate. It matches the upstairs neighbors' doorbell. It is simple and looks fine.
   I don't want to add a second doorbell just for our unit. That would be confusing,
   and might annoy the neighbors.

2. I already have a Raspberry Pi collecting dust. Even if I didn't, one can be had for
   ~$30.

3. $300 seems steep for a doorbell (especially since I already have one). I'd rather
   spend $300 on beer.

4. I like to tinker.

License
-------

Everything provided in this repository is free to use, and granted to the public domain.
Do whatever you want with it, subject to the Limitation of Liabilty, below. If you like
this, or find it useful, you might consider dropping me a note so I feel warm an fuzzy
inside. Or not. It's up to you.

Limitation of Liability
-----------------------

This software, and any accompaying schematics, diagrams and instructions (the "Project")
are provided "AS IS" with no warranty either expressed or implied. Further, the author
shall not be held liable for any outcome whatsoever as the result of your use of the
Project. To be crystal clear, if you try this at home, and it frys your Pi, burns down
your house, and leaves you disfigured for life, you agree that it was entirely your own
fault. **Use this Project at your own risk.**
