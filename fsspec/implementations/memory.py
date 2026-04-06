from __future__ import annotations

import logging
from datetime import datetime, timezone
from errno import ENOTEMPTY
from io import BytesIO
from pathlib import PurePath, PureWindowsPath
from typing import Any, ClassVar

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from fsspec.utils import stringify_path

logger = logging.getLogger("fsspec.memoryfs")


class MemoryFileSystem(AbstractFileSystem):
    """A filesystem based on a dict of BytesIO objects

    This is a global filesystem so instances of this class all point to the same
    in memory filesystem.
    """

    store: ClassVar[dict[str, Any]] = {}  # global, do not overwrite!
    pseudo_dirs = [""]  # global, do not overwrite!
    protocol = "memory"
    root_marker = "/"

    @classmethod
    def _strip_protocol(cls, path):
        pass

    def ls(self, path, detail=True, **kwargs):
        pass

    def mkdir(self, path, create_parents=True, **kwargs):
        pass

    def makedirs(self, path, exist_ok=False):
        pass

    def pipe_file(self, path, value, mode="overwrite", **kwargs):
        """Set the bytes of given file

        Avoids copies of the data if possible
        """
        pass

    def rmdir(self, path):
        pass

    def info(self, path, **kwargs):
        pass

    def _open(
        self,
        path,
        mode="rb",
        block_size=None,
        autocommit=True,
        cache_options=None,
        **kwargs,
    ):
        pass

    def cp_file(self, path1, path2, **kwargs):
        pass

    def cat_file(self, path, start=None, end=None, **kwargs):
        pass

    def _rm(self, path):
        pass

    def modified(self, path):
        pass

    def created(self, path):
        pass

    def isfile(self, path):
        pass

    def rm(self, path, recursive=False, maxdepth=None):
        pass


class MemoryFile(BytesIO):
    """A BytesIO which can't close and works as a context manager

    Can initialise with data. Each path should only be active once at any moment.

    No need to provide fs, path if auto-committing (default)
    """

    def __init__(self, fs=None, path=None, data=None):
        logger.debug("open file %s", path)
        self.fs = fs
        self.path = path
        self.created = datetime.now(tz=timezone.utc)
        self.modified = datetime.now(tz=timezone.utc)
        if data:
            super().__init__(data)
            self.seek(0)

    @property
    def size(self):
        pass

    def __enter__(self):
        return self

    def close(self):
        pass

    def discard(self):
        pass

    def commit(self):
        pass
