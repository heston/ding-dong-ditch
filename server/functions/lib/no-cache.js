module.exports = function nocache(handler) {

    return function innerHandler(req, res) {
        res.set({
            'Cache-Control': 'no-store',
        });

        return handler(req, res);
    };
};
