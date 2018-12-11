const constants = require('../constants');

// TTL days, in milliseconds
const TTL_MS = 1000 * 60 * 60 * 24 * constants.EVENT_TTL_DAYS;

module.exports = function cleanupEvents(change, context) {
    // Grab the current value of what was written to the Realtime Database.
    const original = change.after.val();
    const now = (new Date()).getTime();

    const pendingOperations = [];

    Object.keys(original).forEach((unitId) => {
        const unit = original[unitId];

        if (!unit) {
            return;
        }

        Object.keys(unit).forEach((eventId) => {
            const event = unit[eventId];

            if (!event || !event.occurredAt) {
                return;
            }

            const occurredAtMs = event.occurredAt * 1000;

            if (now - occurredAtMs > TTL_MS) {
                console.log(`Deleting stale event: ${unitId}/${eventId}`);

                // This event is stale, and should be cleaned up
                pendingOperations.push(
                    change.after.ref.child(unitId).child(eventId).set(null)
                );
                // TODO: Delete corresponding image in Google Cloud Storage
            }
        });
    });

    return Promise.all(pendingOperations);
};
