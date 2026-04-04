"""This file is largely copied from http.py"""

import io
import logging
import re
import urllib.error
import urllib.parse
from copy import copy
from json import dumps, loads
from urllib.parse import urlparse

try:
    import yarl
except (ImportError, ModuleNotFoundError, OSError):
    yarl = False

from fsspec.callbacks import _DEFAULT_CALLBACK
from fsspec.registry import register_implementation
from fsspec.spec import AbstractBufferedFile, AbstractFileSystem
from fsspec.utils import DEFAULT_BLOCK_SIZE, isfilelike, nullcontext, tokenize

from ..caching import AllBytes

# https://stackoverflow.com/a/15926317/3821154
ex = re.compile(r"""<(a|A)\s+(?:[^>]*?\s+)?(href|HREF)=["'](?P<url>[^"']+)""")
ex2 = re.compile(r"""(?P<url>http[s]?://[-a-zA-Z0-9@:%_+.~#?&/=]+)""")
logger = logging.getLogger("fsspec.http")


class JsHttpException(urllib.error.HTTPError): ...


class StreamIO(io.BytesIO):
    # fake class, so you can set attributes on it
    # will eventually actually stream
    ...


class ResponseProxy:
    """Looks like a requests response"""

    def __init__(self, req, stream=False):
        self.request = req
        self.stream = stream
        self._data = None
        self._headers = None














class RequestsSessionShim:
    def __init__(self):
        self.headers = {}


    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)







class HTTPFileSystem(AbstractFileSystem):
    """
    Simple File-System for fetching data via HTTP(S)

    This is the BLOCKING version of the normal HTTPFileSystem. It uses
    requests in normal python and the JS runtime in pyodide.

    ***This implementation is extremely experimental, do not use unless
    you are testing pyodide/pyscript integration***
    """

    protocol = ("http", "https", "sync-http", "sync-https")
    sep = "/"

    def __init__(
        self,
        simple_links=True,
        block_size=None,
        same_scheme=True,
        cache_type="readahead",
        cache_options=None,
        client_kwargs=None,
        encoded=False,
        **storage_options,
    ):
        """

        Parameters
        ----------
        block_size: int
            Blocks to read bytes; if 0, will default to raw requests file-like
            objects instead of HTTPFile instances
        simple_links: bool
            If True, will consider both HTML <a> tags and anything that looks
            like a URL; if False, will consider only the former.
        same_scheme: True
            When doing ls/glob, if this is True, only consider paths that have
            http/https matching the input URLs.
        size_policy: this argument is deprecated
        client_kwargs: dict
            Passed to aiohttp.ClientSession, see
            https://docs.aiohttp.org/en/stable/client_reference.html
            For example, ``{'auth': aiohttp.BasicAuth('user', 'pass')}``
        storage_options: key-value
            Any other parameters passed on to requests
        cache_type, cache_options: defaults used in open
        """
        super().__init__(self, **storage_options)
        self.block_size = block_size if block_size is not None else DEFAULT_BLOCK_SIZE
        self.simple_links = simple_links
        self.same_schema = same_scheme
        self.cache_type = cache_type
        self.cache_options = cache_options
        self.client_kwargs = client_kwargs or {}
        self.encoded = encoded
        self.kwargs = storage_options

        try:
            import js  # noqa: F401

            logger.debug("Starting JS session")
            self.session = RequestsSessionShim()
            self.js = True
        except Exception as e:
            import requests

            logger.debug("Starting cpython session because of: %s", e)
            self.session = requests.Session(**(client_kwargs or {}))
            self.js = False

        request_options = copy(storage_options)
        self.use_listings_cache = request_options.pop("use_listings_cache", False)
        request_options.pop("listings_expiry_time", None)
        request_options.pop("max_paths", None)
        request_options.pop("skip_instance_cache", None)
        self.kwargs = request_options



    @classmethod
    def _strip_protocol(cls, path: str) -> str:
        """For HTTP, we always want to keep the full URL"""
        pass




    def _raise_not_found_for_status(self, response, url):
        """
        Raises FileNotFoundError for 404s, otherwise uses raise_for_status.
        """
        pass




    def _process_limits(self, url, start, end):
        """Helper for "Range"-based _cat_file"""
        pass



    def _open(
        self,
        path,
        mode="rb",
        block_size=None,
        autocommit=None,  # XXX: This differs from the base class.
        cache_type=None,
        cache_options=None,
        size=None,
        **kwargs,
    ):
        """Make a file-like object

        Parameters
        ----------
        path: str
            Full URL with protocol
        mode: string
            must be "rb"
        block_size: int or None
            Bytes to download in one request; use instance value if None. If
            zero, will return a streaming Requests file-like instance.
        kwargs: key-value
            Any other parameters, passed to requests calls
        """
        pass

    def ukey(self, url):
        """Unique identifier; assume HTTP files are static, unchanging"""
        pass

    def info(self, url, **kwargs):
        """Get info of URL

        Tries to access location via HEAD, and then GET methods, but does
        not fetch the data.

        It is possible that the server does not supply any size information, in
        which case size will be given as None (and certain operations on the
        corresponding file will not work).
        """
        pass

    def glob(self, path, maxdepth=None, **kwargs):
        """
        Find files by glob-matching.

        This implementation is idntical to the one in AbstractFileSystem,
        but "?" is not considered as a character for globbing, because it is
        so common in URLs, often identifying the "query" part.
        """
        pass



