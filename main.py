import requests
import os
from xml.dom import minidom
from models import DomainInfo
import xmltodict

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

    def __get_content(self, url):
        return self.__process_request(requests.get(os.path.join(self.__base_url, url)).content.decode())

    def __get_content_xml(self, url):
        return xmltodict.parse(requests.get(os.path.join(self.__base_url, url)).content.decode())

    def check_domains(self, domain_names):
        """

        :param domain_names:
        :return:
        """
        available_domains = []
        url_extend = "checkRegisterAvailability?version=1&type=xml&key=%s&domains=%s" % (self.__token, domain_names)
        data = self.__get_content(url_extend)
        get_availabe_domains = data.getElementsByTagName("available")
        for domain in get_availabe_domains[0].childNodes:
            available_domains.append(domain.childNodes[0].data)

        return available_domains

    def get_domain_info(self, domain_name):
        url_extend = "getDomainInfo?version=1&type=xml&key=%s&domain=%s" % (self.__token, domain_name)
        content = self.__get_content_xml(url_extend)
        return DomainInfo(content)

    def list_domains(self):
        """
        :return: list of registered domains
        """
        domain_list = []
        url_extend = "listDomains?version=1&type=xml&key=%s" % self.__token
        parsed_content = self.__get_content(url_extend)
        for domain in parsed_content.getElementsByTagName("domain"):
            domain_list.append(domain.childNodes[0].data)

        return domain_list

    def register_domain(self, domain_name, years=1, auto_renew=0, private=0):
        """

        :param domain_name: name of domain
        :param years:
        :param auto_renew:
        :param private:
        :return:
        """
        url_extend = "registerDomain?version=1&type=xml&key=%s&domain=%s&years=%s&private=%s&auto_renew=%s" % \
                     (self.__token, domain_name, years, private, auto_renew)
        parsed_content = self.__get_content(url_extend)
