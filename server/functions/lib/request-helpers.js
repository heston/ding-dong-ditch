const url = require('url');
const { isArray } = require('lodash');

module.exports.getBaseUrl = function getBaseUrl(req) {
    return url.format({
        protocol: req.protocol,
        host: req.get('host')
    });
}

module.exports.getFrom = function getFrom(req) {
    let from = req.query.From;

    // If "From" is an array, use the first number
    if (isArray(from)) {
        from = from[0];
    }

    return from;
}
