const admin = require('firebase-admin');
const { setSettings } = require('../lib/settings');
const { UNIT_CONFIG_PATH } = require('../constants');

module.exports = function resetStrike() {
    const units = admin.database().ref(UNIT_CONFIG_PATH).once('value');
    const pendingOperations = [];

    Object.keys(units).forEach((unitId) => {
        pendingOperations.push(
            setSettings(unitId, 'strike', 0)
        );
    });


    return Promise.all(pendingOperations);
};
