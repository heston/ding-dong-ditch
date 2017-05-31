const admin = require('firebase-admin');

module.exports.getSettings = function getSettings(pin, optPath) {
    if (!pin) {
        return Promise.reject(new Error('No pin provided'));
    }

    const name = `settings/${pin}${optPath ? '/' + optPath : ''}`;
    return admin.database().ref(name).once('value');
}

module.exports.setSettings = function setSettings(pin, path, value) {
    if (!pin) {
        return Promise.reject(new Error('No pin provided'));
    }

    const name = `settings/${pin}${path ? '/' + path : ''}`;
    return admin.database().ref(name).set(value);
}
