# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html)

{
    "name": "LDAP multi login",
    "summary": """
        The module allows you to specify several fields in ldap to find the entered login""",
    "description": """
        The module allows you to specify several fields in ldap to find the entered login.
        Also you can specify which ldap field to use as the login when creating the user Odoo.
    """,
    "author": "Rydlab",
    "support": "company@rydlab.ru",
    "website": "https://rydlab.ru",
    "license": "LGPL-3",
    "category": "Tools",
    "version": "12.0.0.1.0",
    "sequence": 10,
    "depends": ["base", "auth_ldap"],
    "data": ["views/res_company_ldap_views.xml"],
    "images": ["static/description/rydlab_ldap_2.jpg"]
}
