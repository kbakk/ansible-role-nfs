import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture(scope='module')
def os_map(host):
    os_fam = host.ansible('setup')['ansible_facts']['ansible_os_family']
    os_fam = str(os_fam).lower()
    map_ = dict(
        cmd_showmount=dict(debian='/sbin/showmount',
                           redhat='/usr/sbin/showmount'),
        pkg_nfsutils=dict(debian='nfs-common', redhat='nfs-utils'),
        stdout_showmount_nfs_1=dict(debian='127.0.0.1:/exports', redhat='::1:/exports')
    )
    return {k: v[os_fam] for k, v in map_.items()}
