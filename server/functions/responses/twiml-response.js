const twilio = require('twilio');
const URLSearchParams = require('url-search-params');
const url = require('url');

module.exports = class TwimlResponse {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    getUrl(cloudFunctionName, params) {
        let qs;

        if (typeof params !== undefined) {
            const searchParams = new URLSearchParams(params);
            const encodedParams = searchParams.toString();
            qs = `?${encodedParams}`;
        } else {
            qs = '';
        }

        return url.resolve(this.baseUrl, `/${cloudFunctionName}${qs}`);
    }

    getTwiml() {
        return new twilio.twiml.VoiceResponse();
    }

    render() {
        const resp = this.getTwiml();
        return resp.toString();
    }
}
