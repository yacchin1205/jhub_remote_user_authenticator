import pytest
from jhub_remote_user_authenticator import remote_user_auth


@pytest.mark.parametrize('authclass',
                         [remote_user_auth.RemoteUserAuthenticator,
                          remote_user_auth.RemoteUserLocalAuthenticator])
def test_valid_organization(authclass):
    auth = authclass()
    assert auth.check_valid_organization({})

    auth.allow_any_organizations = False
    assert auth.check_valid_organization({})