class HTTPFile(AbstractBufferedFile):
    """
    A file-like object pointing to a remove HTTP(S) resource

    Supports only reading, with read-ahead of a predermined block-size.

    In the case that the server does not supply the filesize, only reading of
    the complete file in one go is supported.

    Parameters
    ----------
    url: str
        Full URL of the remote resource, including the protocol
    session: requests.Session or None
        All calls will be made within this session, to avoid restarting
        connections where the server allows this
    block_size: int or None
        The amount of read-ahead to do, in bytes. Default is 5MB, or the value
        configured for the FileSystem creating this file
    size: None or int
        If given, this is the size of the file in bytes, and we don't attempt
        to call the server to find the value.
    kwargs: all other key-values are passed to requests calls.
    """

    def __init__(
        self,
        fs,
        url,
        session=None,
        block_size=None,
        mode="rb",
        cache_type="bytes",
        cache_options=None,
        size=None,
        **kwargs,
    ):
        if mode != "rb":
            raise NotImplementedError("File mode not supported")
        self.url = url
        self.session = session
        self.details = {"name": url, "size": size, "type": "file"}
        super().__init__(
            fs=fs,
            path=url,
            mode=mode,
            block_size=block_size,
            cache_type=cache_type,
            cache_options=cache_options,
            **kwargs,
        )

    def read(self, length=-1):
        """Read bytes from file

        Parameters
        ----------
        length: int
            Read up to this many bytes. If negative, read all content to end of
            file. If the server has not supplied the filesize, attempting to
            read only part of the data will raise a ValueError.
        """
        if (
            (length < 0 and self.loc == 0)  # explicit read all
            # but not when the size is known and fits into a block anyways
            and not (self.size is not None and self.size <= self.blocksize)
        ):
            self._fetch_all()
        if self.size is None:
            if length < 0:
                self._fetch_all()
        else:
            length = min(self.size - self.loc, length)
        return super().read(length)

    def _fetch_all(self):
        """Read whole file in one shot, without caching

        This is only called when position is still at zero,
        and read() is called without a byte-count.
        """
        pass

    def _parse_content_range(self, headers):
        """Parse the Content-Range header"""
        pass

    def _fetch_range(self, start, end):
        """Download a block of data

        The expectation is that the server returns only the requested bytes,
        with HTTP code 206. If this is not the case, we first check the headers,
        and then stream the output - if the data size is bigger than we
        requested, an exception is raised.
        """
        pass


magic_check = re.compile("([*[])")




class HTTPStreamFile(AbstractBufferedFile):
    def __init__(self, fs, url, mode="rb", session=None, **kwargs):
        self.url = url
        self.session = session
        if mode != "rb":
            raise ValueError
        self.details = {"name": url, "size": None}
        super().__init__(fs=fs, path=url, mode=mode, cache_type="readahead", **kwargs)

        r = self.session.get(self.fs.encode_url(url), stream=True, **kwargs)
        self.fs._raise_not_found_for_status(r, url)
        self.it = r.iter_content(1024, False)
        self.leftover = b""

        self.r = r

    def seek(self, *args, **kwargs):
        raise ValueError("Cannot seek streaming HTTP file")

    def read(self, num=-1):
        bufs = [self.leftover]
        leng = len(self.leftover)
        while leng < num or num < 0:
            try:
                out = self.it.__next__()
            except StopIteration:
                break
            if out:
                bufs.append(out)
            else:
                break
            leng += len(out)
        out = b"".join(bufs)
        if num >= 0:
            self.leftover = out[num:]
            out = out[:num]
        else:
            self.leftover = b""
        self.loc += len(out)
        return out





def _file_info(url, session, size_policy="head", **kwargs):
    """Call HEAD on the server to get details about the file (size/checksum etc.)

    Default operation is to explicitly allow redirects and use encoding
    'identity' (no compression) to get the true size of the target.
    """
    pass


# importing this is enough to register it
def register():
    register_implementation("http", HTTPFileSystem, clobber=True)
    register_implementation("https", HTTPFileSystem, clobber=True)
    register_implementation("sync-http", HTTPFileSystem, clobber=True)
    register_implementation("sync-https", HTTPFileSystem, clobber=True)


register()


