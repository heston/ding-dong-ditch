const { getSettings, setSettings } = require('../lib/settings');

module.exports = function togglePhone(pin, from) {
    return getSettings(pin, `recipients/${from}`).then(snapshot => {
        const recipient = snapshot.val();
        if (recipient) {
            // Disable recipient
            return setSettings(pin, `recipients/${from}`, null);
        } else {
            // Enable recipient
            return setSettings(pin, `recipients/${from}`, 1);
        }
    });
}
