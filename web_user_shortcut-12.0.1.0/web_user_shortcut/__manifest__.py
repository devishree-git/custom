# -*- coding: utf-8 -*-
{
    'name': 'User Shortcut Menu',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'version': '12.0.1.0',
    'author': 'CuuNV',
    'maintainer': 'CuuNV <nguyenvancuu.vp@gmail.com>',
    'support': 'CuuNV <nguyenvancuu.vp@gmail.com>',
    'website': '',
    # 'price': 0.0,
    # 'currency': 'EUR',
    'description': """
    Shortcut menu
    =============
    Allow user add list of frequently used menu items and display in a systray item
    """,
    'depends': [
        'base',
        'web'
    ],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/templates.xml'
    ],
    'installable': True,
    'auto_install': False,
}
