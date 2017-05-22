const { getSettings, setSettings } = require('../lib/settings');

module.exports = function toggleChime(pin) {
    return getSettings(pin, 'chime').then(snapshot => {
        const chime = snapshot.val();
        if (chime === 1) {
            // Disable chime
            return setSettings(pin, 'chime', 0);
        } else {
            // Enable chime
            return setSettings(pin, 'chime', 1);
        }
    });
}
