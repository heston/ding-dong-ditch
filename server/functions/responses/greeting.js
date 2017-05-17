const TwimlResponse = require('./twiml-response');

module.exports = class Greeting extends TwimlResponse {
    getTwiml() {
        const message = 'Ding dong. Please enter your pin, followed by the pound key.';
        const resp = super.getTwiml();

        const gather = resp.gather({
            action: this.getUrl('mainMenu'),
            method: 'GET',
            timeout: 20
        });
        gather.say(message);
        gather.pause({length: 3});
        gather.say(message);

        return resp;
    }
}
