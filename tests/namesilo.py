import os
import unittest
from random import uniform
from uuid import uuid4
from main import NameSilo, ContactModel
from common.models import DomainInfo
from common.error_codes import check_error_code


class NamesiloTestCase(unittest.TestCase):
    namesilo = NameSilo(os.environ['TOKEN'], sandbox=True)

    def test_account_balance(self):
        balance = self.namesilo.get_account_balance()
        self.assertIsInstance(balance, float)
        self.assertGreaterEqual(balance, 0)

    def test_add_funds(self):
        starting_balance = self.namesilo.get_account_balance()
        random_amount = round(uniform(0, 50), 2)
        expected_amount = round(starting_balance + random_amount, 2)
        status, balance = self.namesilo.add_account_funds(random_amount, 281)
        self.assertEqual(expected_amount, balance)

    def test_domain_check_available(self):
        domain_name = "%s.com" % uuid4()
        self.assertTrue(self.namesilo.check_domain(domain_name))

    def test_domain_check_not_availabe(self):
        registered_domains = self.namesilo.list_domains()
        self.assertFalse(self.namesilo.check_domain(registered_domains[0]))

    def test_domain_registration(self):
        domain_name = "test-%s.com" % uuid4()
        self.assertTrue(self.namesilo.register_domain(domain_name))

    def test_domain_renewal(self):
        domain_name = self.namesilo.list_domains()[0]
        self.assertTrue(self.namesilo.renew_domain(domain_name))

    def test_domain_registration_fail(self):
        self.assertRaises(Exception, self.namesilo.register_domain)

    def test_contacts_lists(self):
        self.assertIsInstance(self.namesilo.list_contacts(), list)

    def test_domain_price(self):
        self.assertIsInstance(self.namesilo.get_prices(), dict)

    def test_check_error_code(self):
        self.assertIsInstance(check_error_code((300, "")), str)

    def test_get_domain_info(self):
        self.assertIsInstance(self.namesilo.get_domain_info(self.namesilo.list_domains()[0]), DomainInfo)

    def test_add_contact(self):
        contact = ContactModel("First", "Last", "Address 15", "Some City", "Vojvodina", "RS", "test@nomail.com", "0038169999999", "21000")
        self.assertTrue(self.namesilo.add_contact(contact))

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as ex:
        print(str(ex))
