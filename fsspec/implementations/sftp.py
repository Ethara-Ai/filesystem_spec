import datetime
import logging
import os
import types
import uuid
from stat import S_ISDIR, S_ISLNK

import paramiko

from .. import AbstractFileSystem
from ..utils import infer_storage_options

logger = logging.getLogger("fsspec.sftp")


class SFTPFileSystem(AbstractFileSystem):
    """Files over SFTP/SSH

    Peer-to-peer filesystem over SSH using paramiko.

    Note: if using this with the ``open`` or ``open_files``, with full URLs,
    there is no way to tell if a path is relative, so all paths are assumed
    to be absolute.
    """

    protocol = "sftp", "ssh"

    def __init__(self, host, **ssh_kwargs):
        """

        Parameters
        ----------
        host: str
            Hostname or IP as a string
        temppath: str
            Location on the server to put files, when within a transaction
        ssh_kwargs: dict
            Parameters passed on to connection. See details in
            https://docs.paramiko.org/en/3.3/api/client.html#paramiko.client.SSHClient.connect
            May include port, username, password...
        """
        if self._cached:
            return
        super().__init__(**ssh_kwargs)
        self.temppath = ssh_kwargs.pop("temppath", "/tmp")  # remote temp directory
        self.host = host
        self.ssh_kwargs = ssh_kwargs
        self._connect()

    def _connect(self):
        pass

    @classmethod
    def _strip_protocol(cls, path):
        pass

    @staticmethod
    def _get_kwargs_from_urls(urlpath):
        pass

    def mkdir(self, path, create_parents=True, mode=511):
        pass

    def makedirs(self, path, exist_ok=False, mode=511):
        pass

    def rmdir(self, path):
        pass

    def info(self, path):
        pass

    @staticmethod
    def _decode_stat(stat, parent_path=None):
        pass

    def ls(self, path, detail=False):
        pass

    def put_file(self, lpath, rpath, callback=None, **kwargs):
        pass

    def get_file(self, rpath, lpath, **kwargs):
        pass

    def _open(self, path, mode="rb", block_size=None, **kwargs):
        """
        block_size: int or None
            If 0, no buffering, if 1, line buffering, if >1, buffer that many
            bytes, if None use default from paramiko.
        """
        pass

    def _rm(self, path):
        pass

    def mv(self, old, new):
        pass


def commit_a_file(self):
    pass


def discard_a_file(self):
    pass
