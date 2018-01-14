__author__ = 'goran.vrbaski'


class NameSilo(Exception):
    """Base NameSilo exception"""
    pass


class HTTPSNotUsed(NameSilo):
    """Request made without https"""
    pass


class InvalidAPIVersion(NameSilo):
    """Invalid API version while making a request"""
    pass


class NoTypeSpecified(NameSilo):
    """"""
    pass


class InvalidAPIType(NameSilo):
    """"""
    pass


class NoOperationSpecified(NameSilo):
    """"""
    pass


class InvalidAPIOperation(NameSilo):
    """"""
    pass


class MissingParameters(NameSilo):
    """"""
    pass


class NoApiKeySpecified(NameSilo):
    """"""
    pass


class InvalidAPIKey(NameSilo):
    """"""
    pass


class InvalidUser(NameSilo):
    """"""
    pass


class APINotAvailableSubs(NameSilo):
    pass


class IPForbidden(NameSilo):
    pass


class InvalidDomainSyntax(NameSilo):
    pass


class CreditCardProfileDoesntExists(NameSilo):
    pass


class CreditCardNotVerified(NameSilo):
    pass


class InsufficientFunds(NameSilo):
    pass


class APIKeyPass(NameSilo):
    pass


class DomainNotActive(NameSilo):
    pass


class InternalSystemError(NameSilo):
    pass


class GeneralError(NameSilo):
    pass


class DomainAlreadyAutoRenew(NameSilo):
    pass


class DomainAlreadyNotAutoRenew(NameSilo):
    pass


class DomainAlreadyLocked(NameSilo):
    pass


class DomainAlreadyUnlocked(NameSilo):
    pass


class NameServerUpdateError(NameSilo):
    pass


class DomainAlreadyPrivate(NameSilo):
    pass


class DomainAlreadyNotPrivate(NameSilo):
    pass


class DomainProcessingError(NameSilo):
    pass


class DomainAlreadyActiveInSystem(NameSilo):
    pass


class InvalidNumberOfYears(NameSilo):
    pass


class CentralRegistryNotResponding(NameSilo):
    pass


class InvalidSandboxAccount(NameSilo):
    pass


class NoAPIVersionSpecified(NameSilo):
    pass


class DomainNotRenewed(NameSilo):
    pass


class DomainNotTransferred(NameSilo):
    pass


class NoDomainTransfer(NameSilo):
    pass


class InvalidDomainNameOrExtension(NameSilo):
    pass


class DNSModificationError(NameSilo):
    pass


class APIRequestError(NameSilo):
    pass


exception_codes = {
    101: HTTPSNotUsed,
    102: NoAPIVersionSpecified,
    103: InvalidAPIVersion,
    104: NoTypeSpecified,
    105: InvalidAPIKey,
    106: NoOperationSpecified,
    107: InvalidAPIOperation,
    108: MissingParameters,
    109: NoApiKeySpecified,
    110: InvalidAPIKey,
    111: InvalidUser,
    112: APINotAvailableSubs,
    113: IPForbidden,
    114: InvalidDomainSyntax,
    115: CentralRegistryNotResponding,
    116: InvalidSandboxAccount,
    117: CreditCardProfileDoesntExists,
    118: CreditCardNotVerified,
    119: InsufficientFunds,
    120: APIKeyPass,
    200: DomainNotActive,
    201: InternalSystemError,
    210: GeneralError,
    250: DomainAlreadyAutoRenew,
    251: DomainAlreadyNotAutoRenew,
    252: DomainAlreadyLocked,
    253: DomainAlreadyUnlocked,
    254: NameServerUpdateError,
    255: DomainAlreadyPrivate,
    256: DomainAlreadyNotPrivate,
    261: DomainProcessingError,
    262: DomainAlreadyActiveInSystem,
    263: InvalidNumberOfYears,
    264: DomainNotRenewed,
    265: DomainNotTransferred,
    266: NoDomainTransfer,
    267: InvalidDomainNameOrExtension,
    280: DNSModificationError,
    300: "Successful API operation",
    301: "Successful registration, but not all provided hosts were valid resulting in our name servers being used",
    302: "Successful order, but there was an error with the contact information provided so your account default "
         "contact profile was used (you can configure your account to reject orders with invalid contact information "
         "via the Reseller Manager page in your account.)",
    400: APIRequestError
}
