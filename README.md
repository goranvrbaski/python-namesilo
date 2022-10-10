# Python Namesilo Module
[![PyPiVersion Badge][PyPiVersion]](https://pypi.org/project/python-namesilo)
[![Read The Docs][ReadtheDocs]](https://python-namesilo.readthedocs.io)
[![DonateMe][PaypalBadge]](https://paypal.me/goranvrbaski)

This code is written in Python, and the following versions are supported: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`.

 If you want to contribute to this
project feel free to contact me at any time. If you're using this module and 
you like it, consider [buying me a beer.](https://paypal.me/goranvrbaski) :beer:

### Installation

```bash
pip install python-namesilo
```

### Usage
```python
from namesilo.core import NameSilo

client = NameSilo(token="your-token", sandbox=False)
domain_available = client.check_domain("domain-to-register.com")

if domain_available:
    print("Domain is available!")
    client.register_domain("domain-to-register", private=1) # use whois privacy
```

### Functionality Status

| Functionality | Description | Implemented  |
| :-------------: |:-------------:| :-----:|
| registerDomain| Register a new domain name | Yes |
| registerDomainDrop| Register a new domain name using drop-catching | No |
| renewDomain| Renew a domain name | Yes |
| transferDomain| Transfer a domain name into your NameSilo account | No |
| checkTransferStatus| Check the status of a domain transfer | No |
| checkRegisterAvailability| Determine if up to 200 domains can be registered at this time | Yes |
| checkTransferAvailability| Determine if up to 200 domains can be transferred into your account at this time | No |
| listDomains| A list of all active domains within your account | Yes |
| getDomainInfo| Get essential information on a domain within your account | Yes |
| contactList| View all contact profiles in your account | Yes |
| contactAdd| Add a contact profile to your account | Yes |
| contactUpdate| Update a contact profile in account | Yes |
| contactDelete| Delete a contact profile in account | Yes |
| contactDomainAssociate| Associate contact profiles with a domain | No |
| dnsListRecords| View all DNS records associated with your domain | No |
| dnsAddRecord| Add a new DNS resource record | No |
| dnsUpdateRecord| Update an existing DNS resource record | No |
| dnsDeleteRecord| Delete an existing DNS resource record | No |
| changeNameServers| Change the NameServers for up to 200 domains | Yes |
| portfolioList| List the active portfolios within your account | No |
| portfolioAdd| Add a portfolio to your account | No |
| portfolioDelete| Delete a portfolio from your account | No |
| portfolioDomainAssociate| Add up to 200 domains to a portfolio | No |
| listRegisteredNameServers| List the Registered NameServers associated with one of your domains | No |
| addRegisteredNameServer| Add a Registered NameServer for one of your domains | No |
| modifyRegisteredNameServer| Modify a Registered NameServer | No |
| deleteRegisteredNameServer| Delete a Registered NameServer | No |
| addPrivacy| Add WHOIS Privacy to a domain | Yes |
| removePrivacy| Remove WHOIS Privacy from a domain | Yes |
| addAutoRenewal| Set your domain to be auto-renewed | No |
| removeAutoRenewal| Remove the auto-renewal setting from your domain | No |
| retrieveAuthCode| Have the EPP authorization code for the domain emailed to the administrative contact | No |
| domainForward| Forward your domain | No |
| domainForwardSubDomain| Forward a sub-domain | No |
| domainForwardSubDomainDelete| Delete a sub-domain forward | No |
| domainLock| Lock your domain | Yes |
| domainUnlock| Unlock your domain | Yes |
| listEmailForwards| List all email forwards for your domain | No |
| configureEmailForward| Add or modify an email forward for your domain | No |
| deleteEmailForward| Delete an email forward for your domain | No |
| emailVerification| Verify a Registrant email address | No |


[BuildStatus]: https://img.shields.io/travis/goranvrbaski/python-namesilo/master.svg?style=flat-square
[CodeCov]: https://img.shields.io/codecov/c/github/goranvrbaski/python-namesilo/master.svg?style=flat-square
[PyPiVersion]: https://img.shields.io/pypi/v/python-namesilo.svg?style=flat-square
[PaypalBadge]: https://img.shields.io/badge/Donate-PayPal-green.svg?style=flat-square
[ReadtheDocs]: https://img.shields.io/readthedocs/python-namesilo.svg?style=flat-square
