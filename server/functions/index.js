const admin = require('firebase-admin');
const functions = require('firebase-functions');
const greeting = require('./actions/greeting');
const mainMenu = require('./actions/main-menu');
const handleAction = require('./actions/handle-action');
const unlock = require('./actions/unlock');
const doorbell = require('./actions/doorbell');

admin.initializeApp(functions.config().firebase);

exports.greeting = functions.https.onRequest(greeting);
exports.mainMenu = functions.https.onRequest(mainMenu);
exports.handleAction = functions.https.onRequest(handleAction);
exports.unlock = functions.https.onRequest(unlock);
exports.doorbell = functions.https.onRequest(doorbell);
