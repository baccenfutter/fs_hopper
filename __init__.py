from nodes import DirectoryNode as Directory
from nodes import FileNode as File

def get_root():
    import nodes
    return nodes.set_root

def set_root(base_root):
    import nodes
    nodes.set_root = base_root
