import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nfs_common_is_installed(host, os_map):
    nfs = host.package(os_map['pkg_nfsutils'])
    assert nfs.is_installed


def test_nfs_exports_exist(host, os_map):
    exports = host.check_output(os_map['cmd_showmount'] +
                                ' --exports --no-headers')
    assert exports.strip() == '/tmp *'


def test_nfs_services_running(host):
    assert host.service('rpcbind').is_running
    assert host.service('rpcbind').is_enabled
    assert host.service('nfs-server').is_running
