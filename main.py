import os
import requests
import xmltodict
from xml.dom import minidom
from common.models import DomainInfo
from common.error_codes import check_error_code

__author__ = 'goran.vrbaski'


class NameSilo:
    def __init__(self, token: str, sandbox: bool=True):
        """

        :param token: access token from namesilo.com
        :param sandbox: true or false
        """
        self.__token = token
        if sandbox:
            self.__base_url = "http://sandbox.namesilo.com/api/"
        else:
            self.__base_url = "https://www.namesilo.com/api/"

    def __process_request(self, content):
        return minidom.parseString(content)

    def __get_error_code(self, data):
        return int(data['namesilo']['reply']['code'])

    def __get_content_xml(self, url):
        api_request = requests.get(os.path.join(self.__base_url, url))
        if api_request.status_code != 200:
            raise Exception("API responded with status code: %s" % api_request.status_code)

        content = xmltodict.parse(api_request.content.decode())
        return content

    def check_domain(self, domain_name: str):
        """
        Check if domain name is available
        :param domain_name:
        :return:
        """
        url_extend = "checkRegisterAvailability?version=1&type=xml&key=%s&domains=%s" % (self.__token, domain_name)
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
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
        url_extend = "getDomainInfo?version=1&type=xml&key=%s&domain=%s" % (self.__token, domain_name)
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
        return DomainInfo(parsed_content)

    def list_domains(self):
        """
        List all domains registered with current account
        :return: list of registered domains
        """
        domain_list = []
        url_extend = "listDomains?version=1&type=xml&key=%s" % self.__token
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
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
        url_extend = "registerDomain?version=1&type=xml&key=%s&domain=%s&years=%s&private=%s&auto_renew=%s" % \
                     (self.__token, domain_name, years, private, auto_renew)
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
        return True

    def renew_domain(self, domain_name: str, years: int=1):
        """
        Renew domain name
        :param domain_name:
        :param years:
        :return:
        """
        url_extend = "renewDomain?version=1&type=xml&key=%s&domain=%s&years=%s" % (self.__token, domain_name, years)
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
        return True

    def get_prices(self):
        """
        Returns all supported tld prices
        :return:
        """
        url_extend = "getPrices?version=1&type=xml&key=%s" % self.__token
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
        return parsed_content['namesilo']['reply']
