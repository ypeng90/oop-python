"""
Unit tests
Command line: python test_account.py
"""

from account import TimeZone, Account
from datetime import timedelta
import unittest


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account_number = "A100"
        self.first_name = "FIRST"
        self.last_name = "LAST"
        self.tz = TimeZone("TZ", 1, 30)
        self.balance = 100.00
    
    def create_account(self):
        return Account(self.account_number, self.first_name, self.last_name, self.tz, self.balance)
    
    def test_create_timezone(self):
        tz = TimeZone("ABC", -1, -30)
        self.assertEqual("ABC", tz.name)
        self.assertEqual(timedelta(hours=-1, minutes=-30), tz.offset)
    
    def test_timezones_equal(self):
        tz1 = TimeZone("ABC", -1, -30)
        tz2 = TimeZone("ABC", -1, -30)
        self.assertEqual(tz1, tz2)
    
    def test_timezones_not_equal(self):
        tz = TimeZone("ABC", -1, -30)
        test_timezones = (
            TimeZone("DEF", -1, -30),
            TimeZone("ABC", -1, 0),
            TimeZone("ABC", 1, -30)
        )
        
        for i, test_tz in enumerate(test_timezones):
            with self.subTest(test_number=i):
                self.assertNotEqual(tz, test_tz)
    
    def test_create_account(self):
        a = self.create_account()
        self.assertEqual(self.account_number, a.account_number)
        self.assertEqual(self.first_name, a.first_name)
        self.assertEqual(self.last_name, a.last_name)
        self.assertEqual(self.first_name + " " + self.last_name, a.full_name)
        self.assertEqual(self.tz, a.timezone)
        self.assertEqual(self.balance, a.balance)
    
    def test_create_account_blank_first_name(self):
        self.first_name = ""
        
        with self.assertRaises(ValueError):
            self.create_account()
    
    def test_create_account_negative_balance(self):
        self.balance = -100.00
        
        with self.assertRaises(ValueError):
            self.create_account()
    
    def test_account_deposit_ok(self):
        a = self.create_account()
        conf_code = a.deposit(100)
        # self.assertIn("D-", conf_code)
        self.assertTrue(conf_code.startswith("D-"))
        self.assertEqual(200, a.balance)
    
    def test_account_deposit_negative_amount(self):
        a = self.create_account()
        with self.assertRaises(ValueError):
            a.deposit(-100)
    
    def test_account_withdraw_ok(self):
        a = self.create_account()
        conf_code = a.withdraw(20)
        self.assertEqual(80, a.balance)
        self.assertTrue(conf_code.startswith("W-"))
    
    def test_account_withdraw_negative_amount(self):
        a = self.create_account()
        with self.assertRaises(ValueError):
            a.withdraw(-100)
    
    def test_account_withdraw_overdraw(self):
        a = self.create_account()
        conf_code = a.withdraw(200)
        self.assertTrue(conf_code.startswith("X-"))
        self.assertEqual(self.balance, a.balance)


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    run_tests(TestAccount)
