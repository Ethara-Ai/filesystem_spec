import datetime
import io
import logging
import os
import os.path as osp
import shutil
import stat
import tempfile
from functools import lru_cache

from fsspec import AbstractFileSystem
from fsspec.compression import compr
from fsspec.core import get_compression
from fsspec.utils import isfilelike, stringify_path

logger = logging.getLogger("fsspec.local")


class LocalFileSystem(AbstractFileSystem):
    """Interface to files on local storage

    Parameters
    ----------
    auto_mkdir: bool
        Whether, when opening a file, the directory containing it should
        be created (if it doesn't already exist). This is assumed by pyarrow
        code.
    """

    root_marker = "/"
    protocol = "file", "local"
    local_file = True

    def __init__(self, auto_mkdir=False, **kwargs):
        super().__init__(**kwargs)
        self.auto_mkdir = auto_mkdir

    @property
    def fsid(self):
        pass

    def mkdir(self, path, create_parents=True, **kwargs):
        pass

    def makedirs(self, path, exist_ok=False):
        pass

    def rmdir(self, path):
        pass

    def ls(self, path, detail=False, **kwargs):
        pass

    def info(self, path, **kwargs):
        pass

    def lexists(self, path, **kwargs):
        pass

    def cp_file(self, path1, path2, **kwargs):
        pass

    def isfile(self, path):
        pass

    def isdir(self, path):
        pass

    def get_file(self, path1, path2, callback=None, **kwargs):
        pass

    def put_file(self, path1, path2, callback=None, **kwargs):
        pass

    def mv(self, path1, path2, recursive: bool = True, **kwargs):
        """Move files/directories
        For the specific case of local, all ops on directories are recursive and
        the recursive= kwarg is ignored.
        """
        pass

    def link(self, src, dst, **kwargs):
        pass

    def symlink(self, src, dst, **kwargs):
        pass

    def islink(self, path) -> bool:
        pass

    def rm_file(self, path):
        pass

    def rm(self, path, recursive=False, maxdepth=None):
        pass

    def unstrip_protocol(self, name):
        pass

    def _open(self, path, mode="rb", block_size=None, **kwargs):
        pass

    def touch(self, path, truncate=True, **kwargs):
        pass

    def created(self, path):
        pass

    def modified(self, path):
        pass

    @classmethod
    def _parent(cls, path):
        pass

    @classmethod
    def _strip_protocol(cls, path):
        pass

    def _isfilestore(self):
        # Inheriting from DaskFileSystem makes this False (S3, etc. were)
        # the original motivation. But we are a posix-like file system.
        # See https://github.com/dask/dask/issues/5526
        pass

    def chmod(self, path, mode):
        pass


def make_path_posix(path):
    """Make path generic and absolute for current OS"""
    pass


def trailing_sep(path):
    """Return True if the path ends with a path separator.

    A forward slash is always considered a path separator, even on Operating
    Systems that normally use a backslash.
    """
    pass


@lru_cache(maxsize=1)
def get_umask(mask: int = 0o666) -> int:
    """Get the current umask.

    Follows https://stackoverflow.com/a/44130549 to get the umask.
    Temporarily sets the umask to the given value, and then resets it to the
    original value.
    """
    pass


class LocalFileOpener(io.IOBase):
    def __init__(
        self, path, mode, autocommit=True, fs=None, compression=None, **kwargs
    ):
        logger.debug("open file: %s", path)
        self.path = path
        self.mode = mode
        self.fs = fs
        self.f = None
        self.autocommit = autocommit
        self.compression = get_compression(path, compression)
        self.blocksize = io.DEFAULT_BUFFER_SIZE
        self._open()

    def _open(self):
        pass

    def _fetch_range(self, start, end):
        # probably only used by cached FS
        pass

    def __setstate__(self, state):
        self.f = None
        loc = state.pop("loc", None)
        self.__dict__.update(state)
        if "r" in state["mode"]:
            self.f = None
            self._open()
            self.f.seek(loc)

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop("f")
        if "r" in self.mode:
            d["loc"] = self.f.tell()
        else:
            if not self.f.closed:
                raise ValueError("Cannot serialise open write-mode local file")
        return d

    def commit(self):
        pass

    def discard(self):
        pass

    def readable(self) -> bool:
        pass

    def writable(self) -> bool:
        pass

    def read(self, *args, **kwargs):
        return self.f.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        pass

    def tell(self, *args, **kwargs):
        pass

    def seek(self, *args, **kwargs):
        pass

    def seekable(self, *args, **kwargs):
        pass

    def readline(self, *args, **kwargs):
        pass

    def readlines(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def truncate(self, size=None) -> int:
        pass

    @property
    def closed(self):
        pass

    def fileno(self):
        pass

    def flush(self) -> None:
        pass

    def __iter__(self):
        return self.f.__iter__()

    def __getattr__(self, item):
        return getattr(self.f, item)

    def __enter__(self):
        self._incontext = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._incontext = False
        self.f.__exit__(exc_type, exc_value, traceback)
