LDAP Multi Login
++++++++++++++++
This module extends the functionality of the auth_ldap module to support Login attribute,
and allows you to specify several fields in the filter to search for a user in ldap

Configuration
*************
1 Installed LDAP Multi Login module
2 Go to Settings -> Setup your LDAP Server
3 Configure module
4 In the Login attribute field, specify the fields by whichyou want to search for users in ldap

Here is how it works:
---------------------
    * The system first attempts to authenticate users against the local Odoo
      database;
    * if this authentication fails (for example because the user has no local password),
      the system then attempts to authenticate against LDAP;
    * if the user is not in the database, but is in the ldap directory,
      a new user will be created with the login specified in the login attribute field;
As LDAP users have blank passwords by default in the local Odoo database (which means no access),
the first step always fails and the LDAP server is queried to do the authentication.


