
const RECIPIENT_TYPE = {
    PHONE: 'p',
    SMS: 's',
};
const PHONE_TYPE = 'PHONE';
const SMS_TYPE = 'SMS';
const PHONE_POSTFIX_DELIMITER = '::';

module.exports.PHONE_TYPE = PHONE_TYPE;
module.exports.SMS_TYPE = SMS_TYPE;

module.exports.parsePhoneNumber = function parsePhoneNumber(number) {
    const strNumber = String(number);
    const numberParts = strNumber.split(PHONE_POSTFIX_DELIMITER);
    return numberParts[0];
};

module.exports.unparsePhoneNumber = function unparsePhoneNumber(number, recipientType) {
    const recipientTypeValue = RECIPIENT_TYPE[recipientType];
    if (recipientTypeValue === undefined) {
        throw new Error(`Unknown recipient type: ${recipientType}`);
    }
    return `${number}${PHONE_POSTFIX_DELIMITER}${recipientTypeValue}`;
};
