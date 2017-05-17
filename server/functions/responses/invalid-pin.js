const TwimlResponse = require('./twiml-response');

module.exports = class InvalidPin extends TwimlResponse {
    getTwiml() {
        const resp = super.getTwiml();

        resp.say('I\'m sorry, I don\'t recognize that pin. ');
        resp.redirect(this.getUrl('greeting'));

        return resp
    }
}
