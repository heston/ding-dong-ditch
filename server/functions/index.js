const admin = require('firebase-admin');
const functions = require('firebase-functions');
const greeting = require('./actions/greeting');
const mainMenu = require('./actions/main-menu');
const handleAction = require('./actions/handle-action');

admin.initializeApp(functions.config().firebase);

exports.greeting = functions.https.onRequest(greeting);
exports.mainMenu = functions.https.onRequest(mainMenu);
exports.handleAction = functions.https.onRequest(handleAction);
