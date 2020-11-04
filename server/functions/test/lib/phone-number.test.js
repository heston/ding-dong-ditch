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

const {
    PHONE_TYPE,
    parsePhoneNumber,
    unparsePhoneNumber
} = require('lib/phone-number');

describe('parsePhoneNumber', () => {
    test('returns legacy number', () => {
        const number = '4155551234';
        const result = parsePhoneNumber(number);
        expect(result).toMatch(number);
    });

    test('returns post-fixed number', () => {
        const numberKey = '4155551234::1';
        const result = parsePhoneNumber(numberKey);
        expect(result).toMatch('4155551234');
    });
});

describe('unparsePhoneNumber', () => {
    test('throws on missing type', () => {
        expect(() => {
            unparsePhoneNumber('4155551234');
        }).toThrow('Unknown recipient type: undefined');
    });

    test('throws on invalid type', () => {
        expect(() => {
            unparsePhoneNumber('4155551234', 'x');
        }).toThrow('Unknown recipient type: x');
    });

    test('returns key', () => {
        const result = unparsePhoneNumber('4155551234', PHONE_TYPE);
        expect(result).toMatch('4155551234::p');
    });
});
