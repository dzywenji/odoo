import json

<<<<<<< HEAD
from odoo.addons.account.tests.account_test_classes import AccountingTestCase
=======
from odoo.addons.account.tests.common import AccountTestCommon
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
from odoo.tests import tagged


@tagged('post_install', '-at_install')
<<<<<<< HEAD
class TestAccountIncomingSupplierInvoice(AccountingTestCase):
=======
class TestAccountIncomingSupplierInvoice(AccountTestCommon):
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

    def setUp(self):
        super(TestAccountIncomingSupplierInvoice, self).setUp()

        self.env['ir.config_parameter'].sudo().set_param('mail.catchall.domain', 'test-company.odoo.com')

        self.internal_user = self.env['res.users'].create({
            'name': 'Internal User',
            'login': 'internal.user@test.odoo.com',
            'email': 'internal.user@test.odoo.com',
        })

        self.supplier_partner = self.env['res.partner'].create({
            'name': 'Your Supplier',
            'email': 'supplier@other.company.com',
            'supplier_rank': 10,
        })

        self.journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'code': 'TST',
            'type': 'purchase',
        })

        journal_alias = self.env['mail.alias'].create({
            'alias_name': 'test-bill',
            'alias_model_id': self.env.ref('account.model_account_move').id,
            'alias_defaults': json.dumps({
<<<<<<< HEAD
                'type': 'in_invoice',
=======
                'move_type': 'in_invoice',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
                'company_id': self.env.user.company_id.id,
                'journal_id': self.journal.id,
            }),
        })
        self.journal.write({'alias_id': journal_alias.id})

        self.employee_user = self.env.ref('base.user_demo')

    def test_supplier_invoice_mailed_from_supplier(self):
        message_parsed = {
            'message_id': 'message-id-dead-beef',
            'subject': 'Incoming bill',
            'from': '%s <%s>' % (self.supplier_partner.name, self.supplier_partner.email),
            'to': '%s@%s' % (self.journal.alias_id.alias_name, self.journal.alias_id.alias_domain),
            'body': "You know, that thing that you bought.",
            'attachments': [b'Hello, invoice'],
        }

<<<<<<< HEAD
        invoice = self.env['account.move'].message_new(message_parsed, {'type': 'in_invoice', 'journal_id': self.journal.id})
=======
        invoice = self.env['account.move'].message_new(message_parsed, {'move_type': 'in_invoice', 'journal_id': self.journal.id})
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

        message_ids = invoice.message_ids
        self.assertEqual(len(message_ids), 1, 'Only one message should be posted in the chatter')
        self.assertEqual(message_ids.body, '<p>Vendor Bill Created</p>', 'Only the invoice creation should be posted')

        following_partners = invoice.message_follower_ids.mapped('partner_id')
        self.assertEqual(following_partners, self.env.ref('base.partner_root'))

    def test_supplier_invoice_forwarded_by_internal_user_without_supplier(self):
        """ In this test, the bill was forwarded by an employee,
            but no partner email address is found in the body."""
        message_parsed = {
            'message_id': 'message-id-dead-beef',
            'subject': 'Incoming bill',
            'from': '%s <%s>' % (self.internal_user.name, self.internal_user.email),
            'to': '%s@%s' % (self.journal.alias_id.alias_name, self.journal.alias_id.alias_domain),
            'body': "You know, that thing that you bought.",
            'attachments': [b'Hello, invoice'],
        }

<<<<<<< HEAD
        invoice = self.env['account.move'].message_new(message_parsed, {'type': 'in_invoice', 'journal_id': self.journal.id})
=======
        invoice = self.env['account.move'].message_new(message_parsed, {'move_type': 'in_invoice', 'journal_id': self.journal.id})
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

        message_ids = invoice.message_ids
        self.assertEqual(len(message_ids), 1, 'Only one message should be posted in the chatter')
        self.assertEqual(message_ids.body, '<p>Vendor Bill Created</p>', 'Only the invoice creation should be posted')

        following_partners = invoice.message_follower_ids.mapped('partner_id')
        self.assertEqual(following_partners, self.env.ref('base.partner_root') | self.internal_user.partner_id)

    def test_supplier_invoice_forwarded_by_internal_with_supplier_in_body(self):
        """ In this test, the bill was forwarded by an employee,
            and the partner email address is found in the body."""
        message_parsed = {
            'message_id': 'message-id-dead-beef',
            'subject': 'Incoming bill',
            'from': '%s <%s>' % (self.internal_user.name, self.internal_user.email),
            'to': '%s@%s' % (self.journal.alias_id.alias_name, self.journal.alias_id.alias_domain),
            'body': "Mail sent by %s <%s>:\nYou know, that thing that you bought." % (self.supplier_partner.name, self.supplier_partner.email),
            'attachments': [b'Hello, invoice'],
        }

<<<<<<< HEAD
        invoice = self.env['account.move'].message_new(message_parsed, {'type': 'in_invoice', 'journal_id': self.journal.id})
=======
        invoice = self.env['account.move'].message_new(message_parsed, {'move_type': 'in_invoice', 'journal_id': self.journal.id})
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

        message_ids = invoice.message_ids
        self.assertEqual(len(message_ids), 1, 'Only one message should be posted in the chatter')
        self.assertEqual(message_ids.body, '<p>Vendor Bill Created</p>', 'Only the invoice creation should be posted')

        following_partners = invoice.message_follower_ids.mapped('partner_id')
        self.assertEqual(following_partners, self.env.ref('base.partner_root') | self.internal_user.partner_id)

    def test_supplier_invoice_forwarded_by_internal_with_internal_in_body(self):
        """ In this test, the bill was forwarded by an employee,
            and the internal user email address is found in the body."""
        message_parsed = {
            'message_id': 'message-id-dead-beef',
            'subject': 'Incoming bill',
            'from': '%s <%s>' % (self.internal_user.name, self.internal_user.email),
            'to': '%s@%s' % (self.journal.alias_id.alias_name, self.journal.alias_id.alias_domain),
            'body': "Mail sent by %s <%s>:\nYou know, that thing that you bought." % (self.internal_user.name, self.internal_user.email),
            'attachments': [b'Hello, invoice'],
        }

<<<<<<< HEAD
        invoice = self.env['account.move'].message_new(message_parsed, {'type': 'in_invoice', 'journal_id': self.journal.id})
=======
        invoice = self.env['account.move'].message_new(message_parsed, {'move_type': 'in_invoice', 'journal_id': self.journal.id})
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

        message_ids = invoice.message_ids
        self.assertEqual(len(message_ids), 1, 'Only one message should be posted in the chatter')
        self.assertEqual(message_ids.body, '<p>Vendor Bill Created</p>', 'Only the invoice creation should be posted')

        following_partners = invoice.message_follower_ids.mapped('partner_id')
        self.assertEqual(following_partners, self.env.ref('base.partner_root') | self.internal_user.partner_id)
