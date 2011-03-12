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

    def snapshot(self, name):
        return self.api.snapshot_vm(self, name)

    def suspend(self):
        return self.api.suspend_vm(self)

    def _export(self):
        return self.api._export(self.record['uuid'])

    def export_as_file(self, filepath):
        input = self._export()
        output = open(filepath, 'wb')
        while True:
            data = input.read(constants.EXPORT_BLOCK_SIZE)
            if not data:
                break
            output.write(data)
        output.close()
