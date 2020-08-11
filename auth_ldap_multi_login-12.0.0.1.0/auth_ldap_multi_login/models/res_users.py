from odoo import api, models, fields


class ResUsersLog(models.Model):
    _inherit = "res.users.log"

    last_ldap_login = fields.Char(string="Ldap login", readonly=True, default=False)


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _update_last_login(self, last_ldap_login=None):
        # added remembering the user's last login in ldap
        # only create new records to avoid any side-effect on concurrent transactions
        # extra records will be deleted by the periodical garbage collection
        if last_ldap_login:
            self.env["res.users.log"].create(
                {"last_ldap_login": last_ldap_login}
            )  # populated by defaults
        else:
            self.env["res.users.log"].create({})
