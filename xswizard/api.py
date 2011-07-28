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

    def _vm_get_all_records(self):
        """
        xenapi.VM.get_all_records
        """
        return self._api.VM.get_all_records()

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

    def _vm_get_snapshots(self, ref):
        """
        xenapi.VM.get_snapshots
        """
        return self._api.VM.get_snapshots(ref)

    def _vm_clone(self, ref, name):
        """
        xenapi.VM.clone
        """
        return self._api.VM.clone(ref, name)

    def _vm_provision(self, ref):
        """
        xenapi.VM.provision
        """
        return self._api.VM.provision(ref)

    def _vm_start(self, ref):
        """
        xenapi.VM.start
        """
        return self._api.VM.start(ref, False, False)

    def _vm_resume(self, ref):
        """
        xenapi.VM.resume
        """
        return self._api.VM.resume(ref, False, False)

    def _vm_clean_shutdown(self, ref):
        """
        xenapi.VM.clean_shutdown
        """
        return self._api.VM.clean_shutdown(ref)

    def _vm_clean_reboot(self, ref):
        """
        xenapi.VM.clean_reboot
        """
        return self._api.VM.clean_reboot(ref)

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

    def clone_vm(self, vm, name):
        """
        clone vm
        """
        clone_ref = self._vm_clone(vm.ref, name)
        return VM(clone_ref, self)

    def provision_vm(self, vm):
        """
        provision vm
        """
        return self._vm_provision(vm.ref)

    def start_vm(self, vm):
        """
        start vm
        """
        return self._vm_start(vm.ref)

    def clean_shutdown_vm(self, vm):
        """
        clean shutdown vm
        """
        return self._vm_clean_shutdown(vm.ref)

    def shutdown_vm(self, vm):
        """
        shutdown vm alias
        """
        return self.clean_shutdown_vm(vm)

    def clean_reboot_vm(self, vm):
        """
        clean reboot vm
        """
        return self._vm_clean_reboot(vm.ref)

    def reboot_vm(self, vm):
        """
        reboot vm alias
        """
        return self.clean_reboot_vm(vm)

    def resume_vm(self, vm):
        """
        resume vm
        """
        return self._vm_resume(vm.ref)

    def get_snapshots(self, vm):
        """
        get_snapshots vm
        """
        data = self._vm_get_snapshots(vm.ref)
        return [VM(record, self) for record in data]

    def get_all_vms(self):
        """
        all vm records
        """
        data = self._vm_get_all_records()
        return [VM(record, self) for record in data]

    def get_vm_by_name(self, name):
        """
        vm by name
        """
        vms = self.get_all_vms()
        filtered = filter(lambda vm: vm.name_label == name, vms)
        if filtered:
            return filtered[0]

    def get_all_vm_templates(self):
        """
        all vm templates
        """
        vms = self.get_all_vms()
        return filter(lambda vm: vm.is_a_template, vms)

    def get_instant_vm_templates(self):
        """
        vm templates not default
        """
        vms = self.get_all_vm_templates()
        return filter(lambda vm: vm.is_instant, vms)

    def get_instant_vm_template_by_name(self, name):
        """
        vm template by name
        """
        vms = self.get_instant_vm_templates()
        filtered = filter(lambda vm: vm.name_label == name, vms)
        if filtered:
            return filtered[0]

    def get_all_vm_not_templates(self):
        """
        all vm templates
        """
        vms = self.get_all_vms()
        return filter(lambda vm: not vm.is_a_template, vms)
