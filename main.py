import os
import requests
import xmltodict

from common.models import DomainInfo
from common.error_codes import check_error_code

__author__ = 'goran.vrbaski'


class ContactModel:
    def __init__(self, **kwargs):
        """
        Model for manipulating NameSilo contacts

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
        self.first_name = self._correct_formating(kwargs.get('first_name'))
        self.last_name = self._correct_formating(kwargs.get('last_name'))
        self.address = self._correct_formating(kwargs.get('address'))
        self.city = self._correct_formating(kwargs.get('city'))
        self.state = self._correct_formating(kwargs.get('state'))
        self.country = self._correct_formating(kwargs.get('country'))
        self.email = self._correct_formating(kwargs.get('email'))
        self.phone = self._correct_formating(kwargs.get('phone'))
        self.zip = self._correct_formating(kwargs.get('zip'))

    @staticmethod
    def _correct_formating(data: str):
        """
        Replacing all whitespaces with %20 (NameSilo requirement)
        :param data:

        :return: string
        """
        return data.replace(" ", "%20")


class NameSilo:
    def __init__(self, token, sandbox: True):
        """
        Creating Namesilo object with given token

        :param token: access token from namesilo.com
        :param sandbox: true or false
        """
        self._token = token
        if sandbox:
            self.__base_url = "http://sandbox.namesilo.com/api/"
        else:
            self.__base_url = "https://www.namesilo.com/api/"

    def _process_data(self, url_extend):
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        return parsed_context

    @staticmethod
    def _get_error_code(data):
        return int(data['namesilo']['reply']['code']), \
               data['namesilo']['reply']['detail']

    def _get_content_xml(self, url):
        api_request = requests.get(os.path.join(self.__base_url, url))
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
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
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
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return DomainInfo(parsed_content)

    def list_domains(self):
        """
        List all domains registered with current account

        :return: list of registered domains
        :rtype: list
        """
        url_extend = f"listDomains?version=1&type=xml&key={self._token}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
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
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
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
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return True

    def get_prices(self):
        """
        Returns all prices for supported TLDs

        :return: Prices for supported TLDs
        :rtype: dict
        """
        url_extend = f"getPrices?version=1&type=xml&key={self._token}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return parsed_content['namesilo']['reply']

    def list_contacts(self):
        """
        Returns list of all contacts for current account

        :return: list of all contacts
        :rtype: list
        """
        contacts = []
        url_extend = f"contactList?version=1&type=xml&key={self._token}"
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        for contact in parsed_context['namesilo']['reply']['contact']:
            contacts.append(contact)
        return contacts

    def add_contact(self, contact: ContactModel):
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
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        return True

    def update_contact(self, contact_id, contact: ContactModel):
        """
        Update existing contact with new information

        :param str contact_id: contact id to change
        :param ContactModel contact: new contact information
        :return: status of action
        :rtype: bool
        """
        url_extend = f"contactUpdate?version=1&type=xml&key={self._token}&" \
                     f"contact_id={contact_id}&" \
                     f"fn={contact.first_name}%20{contact.last_name}&" \
                     f"ad={contact.address}&cy={contact.city}&" \
                     f"st={contact.state}&zp={contact.zip}&" \
                     f"ct={contact.country}&em={contact.email}&" \
                     f"ph={contact.phone}"

        return self._process_data(url_extend)

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
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        amount = parsed_context['namesilo']['reply']['new_balance']
        return True, float(amount.replace(",", ""))

    def get_account_balance(self):
        """
        Returns current account balance

        :return: current account balance
        :rtype: float
        """
        url_extend = f"getAccountBalance?version=1&type=xml&key={self._token}"
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        amount = parsed_context['namesilo']['reply']['balance']
        return float(amount.replace(",", ""))
