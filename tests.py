import time

from xswizard.api import API

def main():
    api = API('https://192.168.11.100/', 'root', 'test')
    print api
    vm_template = api.get_instant_vm_template_by_name('ubuntu10.04-server')
    print vm_template
    new_vm = vm_template.clone('sandbox')
    print new_vm
    new_vm.provision()
    print new_vm.ref
    print 'start...'
    new_vm.start()
    time.sleep(10)
    print 'suspend...'
    new_vm.suspend()
    time.sleep(10)
    print 'resume...'
    new_vm.resume()
    time.sleep(10)
    print 'reboot...'
    new_vm.reboot()
    time.sleep(20)
    print 'shutdown...'
    new_vm.shutdown()

if __name__ == '__main__':
    main()
