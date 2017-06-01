const Greeting = require('../responses/greeting');
const { getBaseUrl } = require('../lib/request-helpers');

module.exports = function greeting(req, res) {
    res.status(200).type('xml');
    const greeting = new Greeting(getBaseUrl(req));
    res.send(greeting.render());
};
