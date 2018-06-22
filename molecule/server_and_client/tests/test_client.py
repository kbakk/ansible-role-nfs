import os
import uuid

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nfs_client_package(host, os_map):
    nfs = host.package(os_map['pkg_nfsutils'])
    assert host.package(nfs)


def test_showmount_returns_mountentry(host, os_map):
    ''' Executing showmount command
            $ showmount --all --no-header ::1
            ::1:/tmp
        Ensure output is the same'''

    mount = host.check_output(os_map['cmd_showmount'] +
                              ' --all --no-header ::1')
    assert mount.strip() == os_map['stdout_showmount_nfs_1']


def test_mount_returns_mountentry(host):
    ''' Executing mount command
            $ mount|grep /tmp
            localhost:/tmp on /mnt/remote type nfs (rw,relatime,vers=3...remov\
            ed...)
        Ensure output is the same'''
    mount = host.check_output('mount|grep /mnt/remote')
    assert mount.strip().startswith('localhost:/tmp on /mnt/remote type nfs '
                                    '(rw,relatime,vers=3')


def test_filewrite_on_mount_reflects_on_server(host):
    ''' Executing touch on mount and ensuring this is reflected on server'''
    uuid_string = str(uuid.uuid4())
    host.check_output('echo {0:s} > /mnt/remote/test_{0:s}.txt'.format(
        uuid_string))
    f = host.file('/tmp/test_{}.txt'.format(uuid_string))
    assert f.exists
    assert f.content_string == uuid_string


def test_mount_point_options(host):
    mount = host.mount_point("/mnt/remote")
    assert mount.exists
    assert set(mount.options) >= set(['rw', 'relatime', 'vers=3',
                                      'hard', 'timeo=600'])
