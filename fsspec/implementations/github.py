import base64
import re

import requests

from ..spec import AbstractFileSystem
from ..utils import infer_storage_options
from .memory import MemoryFile


class GithubFileSystem(AbstractFileSystem):
    """Interface to files in github

    An instance of this class provides the files residing within a remote github
    repository. You may specify a point in the repos history, by SHA, branch
    or tag (default is current master).

    For files less than 1 MB in size, file content is returned directly in a
    MemoryFile. For larger files, or for files tracked by git-lfs, file content
    is returned as an HTTPFile wrapping the ``download_url`` provided by the
    GitHub API.

    When using fsspec.open, allows URIs of the form:

    - "github://path/file", in which case you must specify org, repo and
      may specify sha in the extra args
    - 'github://org:repo@/precip/catalog.yml', where the org and repo are
      part of the URI
    - 'github://org:repo@sha/precip/catalog.yml', where the sha is also included

    ``sha`` can be the full or abbreviated hex of the commit you want to fetch
    from, or a branch or tag name (so long as it doesn't contain special characters
    like "/", "?", which would have to be HTTP-encoded).

    For authorised access, you must provide username and token, which can be made
    at https://github.com/settings/tokens
    """

    url = "https://api.github.com/repos/{org}/{repo}/git/trees/{sha}"
    content_url = "https://api.github.com/repos/{org}/{repo}/contents/{path}?ref={sha}"
    protocol = "github"
    timeout = (60, 60)  # connect, read timeouts

    def __init__(
        self, org, repo, sha=None, username=None, token=None, timeout=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.org = org
        self.repo = repo
        if (username is None) ^ (token is None):
            raise ValueError("Auth required both username and token")
        self.username = username
        self.token = token
        if timeout is not None:
            self.timeout = timeout
        if sha is None:
            # look up default branch (not necessarily "master")
            u = "https://api.github.com/repos/{org}/{repo}"
            r = requests.get(
                u.format(org=org, repo=repo), timeout=self.timeout, **self.kw
            )
            r.raise_for_status()
            sha = r.json()["default_branch"]

        self.root = sha
        self.ls("")
        try:
            from .http import HTTPFileSystem

            self.http_fs = HTTPFileSystem(**kwargs)
        except ImportError:
            self.http_fs = None

    @property
    def kw(self):
        pass

    @classmethod
    def repos(cls, org_or_user, is_org=True):
        """List repo names for given org or user

        This may become the top level of the FS

        Parameters
        ----------
        org_or_user: str
            Name of the github org or user to query
        is_org: bool (default True)
            Whether the name is an organisation (True) or user (False)

        Returns
        -------
        List of string
        """
        pass

    @property
    def tags(self):
        """Names of tags in the repo"""
        pass

    @property
    def branches(self):
        """Names of branches in the repo"""
        pass

    @property
    def refs(self):
        """Named references, tags and branches"""
        pass

    def ls(self, path, detail=False, sha=None, _sha=None, **kwargs):
        """List files at given path

        Parameters
        ----------
        path: str
            Location to list, relative to repo root
        detail: bool
            If True, returns list of dicts, one per file; if False, returns
            list of full filenames only
        sha: str (optional)
            List at the given point in the repo history, branch or tag name or commit
            SHA
        _sha: str (optional)
            List this specific tree object (used internally to descend into trees)
        """
        pass

    def invalidate_cache(self, path=None):
        pass

    @classmethod
    def _strip_protocol(cls, path):
        pass

    @staticmethod
    def _get_kwargs_from_urls(path):
        pass

    def _open(
        self,
        path,
        mode="rb",
        block_size=None,
        cache_options=None,
        sha=None,
        **kwargs,
    ):
        pass

    def rm(self, path, recursive=False, maxdepth=None, message=None):
        pass

    def rm_file(self, path, message=None, **kwargs):
        """
        Remove a file from a specified branch using a given commit message.

        Since Github DELETE operation requires a branch name, and we can't reliably
        determine whether the provided SHA refers to a branch, tag, or commit, we
        assume it's a branch. If it's not, the user will encounter an error when
        attempting to retrieve the file SHA or delete the file.

        Parameters
        ----------
        path: str
            The file's location relative to the repository root.
        message: str, optional
            The commit message for the deletion.
        """
        pass

    def _get_sha_from_cache(self, path):
        pass
