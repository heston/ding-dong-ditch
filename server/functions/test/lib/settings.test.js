const adminMock = jest.mock('firebase-admin', () => {
    return {
        database: jest.fn();
    }
});
const settings = require('lib/settings');

describe('getSettings', () => {
    test('rejects for missing pin', () => {
        settings.getSettings().catch((e) => {
            expect(e.message).toMatch('No pin provided');
        });
    });

    test('with no optPath', () => {
        settings.getSettings(1234);
        expect(adminMock.database).toHaveBeenCalled();
        // TODO: test ref() call
    });

    test('with optPath', () => {
        settings.getSettings(1234, 'chime');
        expect(adminMock.database).toHaveBeenCalled();
        // TODO: test ref() call
    });
});


describe('setSettings', () => {
    // TODO
});
