import base64
import urllib2

from xswizard.models import Host, VM


class API(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.is_login = False
        self._session = None

    def __repr__(self):
        return '<%s.%s: url=%s, username=%s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.url,
            self.username)

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

    def _vm_snapshot(self, ref, name):
        """
        xenapi.VM.snapshot
        """
        return self._api.VM.snapshot(ref, name)

    def _vm_suspend(self, ref):
        """
        xenapi.VM.suspend
        """
        return self._api.VM.suspend(ref)

    def _export(self, uuid):
        """
        export as backup (return stream handler)
        """
        if self.url.endswith('/'):
            url = "%sexport?uuid=%s" % (self.url, uuid)
        else:
            url = "%s/export?uuid=%s" % (self.url, uuid)
        auth = base64.b64encode("%s:%s" % (self.username, self.password))
        request = urllib2.Request(url)
        request.add_header('Authorization', "Basic %s" % auth)
        return urllib2.urlopen(request)

    def get_hosts(self):
        data = self._host_get_all()
        return [Host(record, self) for record in data]

    def snapshot_vm(self, vm, name):
        """
        create vm snapshot
        """
        snapshot_ref = self._vm_snapshot(vm.ref, name)
        return VM(snapshot_ref, self)

    def suspend_vm(self, vm):
        """
        suspend vm
        """
        self._vm_suspend(vm.ref)
