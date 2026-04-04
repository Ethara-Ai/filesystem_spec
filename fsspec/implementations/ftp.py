import os
import ssl
import uuid
from ftplib import FTP, FTP_TLS, Error, error_perm
from typing import Any

from ..spec import AbstractBufferedFile, AbstractFileSystem
from ..utils import infer_storage_options, isfilelike

SECURITY_PROTOCOL_MAP = {
    "tls": ssl.PROTOCOL_TLS,
    "tlsv1": ssl.PROTOCOL_TLSv1,
    "tlsv1_1": ssl.PROTOCOL_TLSv1_1,
    "tlsv1_2": ssl.PROTOCOL_TLSv1_2,
    "sslv23": ssl.PROTOCOL_SSLv23,
}


class ImplicitFTPTLS(FTP_TLS):
    """
    FTP_TLS subclass that automatically wraps sockets in SSL
    to support implicit FTPS.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        pass

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        pass


class FTPFileSystem(AbstractFileSystem):
    """A filesystem over classic FTP"""

    root_marker = "/"
    cachable = False
    protocol = "ftp"

    def __init__(
        self,
        host,
        port=21,
        username=None,
        password=None,
        acct=None,
        block_size=None,
        tempdir=None,
        timeout=30,
        encoding="utf-8",
        tls=False,
        **kwargs,
    ):
        """
        You can use _get_kwargs_from_urls to get some kwargs from
        a reasonable FTP url.

        Authentication will be anonymous if username/password are not
        given.

        Parameters
        ----------
        host: str
            The remote server name/ip to connect to
        port: int
            Port to connect with
        username: str or None
            If authenticating, the user's identifier
        password: str of None
            User's password on the server, if using
        acct: str or None
            Some servers also need an "account" string for auth
        block_size: int or None
            If given, the read-ahead or write buffer size.
        tempdir: str
            Directory on remote to put temporary files when in a transaction
        timeout: int
            Timeout of the ftp connection in seconds
        encoding: str
            Encoding to use for directories and filenames in FTP connection
        tls: bool or str
            Enable FTP-TLS for secure connections:
                - False: Plain FTP (default)
                - True: Explicit TLS (FTPS with AUTH TLS command)
                - "tls": Auto-negotiate highest protocol
                - "tlsv1": TLS v1.0
                - "tlsv1_1": TLS v1.1
                - "tlsv1_2": TLS v1.2
        """
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.tempdir = tempdir or "/tmp"
        self.cred = username or "", password or "", acct or ""
        self.timeout = timeout
        self.encoding = encoding
        if block_size is not None:
            self.blocksize = block_size
        else:
            self.blocksize = 2**16
        self.tls = tls
        self._connect()
        if isinstance(self.tls, bool) and self.tls:
            self.ftp.prot_p()















    def __del__(self):
        self.ftp.close()



class TransferDone(Exception):
    """Internal exception to break out of transfer"""

    pass


class FTPFile(AbstractBufferedFile):
    """Interact with a remote FTP file with read/write buffering"""

    def __init__(
        self,
        fs,
        path,
        mode="rb",
        block_size="default",
        autocommit=True,
        cache_type="readahead",
        cache_options=None,
        **kwargs,
    ):
        super().__init__(
            fs,
            path,
            mode=mode,
            block_size=block_size,
            autocommit=autocommit,
            cache_type=cache_type,
            cache_options=cache_options,
            **kwargs,
        )
        if not autocommit:
            self.target = self.path
            self.path = "/".join([kwargs["tempdir"], str(uuid.uuid4())])



    def _fetch_range(self, start, end):
        """Get bytes between given byte limits

        Implemented by raising an exception in the fetch callback when the
        number of bytes received reaches the requested amount.

        Will fail if the server does not respect the REST command on
        retrieve requests.
        """
        pass



def _mlsd2(ftp, path="."):
    """
    Fall back to using `dir` instead of `mlsd` if not supported.

    This parses a Linux style `ls -l` response to `dir`, but the response may
    be platform dependent.

    Parameters
    ----------
    ftp: ftplib.FTP
    path: str
        Expects to be given path, but defaults to ".".
    """
    pass
