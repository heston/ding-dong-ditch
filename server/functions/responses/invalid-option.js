const TwimlResponse = require('./twiml-response');

module.exports = class InvalidOption extends TwimlResponse {
    constructor(baseUrl, from, pin) {
        super(baseUrl);
        this.from = from;
        this.pin = pin
    }

    getTwiml() {
        const resp = super.getTwiml();

        resp.say('I\'m sorry, I didn\'t get that. ');
        resp.redirect(this.getUrl('mainMenu', {Digits: this.pin, From: this.from}));

        return resp
    }
}
