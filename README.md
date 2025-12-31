# Python Namesilo Module

[![PyPiVersion Badge][PyPiVersion]](https://pypi.org/project/python-namesilo)
[![Read The Docs][ReadtheDocs]](https://python-namesilo.vrbaski.dev)

`python-namesilo` is a small Python wrapper around the official NameSilo API.
It focuses on a straightforward interface for the most common domain/account operations.

- Official API docs: https://www.namesilo.com/Support/API-Manager
- Documentation: https://python-namesilo.vrbaski.dev

This project supports Python `3.8` to `3.12`.


## Installation

```bash
pip install python-namesilo
```


## Authentication / configuration

You need an **API key** from your NameSilo account.

- **Sandbox** (default): `NameSilo(..., sandbox=True)`
- **Production**: `NameSilo(..., sandbox=False)`


## Quickstart

```python
import os

from namesilo.core import NameSilo

client = NameSilo(
    token=os.environ["NAMESILO_API_KEY"],
    sandbox=False,
)

domain = "example.com"
if client.check_domain(domain):
    client.register_domain(domain, years=1, private=1, auto_renew=0)
```


## Common usage

### List domains

```python
from namesilo.core import NameSilo

client = NameSilo(token="YOUR_API_KEY", sandbox=False)
print(client.list_domains())
```

### Domain info

```python
from namesilo.core import NameSilo

client = NameSilo(token="YOUR_API_KEY", sandbox=False)
info = client.get_domain_info("example.com")

print(info.status)
print(info.expires)
print(info.name_servers)
```

### Change nameservers

```python
from namesilo.core import NameSilo

client = NameSilo(token="YOUR_API_KEY", sandbox=False)
client.change_domain_nameservers(
    domain="example.com",
    primary_ns="ns1.example.net",
    secondary_ns="ns2.example.net",
)
```

### DNS records

```python
from namesilo.core import NameSilo

client = NameSilo(token="YOUR_API_KEY", sandbox=False)

records = client.list_dns_records("example.com")
print(records)

record_id = client.add_dns_record(
    domain_name="example.com",
    record_type="A",
    record_host="@",
    record_value="203.0.113.10",
    ttl=3600,
)

client.update_dns_record(
    domain_name="example.com",
    record_id=str(record_id),
    record_host="@",
    record_value="203.0.113.11",
    ttl=3600,
)
```

### Balance and pricing

```python
from namesilo.core import NameSilo

client = NameSilo(token="YOUR_API_KEY", sandbox=False)

print(client.get_account_balance())
print(client.get_prices())
```


## Error handling

The library raises specific exception classes from `namesilo.exceptions`.

```python
from namesilo.core import NameSilo
from namesilo.exceptions import (
    APIRequestError,
    DomainAlreadyLocked,
    InvalidAPIKey,
    InvalidDomainSyntax,
    IPForbidden,
)

client = NameSilo(token="YOUR_API_KEY", sandbox=False)

try:
    client.lock_domain("example.com")
except InvalidAPIKey as exc:
    print(f"Invalid API key: {exc}")
except IPForbidden as exc:
    print(f"IP forbidden: {exc}")
except InvalidDomainSyntax as exc:
    print(f"Invalid domain: {exc}")
except DomainAlreadyLocked as exc:
    print(f"Already locked: {exc}")
except APIRequestError as exc:
    print(f"Request error: {exc}")
```


## Functionality status

This table tracks the **NameSilo API operations** and their current support in this library.

| NameSilo API operation | Python method | Implemented |
| :-- | :-- | :--: |
| registerDomain | `NameSilo.register_domain` | Yes |
| renewDomain | `NameSilo.renew_domain` | Yes |
| checkRegisterAvailability | `NameSilo.check_domain` | Yes |
| listDomains | `NameSilo.list_domains` | Yes |
| getDomainInfo | `NameSilo.get_domain_info` | Yes |
| contactList | `NameSilo.list_contacts` | Yes |
| contactAdd | `NameSilo.add_contact` | Yes |
| contactUpdate | `NameSilo.update_contact` | Yes |
| contactDelete | `NameSilo.delete_contact` | Yes |
| getAccountBalance | `NameSilo.get_account_balance` | Yes |
| addAccountFunds | `NameSilo.add_account_funds` | Yes |
| getPrices | `NameSilo.get_prices` | Yes |
| changeNameServers | `NameSilo.change_domain_nameservers` | Yes |
| addPrivacy | `NameSilo.add_domain_privacy` | Yes |
| removePrivacy | `NameSilo.remove_domain_privacy` | Yes |
| addAutoRenewal | `NameSilo.auto_renew_domain` | Yes |
| removeAutoRenewal | `NameSilo.remove_auto_renew_domain` | Yes |
| domainLock | `NameSilo.lock_domain` | Yes |
| domainUnlock | `NameSilo.unlock_domain` | Yes |
| dnsListRecords | `NameSilo.list_dns_records` | Yes |
| dnsAddRecord | `NameSilo.add_dns_record` | Yes |
| dnsUpdateRecord | `NameSilo.update_dns_record` | Yes |


## Contributing

Issues and PRs are welcome.


[PyPiVersion]: https://img.shields.io/pypi/v/python-namesilo.svg?style=flat-square
[ReadtheDocs]: https://img.shields.io/readthedocs/python-namesilo.svg?style=flat-square
