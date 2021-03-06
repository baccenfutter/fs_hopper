=========
FS-Hopper
=========

FS-Hopper is a simplistic and very thin abstraction layer for
accessing a filesystem directory tree in an object-oriented style.
The only two known filesystem nodes are directories and trees. Both
are implemented as new-style classes. Each method call to them (e.g.
DirectoryNode.get_childs()) will return instances of either
DirectoryNode or FileNode, allowing easy traversal throughout the
tree.

Additionally, you can define a set_root, similar to (but not really)
GNU/chroot. It is prohibited to create Nodes above set_root making it
easy for you to jail your code into a certain directory within the
filesystem.

=====
Usage
=====

Jail code into /tmp and create a working directory:

    #!/usr/bin/env python2

    import fs_hopper
    fs_hopper.set_root('/tmp')

    workdir = fs_hopper.Directory('/tmp/fs_hopper')
    workdir.mkdir()
    print workdir

Recursively get all configuration files of some_app

    #!/usr/bin/env python2

    import os
    import fs_hopper

    name = os.path.expanduser('~/.config/some_app')
    confdir = fs_hopper.Directory(name)
    confs = confdir.get_subs('*.conf')
    print confs

Read /etc/passwd

    #!/usr/bin/env python2

    import fs_hopper

    passwd = fs_hopper.File('/etc/passwd')
    print passwd.get_content()

=========
Resources
=========

- Github: https://gihub.com/baccenfutter/fs_hopper/
- PyPi  : https://pypi.python.org/pypi/FS-Hopper/
