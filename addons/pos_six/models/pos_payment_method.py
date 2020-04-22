# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
<<<<<<< HEAD
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [('six_tim', 'SIX without IoT Box')]
=======
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [('six', 'SIX')]
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

    six_terminal_ip = fields.Char('Six Terminal IP')
