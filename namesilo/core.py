import os
import requests
import xmltodict

from namesilo.common import DomainInfo
from namesilo.exceptions import exception_codes

__author__ = 'goran.vrbaski'


class ContactModel:
    def __init__(self, **kwargs):
        """
        Model for manipulating NameSilo contacts

        :param str contact_id: Contact ID
        :param str first_name: First Name
        :param str last_name: Last Name
        :param str address: Address
        :param str city: City
        :param str state: State
        :param str country: Country
        :param str email: Email address
        :param str phone: Telephone number
        :param str zip: ZIP Code
        """
        self.contact_id = self._correct_formating(kwargs.get('contact_id'))
        self.first_name = self._correct_formating(kwargs.get('first_name'))
        self.last_name = self._correct_formating(kwargs.get('last_name'))
        self.address = self._correct_formating(kwargs.get('address'))
        self.city = self._correct_formating(kwargs.get('city'))
        self.state = self._correct_formating(kwargs.get('state'))
        self.country = self._correct_formating(kwargs.get('country'))
        self.email = self._correct_formating(kwargs.get('email'))
        self.phone = self._correct_formating(kwargs.get('phone'))
        self.zip = self._correct_formating(kwargs.get('zip'))

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.contact_id}"

    @staticmethod
    def convert_contact_model(reply):
        """
        Convert standard Namesilo reply to ContactModel

        :param reply: Namesilo Contact response
        :return: Populated ContactModel from Namesilo
        :rtype: ContactModel
        """
        return ContactModel(
            contact_id=reply['contact_id'],
            first_name=reply['first_name'],
            last_name=reply['last_name'],
            address=reply['address'],
            city=reply['city'],
            state=reply['state'],
            country=reply['country'],
            zip=reply['zip'],
            email=reply['email'],
            phone=reply['phone']
        )

    @staticmethod
    def _correct_formating(data: str):
        """
        Replacing all whitespaces with %20 (NameSilo requirement)
        :param data:

        :return: string
        """
        return data.replace(" ", "%20")


