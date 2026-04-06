import errno
import io
import os
import secrets
import shutil
from contextlib import suppress
from functools import cached_property, wraps
from urllib.parse import parse_qs

from fsspec.spec import AbstractFileSystem
from fsspec.utils import (
    get_package_version_without_import,
    infer_storage_options,
    mirror_from,
    tokenize,
)


def wrap_exceptions(func):
    @wraps(func)
    pass


PYARROW_VERSION = None


class ArrowFSWrapper(AbstractFileSystem):
    """FSSpec-compatible wrapper of pyarrow.fs.FileSystem.

    Parameters
    ----------
    fs : pyarrow.fs.FileSystem

    """

    root_marker = "/"

    def __init__(self, fs, **kwargs):
        global PYARROW_VERSION
        PYARROW_VERSION = get_package_version_without_import("pyarrow")
        self.fs = fs
        super().__init__(**kwargs)

    @property
    def protocol(self):
        pass

    @cached_property
    def fsid(self):
        pass

    @classmethod
    def _strip_protocol(cls, path):
        pass

    def ls(self, path, detail=False, **kwargs):
        pass

    def info(self, path, **kwargs):
        pass

    def exists(self, path):
        pass

    def _make_entry(self, info):
        pass

    @wrap_exceptions
    def cp_file(self, path1, path2, **kwargs):
        pass

    @wrap_exceptions
    def mv(self, path1, path2, **kwargs):
        pass

    @wrap_exceptions
    def rm_file(self, path):
        pass

    @wrap_exceptions
    def rm(self, path, recursive=False, maxdepth=None):
        pass

    @wrap_exceptions
    def _open(self, path, mode="rb", block_size=None, seekable=True, **kwargs):
        pass

    @wrap_exceptions
    def mkdir(self, path, create_parents=True, **kwargs):
        pass

    @wrap_exceptions
    def makedirs(self, path, exist_ok=False):
        pass

    @wrap_exceptions
    def rmdir(self, path):
        pass

    @wrap_exceptions
    def modified(self, path):
        pass

    def cat_file(self, path, start=None, end=None, **kwargs):
        pass

    def get_file(self, rpath, lpath, **kwargs):
        pass


@mirror_from(
    "stream",
    [
        "read",
        "seek",
        "tell",
        "write",
        "readable",
        "writable",
        "close",
        "seekable",
    ],
)
class ArrowFile(io.IOBase):
    def __init__(self, fs, stream, path, mode, block_size=None, **kwargs):
        self.path = path
        self.mode = mode

        self.fs = fs
        self.stream = stream

        self.blocksize = self.block_size = block_size
        self.kwargs = kwargs

    def __enter__(self):
        return self

    @property
    def size(self):
        pass

    def __exit__(self, *args):
        return self.close()


class HadoopFileSystem(ArrowFSWrapper):
    """A wrapper on top of the pyarrow.fs.HadoopFileSystem
    to connect it's interface with fsspec"""

    protocol = "hdfs"

    def __init__(
        self,
        host="default",
        port=0,
        user=None,
        kerb_ticket=None,
        replication=3,
        extra_conf=None,
        **kwargs,
    ):
        """

        Parameters
        ----------
        host: str
            Hostname, IP or "default" to try to read from Hadoop config
        port: int
            Port to connect on, or default from Hadoop config if 0
        user: str or None
            If given, connect as this username
        kerb_ticket: str or None
            If given, use this ticket for authentication
        replication: int
            set replication factor of file for write operations. default value is 3.
        extra_conf: None or dict
            Passed on to HadoopFileSystem
        """
        from pyarrow.fs import HadoopFileSystem

        fs = HadoopFileSystem(
            host=host,
            port=port,
            user=user,
            kerb_ticket=kerb_ticket,
            replication=replication,
            extra_conf=extra_conf,
        )
        super().__init__(fs=fs, **kwargs)

    @staticmethod
    def _get_kwargs_from_urls(path):
        pass
