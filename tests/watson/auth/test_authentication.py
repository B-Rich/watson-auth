from tests.watson.auth import support
from watson.auth import authentication


class TestPasswords(object):
    def test_generate_password(self):
        password, salt = authentication.generate_password('test', 10)
        assert password
        assert salt

    def test_check_password(self):
        password, salt = authentication.generate_password('test', 10)
        assert authentication.check_password('test', password, salt)
        assert not authentication.check_password('testing', password, salt)


class TestAuthenticator(object):
    authenticator = None

    def setup(self):
        self.authenticator = support.app.container.get('auth_authenticator')

    def test_session(self):
        assert self.authenticator.session
        assert self.authenticator.user_model == 'tests.watson.auth.support.TestUser'

    def test_get_user(self):
        assert self.authenticator.get_user('test')
        assert not self.authenticator.get_user('testing')
        assert self.authenticator.get_user_by_id(1)
        assert not self.authenticator.get_user_by_id(100)

    def test_authenticate_user(self):
        assert self.authenticator.authenticate('test', 'test')
        assert not self.authenticator.authenticate('test', 'testing')

    def test_authenticate_password_longer_max_length(self):
        assert not self.authenticator.authenticate('test', '1234567890123456789012345678901')