class NameSilo:
    def __init__(self, token, sandbox: bool=True):
        """
        Creating Namesilo object with given token

        :param token: access token from namesilo.com
        :param sandbox: true or false
        """
        self._token = token
        if sandbox:
            self._base_url = "http://sandbox.namesilo.com/api/"
        else:
            self._base_url = "https://www.namesilo.com/api/"

    def _process_data(self, url_extend):
        parsed_context = self._get_content_xml(url_extend)
        self.check_error_code(self._get_error_code(parsed_context))
        return parsed_context

    @staticmethod
    def _get_error_code(data):
        return int(data['namesilo']['reply']['code']), \
               data['namesilo']['reply']['detail']

    @staticmethod
    def check_error_code(error_code: tuple):
        if error_code[0] in [300, 301, 302]:
            return exception_codes[error_code[0]]
        else:
            raise exception_codes[error_code[0]](error_code[1])

    def _get_content_xml(self, url):
        api_request = requests.get(os.path.join(self._base_url, url))
        if api_request.status_code != 200:
            raise Exception(
                f"API responded with status code: {api_request.status_code}"
            )

        content = xmltodict.parse(api_request.content.decode())
        return content

    def check_domain(self, domain_name):
        """
        Check if domain name is available

        :param str domain_name: Domain name for checking
        :return: Availability of domain
        :rtype: bool
        """
        url_extend = f"checkRegisterAvailability?version=1&type=xml&" \
                     f"key={self._token}&domains={domain_name}"
        parsed_content = self._process_data(url_extend)
        if 'available' in parsed_content['namesilo']['reply'].keys():
            return True

        return False

    def get_domain_info(self, domain_name):
        """
        Returns information about specified domain

        :param str domain_name: name of domain
        :return: domain information
        :rtype: DomainInfo
        """
        url_extend = f"getDomainInfo?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        parsed_content = self._process_data(url_extend)
        return DomainInfo(parsed_content)

    def change_domain_nameservers(self, domain, primary_ns, secondary_ns):
        """
        Change name server for specified domain

        :param str domain: Domain name
        :param str primary_ns: Primary name Server
        :param str secondary_ns: Secondary name server
        :return: Status of action
        :rtype: bool
        """
        url_extend = f"changeNameServers?version=1&" \
                     f"type=xml&key={self._token}&domain={domain}&" \
                     f"ns1={primary_ns}&ns2={secondary_ns}"
        self._process_data(url_extend)
        return True

    def list_domains(self):
        """
        List all domains registered with current account

        :return: list of registered domains
        :rtype: list
        """
        url_extend = f"listDomains?version=1&type=xml&key={self._token}"
        parsed_content = self._process_data(url_extend)
        return parsed_content['namesilo']['reply']['domains']['domain']

    def register_domain(self, domain_name, years=1, auto_renew=0, private=0):
        """
        Register a new domain name

        :param str domain_name: name of domain
        :param int years: how long to register domain
        :param int auto_renew: turn on or off auto-renewal option
        :param int private: hide your private information (WHOIS)
        :return: status of domain registration
        :rtype: bool
        """
        url_extend = f"registerDomain?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}&years={years}&private={private}&" \
                     f"auto_renew={auto_renew}"
        self._process_data(url_extend)
        return True

    def renew_domain(self, domain_name, years=1):
        """
        Renew domain name

        :param str domain_name: domain name for renewal
        :param int years:
        :return: status of renewal
        :rtype: bool
        """
        url_extend = f"renewDomain?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}&years={years}"
        self._process_data(url_extend)
        return True

    def lock_domain(self, domain_name: str):
        """

        :param str domain_name:
        :return:
        """
        url_extend = f"domainLock?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        self._process_data(url_extend)
        return True

    def unlock_domain(self, domain_name: str):
        """

        :param str domain_name:
        :return:
        """
        url_extend = f"domainUnlock?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        self._process_data(url_extend)
        return True

    def auto_renew_domain(self, domain_name: str):
        """
        Set auto-renew to specific domain

        :param str domain_name: Domain name
        :return: Status of action
        :rtype: bool
        """
        url_extend = f"addAutoRenewal?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        self._process_data(url_extend)
        return True

    def remove_auto_renew_domain(self, domain_name: str):
        """
        Remove auto-renew to specific domain

        :param str domain_name: Domain name
        :return: Status of action
        :rtype: bool
        """
        url_extend = f"removeAutoRenewal?version=1&type=xml&" \
                     f"key={self._token}&domain={domain_name}"
        self._process_data(url_extend)
        return True

    def get_prices(self):
        """
        Returns all prices for supported TLDs

        :return: Prices for supported TLDs
        :rtype: dict
        """
        url_extend = f"getPrices?version=1&type=xml&key={self._token}"
        parsed_content = self._process_data(url_extend)
        return parsed_content['namesilo']['reply']

    def list_contacts(self):
        """
        Returns list of all contacts for current account

        :return: list of all contacts
        :rtype: list
        """
        contacts = []
        url_extend = f"contactList?version=1&type=xml&key={self._token}"
        parsed_context = self._process_data(url_extend)
        reply = parsed_context['namesilo']['reply']['contact']

        if isinstance(reply, list):
            for contact in reply:
                contacts.append(ContactModel.convert_contact_model(contact))

        elif isinstance(reply, dict):
            contacts.append(ContactModel.convert_contact_model(reply))

        return contacts

    def add_contact(self, contact):
        """
        Adding new contact for current account

        :param ContactModel contact:
        :return: Status for adding contact
        :rtype: bool
        """
        url_extend = f"contactAdd?version=1&type=xml&key={self._token}&" \
                     f"fn={contact.first_name}&ln={contact.last_name}&" \
                     f"ad={contact.address}&cy={contact.city}&" \
                     f"st={contact.state}&zp={contact.zip}&" \
                     f"ct={contact.country}&em={contact.email}&" \
                     f"ph={contact.phone}"
        self._process_data(url_extend)
        return True

    def update_contact(self, contact: ContactModel):
        """
        Update existing contact with new information

        :param ContactModel contact: new contact information
        :return: status of action
        :rtype: bool
        """
        url_extend = f"contactUpdate?version=1&type=xml&key={self._token}&" \
                     f"contact_id={contact.contact_id}&" \
                     f"fn={contact.first_name}%20{contact.last_name}&" \
                     f"ad={contact.address}&cy={contact.city}&" \
                     f"st={contact.state}&zp={contact.zip}&" \
                     f"ct={contact.country}&em={contact.email}&" \
                     f"ph={contact.phone}"

        self._process_data(url_extend)
        return True

    def delete_contact(self, contact_id):
        """
        Delete contact from NameSilo account

        :param int contact_id: Contact ID
        :return:
        :rtype: None
        """
        url_extend = f"contactDelete?version=1&type=xml&key={self._token}&" \
                     f"contact_id={contact_id}"
        parsed_context = self._process_data(url_extend)
        return parsed_context

    def add_account_funds(self, amount, payment_id):
        """
        Adding funds to Namesilo account

        :param float amount: amount to add
        :param int payment_id: ID of payment (credit card)
        :return: Status and amount after adding funds, example: (True, 150.00)
        :rtype: tuple
        """
        url_extend = f"addAccountFunds?version=1&type=xml&key={self._token}&" \
                     f"amount={amount}&payment_id={payment_id}"
        parsed_context = self._process_data(url_extend)
        amount = parsed_context['namesilo']['reply']['new_balance']
        return True, float(amount.replace(",", ""))

    def get_account_balance(self):
        """
        Returns current account balance

        :return: current account balance
        :rtype: float
        """
        url_extend = f"getAccountBalance?version=1&type=xml&key={self._token}"
        parsed_context = self._process_data(url_extend)
        amount = parsed_context['namesilo']['reply']['balance']
        return float(amount.replace(",", ""))

    def add_domain_privacy(self, domain_name):
        """
        Adds privacy to specified domain name

        :param str domain_name: Domain name for adding privacy
        :return: Status of action
        :rtype: bool
        """
        url_extend = f"addPrivacy?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        self._process_data(url_extend)
        return True

    def remove_domain_privacy(self, domain_name):
        """
        Removes privacy for specified domain name

        :param str domain_name: Domain name for removing privacy
        :return: Status of action
        :rtype: bool
        """
        url_extend = f"removePrivacy?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        self._process_data(url_extend)
        return True
