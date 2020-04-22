# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
<<<<<<< HEAD
=======

from odoo import api, SUPERUSER_ID

def load_translations(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref('l10n_id.l10n_id_chart').process_coa_translations()
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
