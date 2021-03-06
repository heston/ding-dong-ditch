const { getSettings, setSettings } = require('../lib/settings');
const { PHONE_TYPE, unparsePhoneNumber } = require('../lib/phone-number');

module.exports = function togglePhone(pin, from) {
    const phoneKey = unparsePhoneNumber(from, PHONE_TYPE);
    return getSettings(pin, `recipients/${phoneKey}`).then(snapshot => {
        const recipient = snapshot.val();
        if (recipient) {
            // Disable recipient
            return setSettings(pin, `recipients/${phoneKey}`, null);
        } else {
            // Enable recipient
            return setSettings(pin, `recipients/${phoneKey}`, 1);
        }
    });
}
