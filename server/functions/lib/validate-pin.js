const admin = require('firebase-admin');

module.exports = function validatePin(pin) {
    if (!pin) {
        return Promise.reject(new Error('No pin provided'));
    }

    const name = `systemSettings/units/${pin}`;
    return admin.database().ref(name).once('value').then(snapshot => {
        const value = snapshot.val();
        return value === 1 ? 1 : Promise.reject(new Error('Unknown pin'));
    });
}
