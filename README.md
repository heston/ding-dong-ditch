Ding Dong Ditch
===============

[![Build Status](https://travis-ci.org/heston/ding-dong-ditch.svg?branch=master)](https://travis-ci.org/heston/ding-dong-ditch)

Ding Dong Ditch is a project to convert a traditional wired doorbell into a newfangled
"smart" doorbell, without changing the external appearance of the house.

Why?
----

Whenever someone rings my doorbell, a 16V AV circuit is connected, which powers a
solenoid that strikes a metal bar to produce a loud "DING DONG" inside my home. The chime prompts my dog to bark wildly, and wakes my sleeping baby. This simply will not do.

Tools
-----

* Raspberry Pi (rev B) that I got for free at PyCon years ago.

* An ~~old~~ *traditional* wired doorbell (powered by a 16V AC 10VA transformer).

* A [custom circuit](schematic) to hook up aforementioned power source to the Raspberry
  Pi's GPIO pins without frying the Pi (which accepts 3.3V DC).

* [This Python app](tree/master/dingdongditch), running on the Pi.

* [This Node JS app](tree/master/server), to power a voice-activated UI.

Approach
--------

1. Replace the chime with a [custom circuit](schematic) that can safely trigger a GPIO 
pin on a Raspberry Pi.

2. When the pin "pulls up," this fires off a request to Twilio.

3. Twilio calls a user-defined set of phone numbers.

Installation
------------

There are two parts to getting Ding Dong Ditch running.

1. [Set up the client app](blob/master/dingdongditch/README.md) on your Raspberry Pi.

2. [Set up the server app](blob/master/server/README.md) with Google Firebase.

Again, Why?
-----------

Sure, I could spend $200 on a fancy, Internet-of-things
[connected doorbell](https://ring.com/). But, I don't really need that:

1. We already have a doorbell built into our front gate. It matches the rest of the
  building, it's simple, and it looks fine.

2. I have a Raspberry Pi collecting dust. Even if I didn't, one can be had for ~$30.

3. $200 seems steep for a doorbell. I'd rather spend $200 on beer.

4. I like to tinker.

License
-------

Everything provided in this repository is free to use, and granted to the public domain.
Do whatever you want with it, subject to the Limitation of Liabilty, below. If you like
this, or find it useful, you might consider dropping me a note so I feel warm and fuzzy
inside. Or not. It's up to you.

Limitation of Liability
-----------------------

This software, and any accompaying schematics, diagrams and instructions (the "Project")
are provided "AS IS" with no warranty either expressed or implied. Further, the author
shall not be held liable for any outcome whatsoever as the result of your use of the
Project. To be crystal clear, if you try this at home, and it frys your Pi, burns down
your house, or leaves you disfigured for life, you agree that it was entirely your own
fault. **Use this Project at your own risk.**
