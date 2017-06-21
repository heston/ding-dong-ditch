const TwimlResponse = require('./twiml-response');
const { times } = require('lodash');
const { DOORBELL_AUDIO_URL } = require('../constants');

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

        times(5, () => {
            gather.play(DOORBELL_AUDIO_URL);
            gather.say(
                'This is your doorbell calling. Someone is at the door. ' +
                'Press any key to unlock the gate.'
            );
            gather.pause({length: 1});
        });

        return resp
    }
}
