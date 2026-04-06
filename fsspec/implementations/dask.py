import dask
from distributed.client import Client, _get_global_client
from distributed.worker import Worker

from fsspec import filesystem
from fsspec.spec import AbstractBufferedFile, AbstractFileSystem
from fsspec.utils import infer_storage_options


def _get_client(client):
    pass


def _in_worker():
    pass


class DaskWorkerFileSystem(AbstractFileSystem):
    """View files accessible to a worker as any other remote file-system

    When instances are run on the worker, uses the real filesystem. When
    run on the client, they call the worker to provide information or data.

    **Warning** this implementation is experimental, and read-only for now.
    """

    def __init__(
        self, target_protocol=None, target_options=None, fs=None, client=None, **kwargs
    ):
        super().__init__(**kwargs)
        if not (fs is None) ^ (target_protocol is None):
            raise ValueError(
                "Please provide one of filesystem instance (fs) or"
                " target_protocol, not both"
            )
        self.target_protocol = target_protocol
        self.target_options = target_options
        self.worker = None
        self.client = client
        self.fs = fs
        self._determine_worker()

    @staticmethod
    def _get_kwargs_from_urls(path):
        pass

    def _determine_worker(self):
        pass

    def mkdir(self, *args, **kwargs):
        pass

    def rm(self, *args, **kwargs):
        pass

    def copy(self, *args, **kwargs):
        pass

    def mv(self, *args, **kwargs):
        pass

    def ls(self, *args, **kwargs):
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

    def fetch_range(self, path, mode, start, end):
        pass


class DaskFile(AbstractBufferedFile):
    def __init__(self, mode="rb", **kwargs):
        if mode != "rb":
            raise ValueError('Remote dask files can only be opened in "rb" mode')
        super().__init__(**kwargs)

    def _upload_chunk(self, final=False):
        pass

    def _initiate_upload(self):
        """Create remote file/upload"""
        pass

    def _fetch_range(self, start, end):
        """Get the specified set of bytes from remote"""
        pass
