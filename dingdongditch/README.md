Ding Dong Ditch Client
======================

The client runs on your Raspberry Pi. It handles interfacing with the exisiting hardware,
including the doorbell, mechanical chime, and door/gate strike, if present.

Prerequisites
--------------
* This has only been tested on Python 3.6. At the time of writing, this was [a pain to install](http://bohdan-danishevsky.blogspot.com/2017/01/building-python-360-on-raspberry-pi-3.html) on Raspbian.

* This has only been tested on a Raspberry Pi B.

* This has only been tested on the OS `Raspbian GNU/Linux 8 (jessie)`.

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

    Edit this file to specify the settings you need. Look at [`system_settings.py`](https://github.com/heston/ding-dong-ditch/blob/master/dingdongditch/system_settings.py) for more detailed descriptions.

4. Set up your Firebase credentials. This allows the client to communicate with the server.

    1. Ensure your [server is set up](../server/README.md).

    2. Log in to the [Firebase console](https://console.firebase.google.com) and select your project.

    3. Click settings (the gear menu next to the "Overview" tab).

    4. Copy your "Project ID" and set it to the `DDD_FIREBASE_APP_NAME` variable in `env.sh`.

    5. Copy the "Web API Key" and set it to the `DDD_FIREBASE_API_KEY` variable in `env.sh`.

    6. Click on "Service Accounts" in the tab bar.

    7. Click "Generate New Private Key" and save the file somewhere.

    8. Copy the key file to your Raspberry Pi (scp, rsync, whatever). The default location is `/home/pi/.firebasekey`.

    9. Ensure the `DDD_FIREBASE_KEY_PATH` variable in `env.sh` points to the file.

5. Run the client:

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

If you decide it's not for you, uninstalling is equally easy:

```bash
make uninstall
```
