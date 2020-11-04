const TwimlResponse = require('./twiml-response');
const { times } = require('lodash');

module.exports = class Doorbell extends TwimlResponse {
    constructor(baseUrl, pin) {
        super(baseUrl);
        this.pin = pin;
    }

    getTwiml() {
        const resp = super.getTwiml();
        const gather = resp.gather({
            timeout: 30,
            numDigits: 1,
            method: 'GET',
            action: this.getUrl('unlock', {pin: this.pin}),
        });

        times(3, () => {
            gather.say(
                'Ding dong! ' +
                'This is your doorbell calling. Someone is at the door. ' +
                'Press any key to unlock the gate.'
            );
            gather.pause({length: 1});
        });

        return resp
    }
}
