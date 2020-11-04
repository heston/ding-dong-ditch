const BadRequest = require('../responses/bad-request');
const triggerStrike = require('../activities/trigger-strike');
const validatePin = require('../lib/validate-pin');

module.exports = function unlock(req, res) {
    // Get the pin from the request
    const pin = req.query.pin;

    console.log('unlock', req.query);

    if (!pin) {
        res.send((new BadRequest()).render())
        return res;
    }

    return validatePin(pin).then(() => {
        console.log('unlock triggered');
        return triggerStrike(pin);
     }).then((ResponseClass) => {
            res.send((new ResponseClass()).render());
            return res;
    }, () => {
        res.send((new BadRequest()).render());
        return res;
    });
};
