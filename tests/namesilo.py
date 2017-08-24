import unittest

from unittest import mock

from main import NameSilo, ContactModel
from common.models import DomainInfo
from common.error_codes import check_error_code
from tests.mocked_data import mocked_data, mocked_single_contact


class NamesiloTestCase(unittest.TestCase):
    def setUp(self):
        self.namesilo = NameSilo("name-silo-token", sandbox=True)

    @mock.patch('main.NameSilo._get_content_xml')
    @mock.patch('main.check_error_code')
    @mock.patch('main.NameSilo._get_error_code')
    def test_process_data(self, mock_xml, mock_check, mock_error_code):
        self.namesilo._process_data("some-url-extend")
        mock_xml.assert_called_once()
        mock_check.assert_called_once()
        mock_error_code.assert_called_once()

    @mock.patch('main.requests.get')
    def test_get_content_xml(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = "<?xml version='1.0' encoding='UTF-8'?>" \
                                "<example></example>".encode('utf-8')

        mock_requests.return_value = mock_response
        result = self.namesilo._get_content_xml('some_url_extend')
        self.assertIsInstance(result, dict)
        mock_requests.assert_called_once()

    @mock.patch('main.requests.get')
    def test_get_content_xml_exception(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_requests.return_value = mock_response
        self.assertRaises(Exception, self.namesilo._get_content_xml, 'url')
        mock_requests.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_account_balance(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        balance = self.namesilo.get_account_balance()
        self.assertIsInstance(balance, float)
        self.assertEqual(balance, 500)
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_add_funds(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        status, balance = self.namesilo.add_account_funds(5, 281)
        self.assertEqual(balance, 505)
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_domain_check_available(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.namesilo.check_domain(domain_name))
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_domain_check_not_available(self, mock_content_xml):
        domain_name = "some-domain.com"
        del mocked_data['namesilo']['reply']['available']
        mock_content_xml.return_value = mocked_data
        self.assertFalse(self.namesilo.check_domain(domain_name))
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_domain_registration(self, mock_content_xml):
        domain_name = "some-domain.com"
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.namesilo.register_domain(domain_name))
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_domain_renewal(self, mock_content_xml):
        domain_name = "some-domain.com"
        mocked_data['namesilo']['reply']['code'] = 300
        mock_content_xml.return_value = mocked_data
        self.assertTrue(self.namesilo.renew_domain(domain_name))
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_list_domains(self, mock_content_xml):
        mocked_data['namesilo']['reply']['code'] = 300
        mock_content_xml.return_value = mocked_data
        self.assertEqual(
            self.namesilo.list_domains(),
            mocked_data['namesilo']['reply']['domains']['domain']
        )
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_contacts_lists(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertIsInstance(self.namesilo.list_contacts(), list)
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_contacts_lists_only_one_contact(self, mock_content_xml):
        mock_content_xml.return_value = mocked_single_contact
        self.assertIsInstance(self.namesilo.list_contacts(), list)
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_add_contact(self, mock_content_xml):
        mock_content_xml.return_value = mocked_single_contact
        self.assertTrue(self.namesilo.add_contact(ContactModel(
            **mocked_single_contact['namesilo']['reply']['contact'])
        ))
        mock_content_xml.assert_called_once_with(
            'contactAdd?version=1&type=xml&key=name-silo-token&fn=First&'
            'ln=Last&ad=Fake%20Address%2018&cy=Zrenjanin&st=Vojvodina&'
            'zp=23000&ct=RS&em=some.email@some.domain.com&ph=003816050005000'
        )

    @mock.patch('main.NameSilo._process_data')
    def test_delete_contact(self, mock_process):
        mock_process.return_value = dict()
        self.namesilo.delete_contact(500)
        mock_process.assert_called_once_with(
            "contactDelete?version=1&type=xml&"
            "key=name-silo-token&contact_id=500"
        )

    @mock.patch('main.NameSilo._get_content_xml')
    def test_domain_price(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        self.assertIsInstance(self.namesilo.get_prices(), dict)
        mock_content_xml.assert_called_once()

    def test_check_error_code(self):
        self.assertIsInstance(check_error_code((300, "")), str)

    @mock.patch('main.NameSilo._get_content_xml')
    def test_get_domain_info(self, mock_content_xml):
        mock_content_xml.return_value = mocked_data
        mocked_data['namesilo']['reply']['code'] = 300
        self.assertIsInstance(self.namesilo.get_domain_info("some-domain.com"),
                              DomainInfo)
        mock_content_xml.assert_called_once()

    @mock.patch('main.NameSilo._get_content_xml')
    def test_domain_registration_fail(self, mock_content_xml):
        domain_name = "some-domain.com"
        mocked_data['namesilo']['reply']['code'] = 261
        mock_content_xml.return_value = mocked_data
        self.assertRaises(Exception, self.namesilo.register_domain,
                          domain_name)
        mock_content_xml.assert_called_once()

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as ex:
        print(str(ex))
