const {Storage} = require('@google-cloud/storage');
const constants = require('../constants');

// TTL days, in milliseconds
const TTL_MS = 1000 * 60 * 60 * 24 * constants.EVENT_TTL_DAYS;

module.exports = function cleanupEvents(change, context) {
    // Grab the current value of what was written to the Realtime Database.
    const original = change.after.val();
    const now = (new Date()).getTime();

    const pendingOperations = [];
    const storage = new Storage();

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
                const eventPath = `${constants.EVENTS_PATH}/${unitId}/${eventId}`;
                console.log(`Deleting stale event: ${eventPath}`);

                // This event is stale, and should be cleaned up
                pendingOperations.push(
                    change.after.ref
                        .child(unitId)
                        .child(eventId)
                        .set(null)
                );

                const imagePath = `${eventPath}.jpg`;
                console.log(`Deleting stale image: ${imagePath}`);
                // Delete corresponding image in Google Cloud Storage
                pendingOperations.push(
                    storage
                        .bucket(constants.BUCKET_NAME)
                        .file(imagePath)
                        .delete()
                        .then((result) => {
                            return result;
                        }, (err) => {
                            // Ignore failures
                            return true;
                        })
                );
            }
        });
    });

    return Promise.all(pendingOperations);
};
