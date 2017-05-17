const BadRequest = require('../responses/bad-request');
const Success = require('../responses/success');
const { getBaseUrl, getFrom } = require('../lib/request-helpers');
const { getSettings, setSettings } = require('../lib/settings');

function togglePhone(pin, from) {
    return getSettings(pin, `recipients/${from}`).then(snapshot => {
        const recipient = snapshot.val();
        if (recipient) {
            // Disable recipient
            return setSettings(pin, `recipients/${from}`, null);
        } else {
            // Enable recipient
            return setSettings(pin, `recipients/${from}`, 1);
        }
    });
}

function toggleChime(pin) {
    return getSettings(pin, 'chime').then(snapshot => {
        const chime = snapshot.val();
        if (chime === 1) {
            // Disable chime
            return setSettings(pin, 'chime', 0);
        } else {
            // Enable chime
            return setSettings(pin, 'chime', 1);
        }
    });
}

module.exports = function handleAction(req, res) {
    // Get the pin from the request
    const pin = req.query.pin;
    const from = getFrom(req);

    console.log('handleAction', req.query);

    const actions = {
        1: togglePhone,
        2: toggleChime
    };

    const option = req.query.Digits;
    const action = actions[option];

    if (!action || !pin) {
        res.send((new BadRequest()).render())
        return;
    }

    action(pin, from).then(
        () => {
            const success = new Success(
                getBaseUrl(req),
                pin,
                'mainMenu'
            );
            console.log('success', success.render());
            res.send(success.render());
        }, () => {
            res.send((new BadRequest()).render())
        });
};
