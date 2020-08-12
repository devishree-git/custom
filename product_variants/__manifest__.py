# -*- coding: utf-8 -*-
##############################################################################      
#         _______  _____            _______  _       _______
#         |     | |       |       | |     | | \    |    |    |     |
#         |_____| |_____  |   _   | |_____| |  \   |    |    |_____|
#         |     |       | |  / \  | |     | |   \  |    |    |     |
#         |     |  _____| |_/   \_| |     | |    \_|    |    |     |
#                 
##############################################################################


{
    'name': 'product varient configuration',
    'version': '12.0.1.0.0',
    'summary': 'product varient',
    'author': 'Aswanth',
    'description': """
                """,
    'depends': ['base','sale','product'],
    'category': 'Tools',
    'data': [
        'views/sale_view.xml',
        'security/ir.model.access.csv'
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
