# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Drop Shipping',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Drop Shipping',
    'description': """
Manage drop shipping orders
===========================

This module adds a pre-configured Drop Shipping operation type
as well as a procurement route that allow configuring Drop
Shipping products and orders.

When drop shipping is used the goods are directly transferred
from vendors to customers (direct delivery) without
going through the retailer's warehouse. In this case no
internal transfer document is needed.

""",
<<<<<<< HEAD
    'depends': ['sale_purchase', 'sale_stock', 'purchase_stock'],
=======
    'depends': ['sale_purchase_stock'],
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
    'data': ['data/stock_data.xml', 'views/sale_order_views.xml'],
    'installable': True,
    'auto_install': False,
}
