# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Colombian - Point of Sale',
    'version': '1.0',
    'description': """Colombian - Point of Sale""",
<<<<<<< HEAD
    'category': 'Localization',
=======
    'category': 'Accounting/Localizations',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
    'auto_install': True,
    'depends': [
        'l10n_co',
        'point_of_sale'
    ],
    'data': [
        'views/templates.xml',
        'views/views.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
}
