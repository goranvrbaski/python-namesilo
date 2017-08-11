__author__ = 'goran.vrbaski'


error_codes_to_messages = {
    101: "HTTPS not used",
    102: "No version specified",
    103: "Invalid API version",
    104: "No type specified",
    105: "Invalid API type",
    106: "No operation specified",
    107: "Invalid API operation",
    108: "Missing parameters for the specified operation",
    109: "No API key specified",
    110: "Invalid API key",
    111: "Invalid User",
    112: "API not available to Sub-Accounts",
    113: "This API account cannot be accessed from your IP",
    114: "Invalid Domain Syntax",
    115: "Central Registry Not Responding - try again later",
    116: "Invalid sandbox account",
    117: "The provided credit card profile either does not exist, or is not associated with your account",
    118: "The provided credit card profile has not been verified",
    119: "Insufficient account funds for requested transaction",
    120: "API key must be passed as a GET",
    200: "Domain is not active, or does not belong to this user",
    201: "Internal system error",
    210: "General error (details provided in response)",
    250: "Domain is already set to AutoRenew - No update made.",
    251: "Domain is already set not to AutoRenew - No update made.",
    252: "Domain is already Locked - No update made.",
    253: "Domain is already Unlocked - No update made.",
    254: "NameServer update cannot be made. (details provided in response)",
    255: "Domain is already Private - No update made.",
    256: "Domain is already Not Private - No update made.",
    261: "Domain processing error (details provided in response)",
    262: "This domain is already active within our system and therefore cannot be processed.",
    263: "Invalid number of years, or no years provided.",
    264: "Domain cannot be renewed for specified number of years (details provided in response)",
    265: "Domain cannot be transferred at this time (details provided in response)",
    266: "No domain transfer exists for this user for this domain",
    267: "Invalid domain name, or we do not support the provided extension/TLD.",
    280: "DNS modification error",
    300: "Successful API operation",
    301: "Successful registration, but not all provided hosts were valid resulting in our name servers being used",
    302: "Successful order, but there was an error with the contact information provided so your account default "
         "contact profile was used (you can configure your account to reject orders with invalid contact information "
         "via the Reseller Manager page in your account.)",
    400: "Existing API request is still processing - request will need to be re-submitted"
}


def check_error_code(error_code: tuple):
    if error_code[0] in [300, 301, 302]:
        return error_codes_to_messages[error_code[0]]
    elif error_code[0] in [210, 261, 264]:
        raise Exception(error_code[1])
    else:
        raise Exception(error_codes_to_messages[error_code[0]])
