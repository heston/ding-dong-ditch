const mockDoorbell = jest.fn(() => ({
    render: () => '__result__'
}));
const mockGetBaseUrl = jest.fn(() => 'http://localhost');

jest.mock('responses/doorbell', () => mockDoorbell);
jest.mock('lib/request-helpers', () => ({ getBaseUrl: mockGetBaseUrl }));

const doorbell = require('actions/doorbell');

describe('doorbell action', () => {
    test('renders twiml response', () => {
        const req = {
            query: {
                pin: 1234
            }
        };
        const mockType = jest.fn();
        const mockStatus = jest.fn(() => ({
            type: mockType
        }));
        const res = {
            status: mockStatus,
            send: jest.fn()
        };

        doorbell(req, res);

        expect(mockStatus).toHaveBeenCalledWith(200);
        expect(mockType).toHaveBeenCalledWith('xml');
        expect(mockDoorbell).toHaveBeenCalledWith(
            'http://localhost',
            1234
        );
        expect(res.send).toHaveBeenCalledWith('__result__');
    });
});
