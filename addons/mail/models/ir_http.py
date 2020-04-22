# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        user = request.env.user
        result = super(IrHttp, self).session_info()
        if self.env.user.has_group('base.group_user'):
<<<<<<< HEAD
            result['out_of_office_message'] = user.out_of_office_message
=======
            result['notification_type'] = user.notification_type
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
        return result
