const TwimlResponse = require('./twiml-response');

module.exports = class StrikeTriggered extends TwimlResponse {
    constructor(baseUrl, pin, action) {
        super(baseUrl);
        this.pin = pin;
        this.action = action;
    }

    getTwiml() {
        const resp = super.getTwiml();

        resp.say('Your gate will open momentarily.');
        resp.pause({length: 1});

        if (this.pin && this.action) {
            resp.redirect(
                {method: 'GET'},
                this.getUrl(this.action, {Digits: this.pin})
            );
        } else {
            resp.hangup();
        }

        return resp
    }
}
