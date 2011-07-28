from xswizard.exceptions import APINotSet
from xswizard import constants


class BaseModel(object):
    def __init__(self, api=None):
        self._api = api

    def get_api(self):
        if self._api is None:
            raise APINotSet
        return self._api

    def set_api(self, api):
        self._api = api

    api = property(get_api, set_api)


class RefModel(BaseModel):
    def __init__(self, ref, api=None):
        super(RefModel, self).__init__(api)
        self._ref = ref

    def _get_ref(self):
        return self._ref
    ref = property(_get_ref)

    def __repr__(self):
        return '<%s.%s: %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ref)


class Host(RefModel):
    def __init__(self, ref, api=None):
        super(Host, self).__init__(ref, api)
        self._record = None

    def get_record(self):
        if self._record is None:
            self._record = self.api._host_get_record(self.ref)
        return self._record
    record = property(get_record)

    def get_residentVMs(self):
        data = self.record['resident_VMs']
        return [VM(record, self.api) for record in data]
    residentVMs = property(get_residentVMs)


class VM(RefModel):
    def __init__(self, ref, api=None):
        super(VM, self).__init__(ref, api)
        self._record = None

    def get_record(self):
        if self._record is None:
            self._record = self.api._vm_get_record(self.ref)
        return self._record
    record = property(get_record)

    def __repr__(self):
        return '<%s.%s: %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.record['name_label'])

    def get_is_control_domain(self):
        return self.record['is_control_domain']
    is_control_domain = property(get_is_control_domain)

    def get_is_a_template(self):
        return self.record['is_a_template']
    is_a_template = property(get_is_a_template)

    def get_is_default_template(self):
        value = self.record['other_config'].get('default_template')
        return value == 'true'
    is_default_template = property(get_is_default_template)

    def get_is_instant(self):
        value = self.record['other_config'].get('instant')
        return value == 'true'
    is_instant = property(get_is_instant)

    def get_name_label(self):
        return self.record['name_label']
    name_label = property(get_name_label)

    def snapshot(self, name):
        return self.api.snapshot_vm(self, name)

    def suspend(self):
        return self.api.suspend_vm(self)

    def clone(self, name):
        return self.api.clone_vm(self, name)

    def provision(self):
        return self.api.provision_vm(self)

    def start(self):
        return self.api.start_vm(self)

    def resume(self):
        return self.api.resume_vm(self)

    def clean_shutdown(self):
        return self.api.clean_shutdown_vm(self)

    def shutdown(self):
        return self.api.shutdown_vm(self)

    def clean_reboot(self):
        return self.api.clean_reboot_vm(self)

    def reboot(self):
        return self.api.reboot_vm(self)

    def get_snapshots(self):
        return self.api.get_snapshots(self)

    def export(self):
        return self.api._export(self.record['uuid'])

    def export_as_file(self, filepath):
        input = self.export()
        output = open(filepath, 'wb')
        while True:
            data = input.read(constants.EXPORT_BLOCK_SIZE)
            if not data:
                break
            output.write(data)
        output.close()
