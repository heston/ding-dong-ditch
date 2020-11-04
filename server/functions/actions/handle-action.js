const BadRequest = require('../responses/bad-request');
const InvalidOption = require('../responses/invalid-option');
const Success = require('../responses/success');
const { getBaseUrl, getFrom } = require('../lib/request-helpers');
const togglePhone = require('../activities/toggle-phone');
const toggleSms = require('../activities/toggle-sms');
const toggleChime = require('../activities/toggle-chime');
const triggerStrike = require('../activities/trigger-strike');

/**
 * Mapping of phone keys to activities.
 *
 * @type {Object.<number, Function>}
 */
const actions = {
    1: togglePhone,
    2: toggleSms,
    3: toggleChime,
    4: triggerStrike,
};

module.exports = function handleAction(req, res) {
    // Get the pin from the request
    const pin = req.query.pin;
    const from = getFrom(req);

    console.log('handleAction', req.query);

    const option = req.query.Digits;
    const action = actions[option];

    if (!pin) {
        res.send((new BadRequest()).render());
        return res;
    }

    if (!action) {
        const resp = new InvalidOption(
            getBaseUrl(req),
            from,
            pin
        );
        res.send(resp.render());
        return res;
    }

    return action(pin, from).then(
        (ResponseClass) => {
            let resp;
            if (ResponseClass) {
                resp = new ResponseClass(
                    getBaseUrl(req),
                    pin,
                    'mainMenu'
                );
            } else {
                resp = new Success(
                    getBaseUrl(req),
                    pin,
                    'mainMenu'
                );
            }
            console.log('success', resp.render());
            res.send(resp.render());
            return res;
        }, () => {
            res.send((new BadRequest()).render())
            return res;
        });
};
