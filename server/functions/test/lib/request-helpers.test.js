const helpers = require('lib/request-helpers');

describe('getFrom', () => {
    test('empty value', () => {
        const req = {
            query: {}
        };
        const result = helpers.getFrom(req);

        expect(result).toBe(undefined);
    });

    test('single value', () => {
        const req = {
            query: {
                From: '+14155551000'
            }
        };
        const result = helpers.getFrom(req);

        expect(result).toBe('+14155551000');
    });

    test('multiple values', () => {
        const req = {
            query: {
                From: [
                    '+14155551000',
                    '+15105551000',
                ]
            }
        };
        const result = helpers.getFrom(req);

        expect(result).toBe('+14155551000');
    });
});


describe('getBaseUrl', () => {
    test('from request', () => {
        const req = {
            protocol: 'https',
            get: () => {
                return 'app.cloudfunction.io';
            }
        };
        const result = helpers.getBaseUrl(req);

        expect(result).toBe('https://app.cloudfunction.io');
    });
});
