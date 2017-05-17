const { get } = require('lodash');
const TwimlResponse = require('./twiml-response');

module.exports = class MainMenu extends TwimlResponse {
    constructor(baseUrl, settings, from, pin) {
        super(baseUrl);
        this.settings = settings;
        this.from = from;
        this.pin = pin
    }

    getMenuOptions() {
        return {
            bellEnabled: get(this.settings, 'chime', 0),
            fromEnabled: get(this.settings, ['recipients', this.from], 0) === 1
        };
    }

    getTwiml() {
        const resp = super.getTwiml();
        const menuOptions = this.getMenuOptions();
        resp.say('Doorbell main menu.');
        const gather = resp.gather({
            timeout: 30,
            numDigits: 1,
            method: 'GET',
            action: this.getUrl('handleAction', {pin: this.pin}),
        });

        if (menuOptions.fromEnabled) {
            gather.say(
                'To disable your phone number, press 1.'
            );
        } else {
            gather.say(
                'To enable your phone number, press 1.'
            );
        }

        gather.pause(1);

        if (menuOptions.bellEnabled) {
            gather.say(
                'To disable your doorbell chime, press 2.'
            );
        } else {
            gather.say(
                'To enable your doorbell chime, press 2.'
            );
        }

        return resp;
    }
}
