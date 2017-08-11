import os
import requests
import xmltodict

from common.models import DomainInfo
from common.error_codes import check_error_code

__author__ = 'goran.vrbaski'


class ContactModel:
    def __init__(self, first_name: str, last_name: str, address: str, city: str, state: str, country: str, email: str, phone: str, zip: str):
        """
        Model for manipulating NameSilo contacts
        :param first_name: First Name
        :param last_name: Last Name
        :param address: Address
        :param city: City
        :param state: State
        :param country: Country
        :param email: Email address
        :param phone: Telephone number
        :param zip: ZIP Code
        """
        self.first_name = self.__correct_formating(first_name)
        self.last_name = self.__correct_formating(last_name)
        self.address = self.__correct_formating(address)
        self.city = self.__correct_formating(city)
        self.state = self.__correct_formating(state)
        self.country = self.__correct_formating(country)
        self.email = self.__correct_formating(email)
        self.phone = self.__correct_formating(phone)
        self.zip = self.__correct_formating(zip)

    @staticmethod
    def __correct_formating(data: str):
        """
        Replacing all whitespaces with %20 (NameSilo requirement)
        :param data:
        :return:
        """
        return data.replace(" ", "%20")


class NameSilo:
    def __init__(self, token: str, sandbox: bool=True):
        """

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
        return int(data['namesilo']['reply']['code']), data['namesilo']['reply']['detail']

    def _get_content_xml(self, url):
        api_request = requests.get(os.path.join(self.__base_url, url))
        if api_request.status_code != 200:
            raise Exception(
                f"API responded with status code: {api_request.status_code}"
            )

        content = xmltodict.parse(api_request.content.decode())
        return content

    def check_domain(self, domain_name: str):
        """
        Check if domain name is available
        :param domain_name:
        :return:
        """
        url_extend = f"checkRegisterAvailability?version=1&type=xml&" \
                     f"key={self._token}&domains={domain_name}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        if 'available' in parsed_content['namesilo']['reply'].keys():
            return True
        else:
            return False

    def get_domain_info(self, domain_name: str):
        """
        Returns information about specified domain
        :param domain_name:
        :return: DomainInfo model from common.models
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
        """
        url_extend = f"listDomains?version=1&type=xml&key={self._token}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return parsed_content['namesilo']['reply']['domains']['domain']

    def register_domain(self, domain_name: str, years: int=1, auto_renew: int=0, private: int=0):
        """
        Register domain name
        :param domain_name: name of domain
        :param years:
        :param auto_renew:
        :param private:
        :return:
        """
        url_extend = f"registerDomain?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}&years={years}&private={private}&" \
                     f"auto_renew={auto_renew}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return True

    def renew_domain(self, domain_name: str, years: int=1):
        """
        Renew domain name
        :param domain_name:
        :param years:
        :return:
        """
        url_extend = f"renewDomain?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}&years={years}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return True

    def get_prices(self):
        """
        Returns all supported tld prices
        :return:
        """
        url_extend = f"getPrices?version=1&type=xml&key={self._token}"
        parsed_content = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_content))
        return parsed_content['namesilo']['reply']

    def list_contacts(self):
        """
        Returns list of all contacts for current account
        :return:
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
        :param contact:
        :return:
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

    # TODO: need to finish update contact
    def update_contact(self, contact: ContactModel):
        url_extend = f"contactUpdate?version=1&type=xml&key={self._token}&contact_id=1440&fn=Goran&ln=Vrbaski&ad=123%20N.%201st%20Street&cy=Anywhere&st=AZ&zp=55555&ct=US&em=test@test.com&ph=4805555555"
        parsed_contect = self._process_data(url_extend)
        return True

    def add_account_funds(self, amount: float, payment_id: int):
        url_extend = f"addAccountFunds?version=1&type=xml&key={self._token}&" \
                     f"amount={amount}&payment_id={payment_id}"
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        amount = parsed_context['namesilo']['reply']['new_balance'].replace(",", "")
        return True, float(amount)

    def get_account_balance(self):
        url_extend = f"getAccountBalance?version=1&type=xml&key={self._token}"
        parsed_context = self._get_content_xml(url_extend)
        check_error_code(self._get_error_code(parsed_context))
        amount = parsed_context['namesilo']['reply']['balance'].replace(",", "")
        return float(amount)
