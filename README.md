Ding Dong Ditch
===============

[![Build Status](https://travis-ci.org/heston/ding-dong-ditch.svg?branch=master)](https://travis-ci.org/heston/ding-dong-ditch)

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

* An ~~old~~ *traditional* wired doorbell (powered by a 16V AC 10VA transformer).

* A [custom circuit](schematic) to hook up aforementioned power source to the Raspberry
  Pi's GPIO pins without frying the Pi (which accepts 3.3V DC).

* This Python app.

Approach
--------

1. Replace the chime with a [custom circuit](schematic) that can safely trigger a GPIO 
pin on a Raspberry Pi.

2. When the pin "pulls up," this fires off a request to Twilio.

3. Twilio calls a pre-determined set of phone numbers.


Installation
------------
1. Clone this repo on your Raspberry Pi somewhere. For the purposes of this guide,
   we'll assume it's `/home/pi/ding-dong-ditch`.

2. Change into the working directory:

   ```bash
   cd /home/pi/ding-dong-ditch
   ```

3. Setup the python virtual environment:

   ```bash
   make setup
   ```

4. Create your settings file:

    ```bash
    cp env.sh.example env.sh
    ```

    Edit this file to specify the settings you need. Look at [`settings.py`](https://github.com/heston/ding-dong-ditch/blob/master/dingdongditch/settings.py)
    for a list of the available settings. The settings defined in the example are the
    minimum needed to run the program.

4. Run the program:

   ```bash
   make run
   ```

   To exit, type `ctrl-c`.


Running on Startup
------------------

To have this program run upon startup of your Raspberry Pi, you'll need to install
a `systemd` service. This is pretty easy:

```bash
make install
```

*Note:* If you cloned this repo into a directory other than `/home/pi/ding-dong-ditch`,
you'll need to update the [`WorkingDirectory` key in `dingdongditch.service`](https://github.com/heston/ding-dong-ditch/blob/master/dingdongditch.service#L7)
to point to the right location *before* running `make install`.

If you decide this is not for you, uninstalling is equally easy:

```bash
make uninstall
```

Again, Why?
-----------

Sure, I could spend $200 on a fancy, Internet-of-things
[connected doorbell](https://ring.com/). But, I don't really need that:

1. We already have a doorbell built into our front gate. It matches the upstairs
  neighbors' doorbell, it's simple, and it looks fine.

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
