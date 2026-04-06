import base64
import io
import re

import requests

import fsspec


class JupyterFileSystem(fsspec.AbstractFileSystem):
    """View of the files as seen by a Jupyter server (notebook or lab)"""

    protocol = ("jupyter", "jlab")

    def __init__(self, url, tok=None, **kwargs):
        """

        Parameters
        ----------
        url : str
            Base URL of the server, like "http://127.0.0.1:8888". May include
            token in the string, which is given by the process when starting up
        tok : str
            If the token is obtained separately, can be given here
        kwargs
        """
        if "?" in url:
            if tok is None:
                try:
                    tok = re.findall("token=([a-z0-9]+)", url)[0]
                except IndexError as e:
                    raise ValueError("Could not determine token") from e
            url = url.split("?", 1)[0]
        self.url = url.rstrip("/") + "/api/contents"
        self.session = requests.Session()
        if tok:
            self.session.headers["Authorization"] = f"token {tok}"

        super().__init__(**kwargs)

    def ls(self, path, detail=True, **kwargs):
        pass

    def cat_file(self, path, start=None, end=None, **kwargs):
        pass

    def pipe_file(self, path, value, **_):
        pass

    def mkdir(self, path, create_parents=True, **kwargs):
        pass

    def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
        pass

    def _rm(self, path):
        pass

    def _open(self, path, mode="rb", **kwargs):
        pass


class SimpleFileWriter(fsspec.spec.AbstractBufferedFile):
    def _upload_chunk(self, final=False):
        """Never uploads a chunk until file is done

        Not suitable for large files
        """
        pass
