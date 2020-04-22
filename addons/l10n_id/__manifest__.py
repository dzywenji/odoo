# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Indonesian - Accounting',
    'version': '1.0',
<<<<<<< HEAD
    'category': 'Localization',
=======
    'category': 'Accounting/Localizations',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
    'description': """
This is the latest Indonesian Odoo localisation necessary to run Odoo accounting for SMEs with:
=================================================================================================
    - generic Indonesian chart of accounts
    - tax structure""",
    'author': 'vitraining.com',
    'website': 'http://www.vitraining.com',
<<<<<<< HEAD
    'depends': ['account', 'base_iban', 'base_vat'],
=======
    'depends': ['account', 'base_iban', 'base_vat', 'l10n_multilang'],
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
    'data': [
        'data/account_chart_template_data.xml',
        'data/account.account.template.csv',
        'data/account_chart_template_post_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_chart_template_configuration_data.xml',
<<<<<<< HEAD
        'views/account_reconcile_model_views.xml',
    ],
=======
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'post_init_hook': 'load_translations',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
}
