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



    # Wrappers below


























    def get(self, rpath, *args, **kwargs):
        return self.fs.get(self._join(rpath), *args, **kwargs)

































    def __repr__(self):
        return f"{self.__class__.__qualname__}(path='{self.path}', fs={self.fs})"


