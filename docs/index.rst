python-namesilo
=============

``python-namesilo`` is a lightweight Python wrapper around the `NameSilo API <https://www.namesilo.com/Support/API-Manager>`_.
It provides a thin, pragmatic interface for common account and domain management tasks such as:
 
- Domain availability checks and registration
- Domain renewal and information lookup
- Nameserver updates
- WHOIS privacy management
- Domain lock/unlock
- Contact profile management
- Account balance and funding
- DNS record listing/creation/update
 
The primary entry point is :class:`namesilo.core.NameSilo`.
 
 
Installation
------------
 
Install from PyPI:
 
.. code-block:: bash
 
   pip install python-namesilo
 
 
Authentication and environment
------------------------------
 
You need an API key from your NameSilo account.
 
- Production API base URL is used when ``sandbox=False``.
- Sandbox API base URL is used when ``sandbox=True`` (default).
 
 
Quickstart
----------
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
 
   domain = "example.com"
   if client.check_domain(domain):
       client.register_domain(domain, years=1, private=1, auto_renew=0)
 
 
Common usage
------------
 
List domains
^^^^^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
   domains = client.list_domains()
   print(domains)
 
 
Get domain information
^^^^^^^^^^^^^^^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
   info = client.get_domain_info("example.com")
 
   print(info.status)
   print(info.expires)
   print(info.name_servers)
 
 
Update nameservers
^^^^^^^^^^^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
   client.change_domain_nameservers(
       "example.com",
       primary_ns="ns1.example.net",
       secondary_ns="ns2.example.net",
   )
 
 
WHOIS privacy
^^^^^^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
   client.add_domain_privacy("example.com")
   client.remove_domain_privacy("example.com")
 
 
Domain lock/unlock
^^^^^^^^^^^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
   client.lock_domain("example.com")
   client.unlock_domain("example.com")
 
 
Contacts
^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import ContactModel, NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
 
   contacts = client.list_contacts()
   for c in contacts:
       print(c)
 
   new_contact = ContactModel(
       first_name="Jane",
       last_name="Doe",
       address="1 Main Street",
       city="Belgrade",
       state="RS",
       country="RS",
       zip="11000",
       email="jane@example.com",
       phone="+381.111111",
   )
 
   client.add_contact(new_contact)
 
 
DNS records
^^^^^^^^^^
 
.. code-block:: python
 
   from namesilo.core import NameSilo
 
   client = NameSilo(token="YOUR_API_KEY", sandbox=False)
 
   records = client.list_dns_records("example.com")
   print(records)
 
   record_id = client.add_dns_record(
       "example.com",
       record_type="A",
       record_host="@",
       record_value="203.0.113.10",
       ttl=3600,
   )
 
   client.update_dns_record(
       "example.com",
       record_id=str(record_id),
       record_host="@",
       record_value="203.0.113.11",
       ttl=3600,
   )
 
 
Error handling
--------------

API errors are mapped to custom exceptions defined in :mod:`namesilo.exceptions`.

.. code-block:: python

   from namesilo.core import NameSilo
   from namesilo.exceptions import (
       APIRequestError,
       DomainAlreadyLocked,
       InsufficientFunds,
       InvalidAPIKey,
       InvalidDomainSyntax,
       IPForbidden,
   )

   client = NameSilo(token="YOUR_API_KEY", sandbox=False)

   try:
       balance = client.get_account_balance()
   except InvalidAPIKey as exc:
       print(f"Invalid API key: {exc}")
   except IPForbidden as exc:
       print(f"Your IP is not allowed to access the API: {exc}")
   except APIRequestError as exc:
       print(f"Request error: {exc}")

   try:
       client.lock_domain("example.com")
   except DomainAlreadyLocked as exc:
       print(f"Domain already locked: {exc}")
   except InvalidDomainSyntax as exc:
       print(f"Invalid domain syntax: {exc}")


Available exception types
-------------------------

The following exception classes are defined in :mod:`namesilo.exceptions`:

- :class:`namesilo.exceptions.HTTPSNotUsed`
- :class:`namesilo.exceptions.NoAPIVersionSpecified`
- :class:`namesilo.exceptions.InvalidAPIVersion`
- :class:`namesilo.exceptions.NoTypeSpecified`
- :class:`namesilo.exceptions.InvalidAPIType`
- :class:`namesilo.exceptions.NoOperationSpecified`
- :class:`namesilo.exceptions.InvalidAPIOperation`
- :class:`namesilo.exceptions.MissingParameters`
- :class:`namesilo.exceptions.NoApiKeySpecified`
- :class:`namesilo.exceptions.InvalidAPIKey`
- :class:`namesilo.exceptions.InvalidUser`
- :class:`namesilo.exceptions.APINotAvailableSubs`
- :class:`namesilo.exceptions.IPForbidden`
- :class:`namesilo.exceptions.InvalidDomainSyntax`
- :class:`namesilo.exceptions.CreditCardProfileDoesntExists`
- :class:`namesilo.exceptions.CreditCardNotVerified`
- :class:`namesilo.exceptions.InsufficientFunds`
- :class:`namesilo.exceptions.APIKeyPass`
- :class:`namesilo.exceptions.DomainNotActive`
- :class:`namesilo.exceptions.InternalSystemError`
- :class:`namesilo.exceptions.GeneralError`
- :class:`namesilo.exceptions.DomainAlreadyAutoRenew`
- :class:`namesilo.exceptions.DomainAlreadyNotAutoRenew`
- :class:`namesilo.exceptions.DomainAlreadyLocked`
- :class:`namesilo.exceptions.DomainAlreadyUnlocked`
- :class:`namesilo.exceptions.NameServerUpdateError`
- :class:`namesilo.exceptions.DomainAlreadyPrivate`
- :class:`namesilo.exceptions.DomainAlreadyNotPrivate`
- :class:`namesilo.exceptions.DomainProcessingError`
- :class:`namesilo.exceptions.DomainAlreadyActiveInSystem`
- :class:`namesilo.exceptions.InvalidNumberOfYears`
- :class:`namesilo.exceptions.CentralRegistryNotResponding`
- :class:`namesilo.exceptions.InvalidSandboxAccount`
- :class:`namesilo.exceptions.DomainNotRenewed`
- :class:`namesilo.exceptions.DomainNotTransferred`
- :class:`namesilo.exceptions.NoDomainTransfer`
- :class:`namesilo.exceptions.InvalidDomainNameOrExtension`
- :class:`namesilo.exceptions.DNSModificationError`
- :class:`namesilo.exceptions.APIRequestError`


API reference
-------------
 
.. autoclass:: namesilo.core.NameSilo
   :members:
 
.. autoclass:: namesilo.core.ContactModel
   :members:
 
.. autoclass:: namesilo.common.DomainInfo
   :members:
 
 
Indices and tables
------------------
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
