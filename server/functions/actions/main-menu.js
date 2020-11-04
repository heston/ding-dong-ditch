const MainMenu = require('../responses/main-menu');
const InvalidPin = require('../responses/invalid-pin');
const { getBaseUrl, getFrom } = require('../lib/request-helpers');
const { getSettings } = require('../lib/settings');
const validatePin = require('../lib/validate-pin');

module.exports = function mainMenu(req, res) {
    // Get the pin from the request
    const pin = req.query.Digits;
    const from = getFrom(req);

    res.status(200).type('xml');

    console.log('mainMenu', req.query);

    return validatePin(pin).then(() => getSettings(pin)).then(
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
            return res;
        },
        (e) => {
            console.log('mainMenu.error', e);
            // Send error, since pin is missing
            const error = new InvalidPin(getBaseUrl(req));
            res.send(error.render());
            return res;
        }
    );
};
