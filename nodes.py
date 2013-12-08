import os
import glob
import fnmatch

set_root = '/'


class BaseNode(object):
    def __new__(cls, name):
        if len(name) < len(set_root):
            raise IOError('%s is outside of base-root: %s' % (name, set_root))
        else:
            return object.__new__(cls, name)

    def __init__(self, name):
        if len(name) >= 2 and name.endswith('/'):
            name = name[:-1]
        self.name = name

    def __repr__(self):
        return self.name

    def exists(self):
        return os.path.exists(self.name)

    def get_parent(self):
        parent_dir = os.path.abspath(os.path.join(self.name, '..'))
        if len(parent_dir) < len(set_root):
            return self
        else:
            return DirectoryNode(parent_dir)

    def is_dir(self):
        return os.path.isdir(self.name)

    def is_file(self):
        return os.path.isfile(self.name)


class FileNode(BaseNode):
    def get_content(self, binary=False):
        output = ''
        if binary:
            open_as = 'rb'
        else:
            open_as = 'r'
        fd = open(self.name, open_as)
        lines = fd.readlines()
        fd.close()
        for line in lines:
            output += line
        return output

    def set_content(self, content, binary=False, force_sync=False):
        if binary:
            open_as = 'wb'
        else:
            open_as = 'w'
        fd = open(self.name, open_as)
        fd.write(content)
        if force_sync:
            fd.flush()
        fd.close()

    def create(self):
        fd = open(self.name, 'a')
        fd.close()


class DirectoryNode(BaseNode):
    def get_childs(self, pattern='*'):
        output = []
        for basename in glob.glob(os.path.join(self.name, pattern)):
            f = os.path.join(self.name, basename)
            if os.path.isdir(f):
                output.append(DirectoryNode(f))
            else:
                output.append(FileNode(f))
        return output

    def get_subs(self, pattern='*'):
        output = []
        for root, dirs, files in os.walk(self.name):
            for d in fnmatch.filter(dirs, pattern):
                output.append(DirectoryNode(os.path.join(root, d)))
            for f in fnmatch.filter(files, pattern):
                output.append(FileNode(os.path.join(root, f)))
        return output

    def mkdir(self):
        os.mkdir(self.name)

    def add_dir(self, name):
        if not name.startswith(self.name):
            name = os.path.join(self.name, name)
        child = DirectoryNode(name)
        child.mkdir()
        return child

    def add_file(self, name):
        if not name.startswith(self.name):
            name = os.path.join(self.name, name)
        child = FileNode(name)
        child.create()
        return child
