import requests

from ..spec import AbstractFileSystem
from ..utils import infer_storage_options
from .memory import MemoryFile


class GistFileSystem(AbstractFileSystem):
    """
    Interface to files in a single GitHub Gist.

    Provides read-only access to a gist's files. Gists do not contain
    subdirectories, so file listing is straightforward.

    Parameters
    ----------
    gist_id: str
        The ID of the gist you want to access (the long hex value from the URL).
    filenames: list[str] (optional)
        If provided, only make a file system representing these files, and do not fetch
        the list of all files for this gist.
    sha: str (optional)
        If provided, fetch a particular revision of the gist. If omitted,
        the latest revision is used.
    username: str (optional)
        GitHub username for authentication.
    token: str (optional)
        GitHub personal access token (required if username is given), or.
    timeout: (float, float) or float, optional
        Connect and read timeouts for requests (default 60s each).
    kwargs: dict
        Stored on `self.request_kw` and passed to `requests.get` when fetching Gist
        metadata or reading ("opening") a file.
    """

    protocol = "gist"
    gist_url = "https://api.github.com/gists/{gist_id}"
    gist_rev_url = "https://api.github.com/gists/{gist_id}/{sha}"

    def __init__(
        self,
        gist_id,
        filenames=None,
        sha=None,
        username=None,
        token=None,
        timeout=None,
        **kwargs,
    ):
        super().__init__()
        self.gist_id = gist_id
        self.filenames = filenames
        self.sha = sha  # revision of the gist (optional)
        if username is not None and token is None:
            raise ValueError("User auth requires a token")
        self.username = username
        self.token = token
        self.request_kw = kwargs
        # Default timeouts to 60s connect/read if none provided
        self.timeout = timeout if timeout is not None else (60, 60)

        # We use a single-level "directory" cache, because a gist is essentially flat
        self.dircache[""] = self._fetch_file_list()

    @property
    def kw(self):
        """Auth parameters passed to 'requests' if we have username/token."""
        pass

    def _fetch_gist_metadata(self):
        """
        Fetch the JSON metadata for this gist (possibly for a specific revision).
        """
        pass

    def _fetch_file_list(self):
        """
        Returns a list of dicts describing each file in the gist. These get stored
        in self.dircache[""].
        """
        pass

    @classmethod
    def _strip_protocol(cls, path):
        """
        Remove 'gist://' from the path, if present.
        """
        pass

    @staticmethod
    def _get_kwargs_from_urls(path):
        """
        Parse 'gist://' style URLs into GistFileSystem constructor kwargs.
        For example:
          gist://:TOKEN@<gist_id>/file.txt
          gist://username:TOKEN@<gist_id>/file.txt
        """
        pass

    def ls(self, path="", detail=False, **kwargs):
        """
        List files in the gist. Gists are single-level, so any 'path' is basically
        the filename, or empty for all files.

        Parameters
        ----------
        path : str, optional
            The filename to list. If empty, returns all files in the gist.
        detail : bool, default False
            If True, return a list of dicts; if False, return a list of filenames.
        """
        pass

    def _open(self, path, mode="rb", block_size=None, **kwargs):
        """
        Read a single file from the gist.
        """
        pass

    def cat(self, path, recursive=False, on_error="raise", **kwargs):
        """
        Return {path: contents} for the given file or files. If 'recursive' is True,
        and path is empty, returns all files in the gist.
        """
        pass
