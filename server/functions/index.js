const admin = require('firebase-admin');
const cleanupEvents = require('./db/cleanup-events');
const constants = require('./constants');
const doorbell = require('./actions/doorbell');
const functions = require('firebase-functions');
const greeting = require('./actions/greeting');
const handleAction = require('./actions/handle-action');
const mainMenu = require('./actions/main-menu');
const unlock = require('./actions/unlock');
const nocache = require('./lib/no-cache');

admin.initializeApp(functions.config().firebase);

exports.greeting = functions.https.onRequest(greeting);
exports.mainMenu = functions.https.onRequest(mainMenu);
exports.handleAction = functions.https.onRequest(nocache(handleAction));
exports.unlock = functions.https.onRequest(nocache(unlock));
exports.doorbell = functions.https.onRequest(doorbell);

exports.cleanupEvents = functions.database
    .ref(constants.EVENTS_PATH)
    .onWrite(cleanupEvents);
