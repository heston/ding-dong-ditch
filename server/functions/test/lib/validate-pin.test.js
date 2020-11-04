const mockOnce = jest.fn();
const mockRef = jest.fn(() => ({ once: mockOnce }));
const mockDatabase = jest.fn(() => ({ ref: mockRef }));

jest.mock('firebase-admin', () =>
    ({
        database: mockDatabase
    })
);

const admin = require('firebase-admin');
const validatePin = require('lib/validate-pin');

describe('validatePin', () => {
    let snapshot;

    beforeEach(() => {
        snapshot = {
            val: jest.fn()
        };

        mockOnce.mockImplementation(() => {
            return Promise.resolve(snapshot);
        });
    });

    test('rejects for missing pin', () => {
        return validatePin().catch((e) => {
            expect(e.message).toMatch('No pin provided');
        });
    });

    test('rejects for unknown pin', () => {
        snapshot.val.mockImplementation(() => null);
        return validatePin(1234).catch((e) => {
            expect(e.message).toMatch('Unknown pin');
        });
    });

    test('resolves for known pin', () => {
        snapshot.val.mockImplementation(() => 1);
        return validatePin(1234).then((value) => {
            expect(value).toEqual(1);
            return 1;
        });
    });
});
