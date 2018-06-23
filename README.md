NFS server/client Role
=======================

Install NFS server/client. This role has been specifically developed to be used in the INDIGO project.


Role Variables
--------------

The variables that can be passed to this role and a brief description about them are as follows.

```yaml
# NFS install mode: server and/or client
nfs_mode: ["server"]

# Line to add to the /etc/exports file
nfs_exports:
  - path: "/home"
    export: "vnode*.localdomain(fsid=0,rw,async,no_root_squash,no_subtree_check,insecure)"

# Line to add to the /etc/fstab file
nfs_client_imports:
  - local: "/home"
    remote: "/home"
    server_host: "{{hostvars['server']['ansible_default_ipv4']}}"
```

NFS client imports can also define the following variables:
  * `state`: see: http://docs.ansible.com/ansible/mount_module.html for more information.
  * `opts`: see https://wiki.debian.org/fr/fstab for more information.
  * `dump`: see https://wiki.debian.org/fr/fstab for more information.
  * `passno`: see https://wiki.debian.org/fr/fstab for more information.


Example Playbook
----------------

This an example of how to install a Torque/PBS cluster:
```yaml
    - hosts: server
      roles:
      - { role: 'indigo-dc.nfs', nfs_mode: 'server', nfs_exports: [{path: "/home", export: "vnode*.localdomain(fsid=0,rw,async,no_root_squash,no_subtree_check,insecure)"}] }

    - hosts: client
      roles:
      - { role: 'indigo-dc.nfs', nfs_mode: 'client', nfs_client_imports: [{ local: "/home", remote: "/home", server_host: "{{hostvars['server']['ansible_default_ipv4']}}" }] }
```


Development
-----------

Using [molecule](https://molecule.readthedocs.io/en/latest/index.html) to test and develop the playbook.

Install it in virtualenv - run `pip install -r test-requirements.txt`. Then run `molecule test --all` to run throught the scenarios. 

There are three scenarios:

* `molecule test -s default` to use the default server only scenario on Vagrant/Virtualbox 
* `molecule test -s server_client_on_docker` to test server+client on Docker provisioned host
  * The host acts both as server and client, i.e. client is mounting localhost
* `molecule test -s server_and_client` to test server+client on Vagrant/Virtualbox 
  * The host acts both as server and client, i.e. client is mounting localhost


License
-------

Apache Licence v2 [1]

[1] http://www.apache.org/licenses/LICENSE-2.0
