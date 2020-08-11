import ldap
import logging
from json import loads
from ldap.filter import filter_format
from re import findall

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


class UsersLdapRoles(models.Model):
    _inherit = "res.company.ldap"

    login_attribute = fields.Char(
        "Login attribute",
        _defaults="uid",
        help="LDAP attribute to use to retrieve login address.",
    )

    def _get_ldap_dicts(self):
        """
        Copy of auth_ldap's function, changing only the SQL, so that it returns
        all fields in the table.
        """
        return (
            self.sudo()
            .search([("ldap_server", "!=", False)], order="sequence")
            .read([])
        )

    def authenticate(self, conf, login, password):
        """
        Authenticate a user against the specified LDAP server.
        In order to prevent an unintended 'unauthenticated authentication',
        which is an anonymous bind with a valid dn and a blank password,
        check for empty passwords explicitely (:rfc:`4513#section-6.3.1`)
        added the ability to search for a login on several fields ldap
        :param dict conf: LDAP configuration
        :param login: username
        :param password: Password for the LDAP user
        :return: LDAP entry of authenticated user or False
        :rtype: dictionary of attributes
        """
        if not password:
            return False

        entry = False
        user = self.env["res.users"].search(
            [("active", "=", True), ("login", "=", login)]
        )
        _logger.info(
            "User with login {} {}".format(
                login, ("found - {}".format(user.id) if user.id else "not found")
            )
        )

        if user:
            login = (
                self.env["res.users.log"]
                .search(
                    [("create_uid", "=", user.id), ("last_ldap_login", "!=", False)],
                    limit=1,
                )
                .last_ldap_login
                or login
            )
            _logger.info("New login set - {}".format(login))
        try:
            match_count = len(findall(r"[^%](%s)", conf["ldap_filter"]))
            filter = filter_format(conf["ldap_filter"], (login,) * match_count)
        except TypeError:
            _logger.warning(
                "Could not format LDAP filter. Your filter should contain one '%s'."
            )
            return False
        try:
            results = self.query(conf, tools.ustr(filter))
            # Get rid of (None, attrs) for searchResultReference replies
            results = [i for i in results if i[0]]
            if len(results) == 1:
                dn = results[0][0]
                conn = self.connect(conf)
                conn.simple_bind_s(dn, password.encode("utf-8"))
                conn.unbind()
                entry = results[0]

        except ldap.INVALID_CREDENTIALS:
            return False

        except ldap.LDAPError as e:
            _logger.error("An LDAP exception occurred: %s", e)

        return entry

    def _get_or_create_user(self, conf, ldap_login, ldap_entry):
        immutable_ldap_login = ldap_login

        if conf["login_attribute"]:
            user_login = ldap_entry[1][conf["login_attribute"]][0]
            if user_login:
                ldap_login = user_login
        user_id = super()._get_or_create_user(conf, ldap_login, ldap_entry)

        if user_id:
            self.env["res.users"].sudo(user_id)._update_last_login(
                last_ldap_login=immutable_ldap_login
            )
        return user_id
