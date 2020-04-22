# -*- coding: utf-8 -*-
<<<<<<< HEAD
from odoo.addons.account.tests.account_test_savepoint import AccountingSavepointCase
=======
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
from odoo.tests import tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
<<<<<<< HEAD
class TestAccountTax(AccountingSavepointCase):
=======
class TestAccountTax(AccountTestInvoicingCommon):
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create another company.
        cls.company_data_2 = cls.setup_company_data('company_2_data')

        # By default, tests are run with the current user set on the first company.
        cls.env.user.company_id = cls.company_data['company']

    def test_changing_tax_company(self):
        ''' Ensure you can't change the company of an account.tax if there are some journal entries '''

        # Avoid duplicate key value violates unique constraint "account_tax_name_company_uniq".
        self.company_data['default_tax_sale'].name = 'test_changing_account_company'

        self.env['account.move'].create({
<<<<<<< HEAD
            'type': 'out_invoice',
=======
            'move_type': 'out_invoice',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
            'date': '2019-01-01',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'invoice_line',
                    'quantity': 1.0,
                    'price_unit': 100.0,
                    'tax_ids': [(6, 0, self.company_data['default_tax_sale'].ids)],
                }),
            ],
        })

        with self.assertRaises(UserError), self.cr.savepoint():
            self.company_data['default_tax_sale'].company_id = self.company_data_2['company']
