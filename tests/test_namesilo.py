import unittest

from unittest import mock

from namesilo.core import NameSilo, ContactModel
from namesilo.common import DomainInfo
from namesilo.exceptions import APIRequestError, DomainProcessingError
from tests.mocked_data import mocked_data, mocked_single_contact


class NameSiloTestCase(unittest.TestCase):
    def setUp(self):
        self.ns = NameSilo("name-silo-token", sandbox=True)

    def test_production_api_url(self):
        ns = NameSilo("name-silo-token", sandbox=False)
        self.assertEqual(ns._base_url, "https://www.namesilo.com/api/")

    def test_sandbox_api_url(self):
        ns = NameSilo("name-silo-token", sandbox=True)
        self.assertEqual(ns._base_url, "http://sandbox.namesilo.com/api/")

    @mock.patch('namesilo.core.NameSilo._get_error_code')
    @mock.patch('namesilo.core.NameSilo.check_error_code')
    @mock.patch('namesilo.core.NameSilo._get_content_xml')
    def test_process_data(self, mock_xml, mock_check, mock_error_code):
        self.ns._process_data("some-url-extend")
        mock_xml.assert_called_once_with("some-url-extend")
        mock_check.assert_called_once()
        mock_error_code.assert_called_once()

    @mock.patch('namesilo.core.requests.get')
    def test_get_content_xml(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = "<?xml version='1.0' encoding='UTF-8'?>" \
                                "<example></example>".encode('utf-8')

        mock_requests.return_value = mock_response
        result = self.ns._get_content_xml('some_url_extend')
        self.assertIsInstance(result, dict)
        mock_requests.assert_called_once_with(
            "http://sandbox.namesilo.com/api/some_url_extend"
        )

    @mock.patch('namesilo.core.requests.get')
    def test_get_content_xml_exception(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_requests.return_value = mock_response
        self.assertRaises(Exception, self.ns._get_content_xml, 'url')
        mock_requests.assert_called_once_with(
            "http://sandbox.namesilo.com/api/url"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_account_balance(self, mock_process_data):
        mock_process_data.return_value = mocked_data
        balance = self.ns.get_account_balance()
        self.assertIsInstance(balance, float)
        self.assertEqual(balance, 500)
        mock_process_data.assert_called_once_with(
            "getAccountBalance?version=1&type=xml&key=name-silo-token"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_add_funds(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        status, balance = self.ns.add_account_funds(5, 281)
        self.assertEqual(balance, 505)
        mock_content_xml.assert_called_once_with(
            "addAccountFunds?version=1&type=xml&key=name-silo-token&amount=5&"
            "payment_id=281"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_domain_check_available(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.check_domain(domain_name))
        mock_content_xml.assert_called_once_with(
            "checkRegisterAvailability?version=1&type=xml&key=name-silo-token&"
            "domains=some-domain.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_domain_check_not_available(self, mock_content_xml):
        domain_name = "some-domain.com"
        del mocked_data['namesilo']['reply']['available']
        mock_content_xml.return_value = mocked_data
        self.assertFalse(self.ns.check_domain(domain_name))
        mock_content_xml.assert_called_once_with(
            "checkRegisterAvailability?version=1&type=xml&key=name-silo-token&"
            "domains=some-domain.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_domain_registration(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.register_domain(domain_name))
        mock_content_xml.assert_called_once_with(
            "registerDomain?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com&years=1&private=0&auto_renew=0"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_domain_renewal(self, mock_content_xml):
        domain_name = "some-domain.com"
        mocked_data['namesilo']['reply']['code'] = 300
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.renew_domain(domain_name))
        mock_content_xml.assert_called_once_with(
            "renewDomain?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com&years=1"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_lock_domain(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.lock_domain("example.com"))
        mock_content_xml.assert_called_once_with(
            "domainLock?version=1&type=xml&key=name-silo-token&"
            "domain=example.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_unlock_domain(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.unlock_domain("example.com"))
        mock_content_xml.assert_called_once_with(
            "domainUnlock?version=1&type=xml&key=name-silo-token&"
            "domain=example.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_list_domains(self, mock_content_xml):
        mocked_data['namesilo']['reply']['code'] = 300
        mock_content_xml.return_value = mocked_data
        self.assertEqual(
            self.ns.list_domains(),
            mocked_data['namesilo']['reply']['domains']['domain']
        )
        mock_content_xml.assert_called_once_with(
            "listDomains?version=1&type=xml&key=name-silo-token"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_contacts_lists(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertIsInstance(self.ns.list_contacts(), list)
        mock_content_xml.assert_called_once_with(
            "contactList?version=1&type=xml&key=name-silo-token"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_contacts_lists_only_one_contact(self, mock_content_xml):
        mock_content_xml.return_value = mocked_single_contact
        self.assertIsInstance(self.ns.list_contacts(), list)
        mock_content_xml.assert_called_once_with(
            "contactList?version=1&type=xml&key=name-silo-token"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_add_contact(self, mock_content_xml):
        mock_content_xml.return_value = mocked_single_contact
        self.assertTrue(self.ns.add_contact(ContactModel(
            **mocked_single_contact['namesilo']['reply']['contact'])
        ))
        mock_content_xml.assert_called_once_with(
            'contactAdd?version=1&type=xml&key=name-silo-token&fn=First&'
            'ln=Last&ad=Fake%20Address%2018&cy=Zrenjanin&st=Vojvodina&'
            'zp=23000&ct=RS&em=some.email@some.domain.com&ph=003816050005000'
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_update_contact(self, mock_content_xml):
        temp_contact = ContactModel(
            contact_id="10050",
            first_name="First",
            last_name="Last",
            address="Some address",
            city="Some city",
            state="Some state",
            country="US",
            email="some.email@some-provider.com",
            phone="00381695959559",
            zip="21000"
        )
        self.assertEqual(temp_contact.__str__(), "First Last - 10050")
        self.assertTrue(
            self.ns.update_contact(temp_contact)
        )

        mock_content_xml.assert_called_once_with(
            "contactUpdate?version=1&type=xml&key=name-silo-token&"
            "contact_id=10050&fn=First%20Last&ad=Some%20address&"
            "cy=Some%20city&st=Some%20state&zp=21000&ct=US&"
            "em=some.email@some-provider.com&ph=00381695959559"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_delete_contact(self, mock_process):
        mock_process.return_value = dict()
        self.ns.delete_contact(500)
        mock_process.assert_called_once_with(
            "contactDelete?version=1&type=xml&"
            "key=name-silo-token&contact_id=500"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_domain_price(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertIsInstance(self.ns.get_prices(), dict)
        mock_content_xml.assert_called_once_with(
            "getPrices?version=1&type=xml&key=name-silo-token"
        )

    def test_check_error_code(self):
        self.assertIsInstance(self.ns.check_error_code((300, "")), str)

    def test_check_error_code_exception(self):
        self.assertRaises(APIRequestError, self.ns.check_error_code, (400, ""))

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_get_domain_info(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        mocked_data['namesilo']['reply']['code'] = 300
        self.assertIsInstance(
            self.ns.get_domain_info("some-domain.com"), DomainInfo
        )
        mock_content_xml.assert_called_once_with(
            "getDomainInfo?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_change_domain_nameservers(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertTrue(
            self.ns.change_domain_nameservers(
                "example.com", "NS1.EXAMPLE.COM", "NS2.EXAMPLE.COM"
            )
        )
        mock_content_xml.assert_called_once_with(
            "changeNameServers?version=1&type=xml&key=name-silo-token&"
            "domain=example.com&ns1=NS1.EXAMPLE.COM&ns2=NS2.EXAMPLE.COM"
        )

    @mock.patch('namesilo.core.NameSilo._get_content_xml')
    def test_domain_registration_fail(self, mock_content_xml):
        domain_name = "some-domain.com"
        mocked_data['namesilo']['reply']['code'] = 261
        mock_content_xml.return_value = mocked_data
        self.assertRaises(DomainProcessingError, self.ns.register_domain,
                          domain_name)
        mock_content_xml.assert_called_once_with(
            "registerDomain?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com&years=1&private=0&auto_renew=0"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_add_domain_privacy(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.add_domain_privacy(domain_name))
        mock_content_xml.assert_called_once_with(
            "addPrivacy?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_remove_domain_privacy(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.remove_domain_privacy(domain_name))
        mock_content_xml.assert_called_once_with(
            "removePrivacy?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_auto_renew_domain(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.auto_renew_domain(domain_name))
        mock_content_xml.assert_called_once_with(
            "addAutoRenewal?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com"
        )

    @mock.patch('namesilo.core.NameSilo._process_data')
    def test_remove_auto_renew_domain(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.ns.remove_auto_renew_domain(domain_name))
        mock_content_xml.assert_called_once_with(
            "removeAutoRenewal?version=1&type=xml&key=name-silo-token&"
            "domain=some-domain.com"
        )


if __name__ == '__main__':
    unittest.main()

