const mockGreeting = jest.fn(() => ({
    render: () => '__result__'
}));
const mockGetBaseUrl = jest.fn(() => 'http://localhost');

jest.mock('responses/greeting', () => mockGreeting);
jest.mock('lib/request-helpers', () => ({ getBaseUrl: mockGetBaseUrl }));

const greeting = require('actions/greeting');

describe('greeting action', () => {
    test('renders twiml response', () => {
        const req = {};
        const mockType = jest.fn();
        const mockStatus = jest.fn(() => ({
            type: mockType
        }));
        const res = {
            status: mockStatus,
            send: jest.fn()
        };

        greeting(req, res);

        expect(mockStatus).toHaveBeenCalledWith(200);
        expect(mockType).toHaveBeenCalledWith('xml');
        expect(mockGreeting).toHaveBeenCalledWith('http://localhost');
        expect(res.send).toHaveBeenCalledWith('__result__');
    });
});
