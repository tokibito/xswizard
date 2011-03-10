from xswizard.models import Host

class API(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.is_login = False
        self._session = None

    def _create_session(self):
        from xswizard import XenAPI
        return XenAPI.Session(self.url)

    def _get_sesion(self):
        if self._session is None:
            self._session = self._create_session()
        return self._session
    session = property(_get_sesion)

    def _get_api(self):
        if not self.is_login:
            self._login()
        return self.session.xenapi
    _api = property(_get_api)

    def _login(self):
        """
        xenapi.login_with_password
        """
        self.session.xenapi.login_with_password(self.username, self.password)
        self.is_login = True

    def _host_get_all(self):
        """
        xenapi.host.get_all
        """
        return self._api.host.get_all()

    def _host_get_record(self, ref):
        """
        xenapi.host.get_record
        """
        return self._api.host.get_record(ref)

    def _vm_get_record(self, ref):
        """
        xenapi.VM.get_record
        """
        return self._api.VM.get_record(ref)

    def get_hosts(self):
        data = self._host_get_all()
        return [Host(record, self) for record in data]
