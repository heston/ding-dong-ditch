const admin = require('firebase-admin');
const MainMenu = require('../responses/main-menu');
const InvalidPin = require('../responses/invalid-pin');
const { getBaseUrl, getFrom } = require('../lib/request-helpers');
const { getSettings } = require('../lib/settings');

function validatePin(pin) {
    if (!pin) {
        return Promise.reject(new Error('No pin provided'));
    }

    const name = `systemSettings/units/${pin}`;
    return admin.database().ref(name).once('value').then(snapshot => {
        const value = snapshot.val();
        console.log('validatePin', name, value);
        return value === 1 ? 1 : Promise.reject(new Error('Unknown pin'));
    });
}

module.exports = function mainMenu(req, res) {
    // Get the pin from the request
    const pin = req.query.Digits;
    const from = getFrom(req);

    res.status(200).type('xml');

    console.log('mainMenu', req.query);

    validatePin(pin).then(() => getSettings(pin)).then(
        (snapshot) => {
            const settings = snapshot.val();
            const menu = new MainMenu(
                getBaseUrl(req),
                settings,
                from,
                pin
            );
            console.log('menu', menu.render());
            res.send(menu.render());
        },
        (e) => {
            console.log('mainMenu.error', e);
            // Send error, since pin is missing
            const error = new InvalidPin(getBaseUrl(req));
            res.send(error.render());
        }
    );
};
