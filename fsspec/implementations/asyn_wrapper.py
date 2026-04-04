import asyncio
import functools
import inspect

import fsspec
from fsspec.asyn import AsyncFileSystem, running_async

from .chained import ChainedFileSystem


def async_wrapper(func, obj=None, semaphore=None):
    """
    Wraps a synchronous function to make it awaitable.

    Parameters
    ----------
    func : callable
        The synchronous function to wrap.
    obj : object, optional
        The instance to bind the function to, if applicable.
    semaphore : asyncio.Semaphore, optional
        A semaphore to limit concurrent calls.

    Returns
    -------
    coroutine
        An awaitable version of the function.
    """
    pass


class AsyncFileSystemWrapper(AsyncFileSystem, ChainedFileSystem):
    """
    A wrapper class to convert a synchronous filesystem into an asynchronous one.

    This class takes an existing synchronous filesystem implementation and wraps all
    its methods to provide an asynchronous interface.

    Parameters
    ----------
    sync_fs : AbstractFileSystem
        The synchronous filesystem instance to wrap.
    """

    protocol = "asyncwrapper", "async_wrapper"
    cachable = False

    def __init__(
        self,
        fs=None,
        asynchronous=None,
        target_protocol=None,
        target_options=None,
        semaphore=None,
        max_concurrent_tasks=None,
        **kwargs,
    ):
        if asynchronous is None:
            asynchronous = running_async()
        super().__init__(asynchronous=asynchronous, **kwargs)
        if fs is not None:
            self.sync_fs = fs
        else:
            self.sync_fs = fsspec.filesystem(target_protocol, **target_options)
        self.protocol = self.sync_fs.protocol
        self.semaphore = semaphore
        self._wrap_all_sync_methods()


    def _wrap_all_sync_methods(self):
        """
        Wrap all synchronous methods of the underlying filesystem with asynchronous versions.
        """
        pass

    @classmethod
    def wrap_class(cls, sync_fs_class):
        """
        Create a new class that can be used to instantiate an AsyncFileSystemWrapper
        with lazy instantiation of the underlying synchronous filesystem.

        Parameters
        ----------
        sync_fs_class : type
            The class of the synchronous filesystem to wrap.

        Returns
        -------
        type
            A new class that wraps the provided synchronous filesystem class.
        """
        pass
