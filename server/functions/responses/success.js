const TwimlResponse = require('./twiml-response');

module.exports = class Success extends TwimlResponse {
    constructor(baseUrl, pin, action) {
        super(baseUrl);
        this.pin = pin;
        this.action = action;
    }

    getTwiml() {
        const resp = super.getTwiml();

        resp.say('OK. Your preferences have been updated. ');
        resp.redirect(
            {method: 'GET'},
            this.getUrl(this.action, {Digits: this.pin})
        );

        return resp
    }
}
