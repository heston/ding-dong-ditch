const StrikeTriggered = require('../responses/strike-triggered');
const { setSettings } = require('../lib/settings');

module.exports = function triggerStrike(pin) {
    return setSettings(pin, 'strike', 1).then(() => {
        return StrikeTriggered;
    });
}
