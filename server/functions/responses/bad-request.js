const TwimlResponse = require('./twiml-response');

module.exports = class BadRequest extends TwimlResponse {
    getTwiml() {
        const resp = super.getTwiml();

        resp.say('I\'m sorry, something went wrong. Please call back to start over. ');
        resp.hangup();

        return resp
    }
}
