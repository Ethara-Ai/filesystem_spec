import base64
import io
from urllib.parse import unquote

from fsspec import AbstractFileSystem


class DataFileSystem(AbstractFileSystem):
    """A handy decoder for data-URLs

    Example
    -------
    >>> with fsspec.open("data:,Hello%2C%20World%21") as f:
    ...     print(f.read())
    b"Hello, World!"

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
    """

    protocol = "data"

    def __init__(self, **kwargs):
        """No parameters for this filesystem"""
        super().__init__(**kwargs)

    def cat_file(self, path, start=None, end=None, **kwargs):
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

    @staticmethod
    def encode(data: bytes, mime: str | None = None):
        """Format the given data into data-URL syntax

        This version always base64 encodes, even when the data is ascii/url-safe.
        """
        pass
