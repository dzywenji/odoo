# -*- coding: utf-8 -*-
<<<<<<< HEAD
from odoo.addons.account.tests.account_test_savepoint import AccountingSavepointCase
from odoo.tests import tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestAccountJournal(AccountingSavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create another company.
        cls.company_data_2 = cls.setup_company_data('company_2_data')

        # By default, tests are run with the current user set on the first company.
        cls.env.user.company_id = cls.company_data['company']

    def test_changing_journal_company(self):
        ''' Ensure you can't change the company of an account.journal if there are some journal entries '''

        self.env['account.move'].create({
            'type': 'entry',
            'date': '2019-01-01',
            'journal_id': self.company_data['default_journal_sale'].id,
        })

        with self.assertRaises(UserError), self.cr.savepoint():
            self.company_data['default_journal_sale'].company_id = self.company_data_2['company']
=======
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError


@tagged('post_install', '-at_install')
class TestAccountJournal(AccountTestInvoicingCommon):

    def test_constraint_currency_consistency_with_accounts(self):
        ''' The accounts linked to a bank/cash journal must share the same foreign currency
        if specified.
        '''
        journal_bank = self.company_data['default_journal_bank']
        journal_bank.currency_id = self.currency_data['currency']

        # Try to set a different currency on the 'debit' account.
        with self.assertRaises(ValidationError), self.cr.savepoint():
            journal_bank.default_debit_account_id.currency_id = self.company_data['currency']

    def test_constraint_shared_accounts(self):
        ''' Ensure the bank/outstanding accounts are not shared between multiple journals. '''
        journal_bank = self.company_data['default_journal_bank']

        account_fields = (
            'default_debit_account_id',
            'default_credit_account_id',
            'payment_debit_account_id',
            'payment_credit_account_id',
        )
        for account_field in account_fields:
            with self.assertRaises(ValidationError), self.cr.savepoint():
                journal_bank.copy(default={
                    'name': 'test_constraint_shared_accounts %s' % account_field,
                    account_field: journal_bank[account_field].id,
                })
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
