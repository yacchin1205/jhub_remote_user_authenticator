
import os
import re
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode, Bool
from .utils import normalize_quoted_printable


def check_valid_organization(headers):
    eppn = headers.get('Eppn', None)
    mail = headers.get('Mail', None)
    if eppn is None:
        return False
    if eppn.endswith('@openidp.nii.ac.jp'):
        if mail is None or not (re.match(r'^.*\.(ac|go)\.jp$', mail) or
           re.match(r'^.*\@(.+\.)?waseda\.jp$', mail)):
            return False
    return True


class RemoteUserLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        remote_user = self.request.headers.get(header_name, "")
        if remote_user == "":
            raise web.HTTPError(401)
        if not self.authenticator.check_valid_organization(self.request.headers):
            raise web.HTTPError(401)
        if self.authenticator.use_quoted_printable_normalization:
            remote_user = normalize_quoted_printable(remote_user)

        user = self.user_from_username(remote_user)
        self.set_login_cookie(user)
        if hasattr(user, "mail_address"):
            mail_header_name = self.authenticator.mail_header_name
            mail_address = self.request.headers.get(mail_header_name, "")
            self.log.debug("E-mail address of user, current={}, set={}".format(user.mail_address, mail_address))
            if mail_address:
                user.mail_address = mail_address
                self.db.commit()
        else:
            self.log.debug("No mail_address attribute")
        next_url = self.get_next_url(user)
        self.redirect(next_url)


class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    """
    Accept the email address of authenticated user from the X_AUTH_MAIL_ADDRESS HTTP header.
    """
    mail_header_name = Unicode(
        default_value='X_AUTH_MAIL_ADDRESS',
        config=True,
        help="""HTTP header to inspect for the email address of authenticated user.""")

    """
    Whether to apply quoted_printable_normalization to REMOTE_USER header.
    """
    use_quoted_printable_normalization = Bool(
        default_value=True,
        config=True,
        help="""Whether to apply quoted_printable_normalization to REMOTE_USER header""")

    """
    Custom Logout URL (e.g. Shibboleth.sso/Logout)
    """
    custom_logout_url = Unicode(
        default_value='',
        config=True,
        help="""The URL for Logout button""")

    """
    Whether to allow any organizations.
    """
    allow_any_organizations = Bool(
        default_value=False,
        config=True,
        help="""Whether to allow any organizations""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    def logout_url(self, base_url):
        if len(self.custom_logout_url):
            return self.custom_logout_url
        return super(RemoteUserAuthenticator, self).logout_url(base_url)

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()

    def check_valid_organization(self, headers):
        if self.allow_any_organizations:
            return True
        self.log.debug("Headers: {}".format(list(headers.keys())))
        self.log.debug("Eppn: {}".format(headers.get('Eppn', '(None)')))
        self.log.debug("Affiliation: {}".format(headers.get('Affiliation', '(None)')))
        self.log.debug("Mail: {}".format(headers.get('Mail', '(None)')))
        return check_valid_organization(headers)


class RemoteUserLocalAuthenticator(LocalAuthenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    """
    Accept the email address of authenticated user from the X_AUTH_MAIL_ADDRESS HTTP header.
    """
    mail_header_name = Unicode(
        default_value='X_AUTH_MAIL_ADDRESS',
        config=True,
        help="""HTTP header to inspect for the email address of authenticated user.""")

    """
    Whether to apply quoted_printable_normalization to REMOTE_USER header.
    """
    use_quoted_printable_normalization = Bool(
        default_value=True,
        config=True,
        help="""Whether to apply quoted_printable_normalization to REMOTE_USER header""")

    """
    Custom Logout URL (e.g. Shibboleth.sso/Logout)
    """
    custom_logout_url = Unicode(
        default_value='',
        config=True,
        help="""The URL for Logout button""")

    """
    Whether to allow any organizations.
    """
    allow_any_organizations = Bool(
        default_value=False,
        config=True,
        help="""Whether to allow any organizations""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    def logout_url(self, base_url):
        if len(self.custom_logout_url):
            return self.custom_logout_url
        return super(RemoteUserLocalAuthenticator, self).logout_url(base_url)

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()

    def check_valid_organization(self, headers):
        if self.allow_any_organizations:
            return True
        self.log.debug("Headers: {}".format(list(headers.keys())))
        self.log.debug("Eppn: {}".format(headers.get('Eppn', '(None)')))
        self.log.debug("Affiliation: {}".format(headers.get('Affiliation', '(None)')))
        self.log.debug("Mail: {}".format(headers.get('Mail', '(None)')))
        return check_valid_organization(headers)
