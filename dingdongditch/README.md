Ding Dong Ditch Client
======================

The client runs on your Raspberry Pi. It handles interfacing with the exisitng hardware,
including the doorbell, mechanical chime, and door/gate stike, if present.

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
