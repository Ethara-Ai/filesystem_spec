from .. import filesystem
from ..asyn import AsyncFileSystem
from .chained import ChainedFileSystem


class DirFileSystem(AsyncFileSystem, ChainedFileSystem):
    """Directory prefix filesystem

    The DirFileSystem is a filesystem-wrapper. It assumes every path it is dealing with
    is relative to the `path`. After performing the necessary paths operation it
    delegates everything to the wrapped filesystem.
    """

    protocol = "dir"

    def __init__(
        self,
        path=None,
        fs=None,
        fo=None,
        target_protocol=None,
        target_options=None,
        **storage_options,
    ):
        """
        Parameters
        ----------
        path: str
            Path to the directory.
        fs: AbstractFileSystem
            An instantiated filesystem to wrap.
        target_protocol, target_options:
            if fs is none, construct it from these
        fo: str
            Alternate for path; do not provide both
        """
        super().__init__(**storage_options)
        if fs is None:
            fs = filesystem(protocol=target_protocol, **(target_options or {}))
        path = path or fo

        if self.asynchronous and not fs.async_impl:
            raise ValueError("can't use asynchronous with non-async fs")

        if fs.async_impl and self.asynchronous != fs.asynchronous:
            raise ValueError("both dirfs and fs should be in the same sync/async mode")

        self.path = fs._strip_protocol(path)
        self.fs = fs

    def _join(self, path):
        pass

    def _relpath(self, path):
        pass

    # Wrappers below

    @property
    def sep(self):
        pass

    async def set_session(self, *args, **kwargs):
        pass

    async def _rm_file(self, path, **kwargs):
        pass

    def rm_file(self, path, **kwargs):
        pass

    async def _rm(self, path, *args, **kwargs):
        pass

    def rm(self, path, *args, **kwargs):
        pass

    async def _cp_file(self, path1, path2, **kwargs):
        pass

    def cp_file(self, path1, path2, **kwargs):
        pass

    async def _copy(
        self,
        path1,
        path2,
        *args,
        **kwargs,
    ):
        pass

    def copy(self, path1, path2, *args, **kwargs):
        pass

    async def _pipe(self, path, *args, **kwargs):
        pass

    def pipe(self, path, *args, **kwargs):
        pass

    async def _pipe_file(self, path, *args, **kwargs):
        pass

    def pipe_file(self, path, *args, **kwargs):
        pass

    async def _cat_file(self, path, *args, **kwargs):
        pass

    def cat_file(self, path, *args, **kwargs):
        pass

    async def _cat(self, path, *args, **kwargs):
        pass

    def cat(self, path, *args, **kwargs):
        pass

    async def _put_file(self, lpath, rpath, **kwargs):
        pass

    def put_file(self, lpath, rpath, **kwargs):
        pass

    async def _put(
        self,
        lpath,
        rpath,
        *args,
        **kwargs,
    ):
        pass

    def put(self, lpath, rpath, *args, **kwargs):
        pass

    async def _get_file(self, rpath, lpath, **kwargs):
        pass

    def get_file(self, rpath, lpath, **kwargs):
        pass

    async def _get(self, rpath, *args, **kwargs):
        pass

    def get(self, rpath, *args, **kwargs):
        return self.fs.get(self._join(rpath), *args, **kwargs)

    async def _isfile(self, path):
        pass

    def isfile(self, path):
        pass

    async def _isdir(self, path):
        pass

    def isdir(self, path):
        pass

    async def _size(self, path):
        pass

    def size(self, path):
        pass

    async def _exists(self, path):
        pass

    def exists(self, path):
        pass

    async def _info(self, path, **kwargs):
        pass

    def info(self, path, **kwargs):
        pass

    async def _ls(self, path, detail=True, **kwargs):
        pass

    def ls(self, path, detail=True, **kwargs):
        pass

    async def _walk(self, path, *args, **kwargs):
        pass

    def walk(self, path, *args, **kwargs):
        pass

    async def _glob(self, path, **kwargs):
        pass

    def glob(self, path, **kwargs):
        pass

    async def _du(self, path, *args, **kwargs):
        pass

    def du(self, path, *args, **kwargs):
        pass

    async def _find(self, path, *args, **kwargs):
        pass

    def find(self, path, *args, **kwargs):
        pass

    async def _expand_path(self, path, *args, **kwargs):
        pass

    def expand_path(self, path, *args, **kwargs):
        pass

    async def _mkdir(self, path, *args, **kwargs):
        pass

    def mkdir(self, path, *args, **kwargs):
        pass

    async def _makedirs(self, path, *args, **kwargs):
        pass

    def makedirs(self, path, *args, **kwargs):
        pass

    def rmdir(self, path):
        pass

    def mv(self, path1, path2, **kwargs):
        pass

    def touch(self, path, **kwargs):
        pass

    def created(self, path):
        pass

    def modified(self, path):
        pass

    def sign(self, path, *args, **kwargs):
        pass

    def __repr__(self):
        return f"{self.__class__.__qualname__}(path='{self.path}', fs={self.fs})"

    def open(
        self,
        path,
        *args,
        **kwargs,
    ):
        pass

    async def open_async(
        self,
        path,
        *args,
        **kwargs,
    ):
        pass
