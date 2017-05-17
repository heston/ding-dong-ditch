const admin = require('firebase-admin');

module.exports.getSettings = function getSettings(pin, optPath) {
    if (!pin) {
        return Promise.reject(new Error('No pin provided'));
    }

    const name = `settings/${pin}${optPath ? '/' + optPath : ''}`;
    console.log('getSettings', name);
    return admin.database().ref(name).once('value');
}

module.exports.setSettings = function setSettings(pin, path, value) {
    const name = `settings/${pin}/${path}`;
    console.log('setSettings', name, value);
    return admin.database().ref(name).set(value);
}
