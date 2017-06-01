const Doorbell = require('../responses/doorbell');
const { getBaseUrl } = require('../lib/request-helpers');

module.exports = function doorbell(req, res) {
    const pin = req.query.pin;

    res.status(200).type('xml');

    const resp = new Doorbell(
        getBaseUrl(req),
        pin
    );
    res.send(resp.render());
};
