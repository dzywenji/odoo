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
class TestAccountAnalyticAccount(AccountingSavepointCase):
=======
class TestAccountAnalyticAccount(AccountTestInvoicingCommon):
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env.user.write({
            'groups_id': [
                (4, cls.env.ref('analytic.group_analytic_accounting').id),
                (4, cls.env.ref('analytic.group_analytic_tags').id),
            ],
        })

        # Create another company.
        cls.company_data_2 = cls.setup_company_data('company_2_data')

        # By default, tests are run with the current user set on the first company.
        cls.env.user.company_id = cls.company_data['company']

        cls.test_analytic_account = cls.env['account.analytic.account'].create({'name': 'test_analytic_account'})
        cls.test_analytic_tag = cls.env['account.analytic.tag'].create({'name': 'test_analytic_tag'})

    def test_changing_analytic_company(self):
        ''' Ensure you can't change the company of an account.analytic.account if there are some journal entries '''

        self.env['account.move'].create({
<<<<<<< HEAD
            'type': 'entry',
=======
            'move_type': 'entry',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
            'date': '2019-01-01',
            'line_ids': [
                (0, 0, {
                    'name': 'line_debit',
                    'account_id': self.company_data['default_account_revenue'].id,
                    'analytic_account_id': self.test_analytic_account.id,
                    'analytic_tag_ids': [(6, 0, self.test_analytic_tag.ids)],
                }),
                (0, 0, {
                    'name': 'line_credit',
                    'account_id': self.company_data['default_account_revenue'].id,
                }),
            ],
        })

        # Set a different company on the analytic account.
        with self.assertRaises(UserError), self.cr.savepoint():
            self.test_analytic_account.company_id = self.company_data_2['company']

        # Making the analytic account not company dependent is allowed.
        self.test_analytic_account.company_id = False

        # Set a different company on the analytic tag.
        with self.assertRaises(UserError), self.cr.savepoint():
            self.test_analytic_tag.company_id = self.company_data_2['company']

        # Making the analytic tag not company dependent is allowed.
        self.test_analytic_tag.company_id = False
