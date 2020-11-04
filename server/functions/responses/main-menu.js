const { get } = require('lodash');
const TwimlResponse = require('./twiml-response');
const { PHONE_TYPE, SMS_TYPE, unparsePhoneNumber } = require('../lib/phone-number');

module.exports = class MainMenu extends TwimlResponse {
    constructor(baseUrl, settings, from, pin) {
        super(baseUrl);
        this.settings = settings;
        this.from = from;
        this.pin = pin
    }

    getMenuOptions() {
        return {
            bellEnabled: get(
                this.settings,
                'chime',
                0),
            phoneEnabled: get(
                this.settings,
                ['recipients', unparsePhoneNumber(this.from, PHONE_TYPE)],
                0),
            smsEnabled: get(
                this.settings,
                ['recipients', unparsePhoneNumber(this.from, SMS_TYPE)],
                0)
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

        if (menuOptions.phoneEnabled) {
            gather.say(
                'To disable your phone number, press 1.'
            );
        } else {
            gather.say(
                'To enable your phone number, press 1.'
            );
        }

        gather.pause({length: 1});

        if (menuOptions.smsEnabled) {
            gather.say(
                'To stop receiving text messages, press 2.'
            );
        } else {
            gather.say(
                'To start receiving text messages, press 2.'
            );
        }

        gather.pause({length: 1});

        if (menuOptions.bellEnabled) {
            gather.say(
                'To disable your doorbell chime, press 3.'
            );
        } else {
            gather.say(
                'To enable your doorbell chime, press 3.'
            );
        }

        gather.pause({length: 1});

        gather.say(
            'To open the front gate, press 4.'
        );

        return resp;
    }
}
