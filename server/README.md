Ding Dong Ditch Server
======================

The Ding Dong Ditch server provides a voice interface for configuring various aspects
of the system. For example, it allows you to register or unregister your phone
number from receiving notifications when the doorbell is rung. It also allows
you to remotely trigger your gate strike (the thing that buzzes to open your gate).

The term "Server" is a bit of a misnomer. It is actually a collection of Firebase
Cloud Functions that interact with the Firebase Realtime Database. The Raspberry Pi
sets up a streaming connection to the database, and gets notified when data changes.

The server will run on the free tier ("Spark" in Google parlance) of Firebase.

Set up
------
This is adapted from the official [Firebase docs](https://firebase.google.com/docs/functions/get-started). Please refer to those docs for additional information.

1. Install the Firebase CLI as described in the [Firebase CLI Reference](https://firebase.google.com/docs/cli/  ). The Firebase CLI requires [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.org/), which you can install by following the instructions on [https://nodejs.org/](https://nodejs.org/). Installing Node.js also installs npm.

    The Firebase CLI requires Node.js version 6.3.1 or greater. Once you have Node.js and npm installed, install the Firebase CLI via npm:

    ```bash
    npm install -g firebase-tools
    ```

    This installs the globally available firebase command. To update to the latest version, rerun the same command.

    If the command fails, you may need to [change npm permissions](https://docs.npmjs.com/getting-started/fixing-npm-permissions).

2. Run `firebase login` to log in via the browser and authenticate the firebase tool.

3. Go to the Firebase project directory (e.g. `dingdongditch/server`).

4. Run `firebase init functions` to associate the server with a Firebase project in your account. You will probably want to select `[create a new project]`.

5. When you are promped with, `File functions/package.json already exists. Overwrite?`. Select `N` (No).

6. When you are prompted with, `File functions/index.js already exists. Overwrite?`. Select `N` (No).

7. When you are prompted with, `Do you want to install dependencies with npm now?`. Select `Y` (Yes).

8. Run this command to deploy the functions:

    ```bash
    $ firebase deploy --only functions
    ```

    After you deploy, the Firebase CLI outputs the URLs for the HTTP function endpoints. In your terminal, you should see output like the following:

    ```
    Project Console: https://console.firebase.google.com/project/YOUR-PROJECT-NAME/overview
    Function URL (doorbell): https://us-central1-YOUR-PROJECT-NAME.cloudfunctions.net/doorbell
    Function URL (greeting): https://us-central1-YOUR-PROJECT-NAME.cloudfunctions.net/greeting
    Function URL (mainMenu): https://us-central1-YOUR-PROJECT-NAME.cloudfunctions.net/mainMenu
    Function URL (handleAction): https://us-central1-YOUR-PROJECT-NAME.cloudfunctions.net/handleAction
    Function URL (unlock): https://us-central1-YOUR-PROJECT-NAME.cloudfunctions.net/unlock
    ```

9. Grab the URL of the first function (`doorbell`) and set it to the `DDD_FIREBASE_CLOUD_FUNCTION_NOTIFY_URL` key in your `env.sh` file.

10. You're done! Enjoy a frosty :beer: for your efforts.
