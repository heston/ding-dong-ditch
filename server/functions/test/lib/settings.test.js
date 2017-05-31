const mockOnce = jest.fn();
const mockSet = jest.fn();
const mockRef = jest.fn(() => ({
    once: mockOnce,
    set: mockSet,
}));
const mockDatabase = jest.fn(() => ({ ref: mockRef }));

jest.mock('firebase-admin', () =>
    ({
        database: mockDatabase
    })
);

const admin = require('firebase-admin');
const settings = require('lib/settings');

describe('getSettings', () => {
    test('rejects for missing pin', () => {
        return settings.getSettings().catch((e) => {
            expect(e.message).toMatch('No pin provided');
        });
    });

    test('with no optPath', () => {
        settings.getSettings(1234);
        expect(mockDatabase).toHaveBeenCalled();
        expect(mockRef).toHaveBeenCalledWith('settings/1234');
        expect(mockOnce).toHaveBeenCalledWith('value');
    });

    test('with optPath', () => {
        settings.getSettings(1234, 'chime');
        expect(mockDatabase).toHaveBeenCalled();
        expect(mockRef).toHaveBeenCalledWith('settings/1234/chime');
        expect(mockOnce).toHaveBeenCalledWith('value');
    });
});


describe('setSettings', () => {
    test('rejects for missing pin', () => {
        return settings.setSettings().catch((e) => {
            expect(e.message).toMatch('No pin provided');
        });
    });

    test('with no path and no value', () => {
        settings.setSettings(1234);
        expect(mockDatabase).toHaveBeenCalled();
        expect(mockRef).toHaveBeenCalledWith('settings/1234');
        expect(mockSet).toHaveBeenCalledWith(undefined);
    });

    test('with a path and no value', () => {
        settings.setSettings(1234, 'chime');
        expect(mockDatabase).toHaveBeenCalled();
        expect(mockRef).toHaveBeenCalledWith('settings/1234/chime');
        expect(mockSet).toHaveBeenCalledWith(undefined);
    });

    test('with no path and a value', () => {
        settings.setSettings(1234, null, 1);
        expect(mockDatabase).toHaveBeenCalled();
        expect(mockRef).toHaveBeenCalledWith('settings/1234');
        expect(mockSet).toHaveBeenCalledWith(1);
    });

    test('with a path and a value', () => {
        settings.setSettings(1234, 'chime', 1);
        expect(mockDatabase).toHaveBeenCalled();
        expect(mockRef).toHaveBeenCalledWith('settings/1234/chime');
        expect(mockSet).toHaveBeenCalledWith(1);
    });
});
