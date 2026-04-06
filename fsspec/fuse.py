import argparse
import logging
import os
import stat
import threading
import time
from errno import EIO, ENOENT

from fuse import FUSE, FuseOSError, LoggingMixIn, Operations

from fsspec import __version__
from fsspec.core import url_to_fs

logger = logging.getLogger("fsspec.fuse")


class FUSEr(Operations):
    def __init__(self, fs, path, ready_file=False):
        self.fs = fs
        self.cache = {}
        self.root = path.rstrip("/") + "/"
        self.counter = 0
        logger.info("Starting FUSE at %s", path)
        self._ready_file = ready_file

    def getattr(self, path, fh=None):
        pass

    def readdir(self, path, fh):
        pass

    def mkdir(self, path, mode):
        pass

    def rmdir(self, path):
        pass

    def read(self, path, size, offset, fh):
        logger.debug("read %s", (path, size, offset))
        if self._ready_file and path in ["/.fuse_ready", ".fuse_ready"]:
            # status indicator
            return b"ready"

        f = self.cache[fh]
        f.seek(offset)
        out = f.read(size)
        return out

    def write(self, path, data, offset, fh):
        pass

    def create(self, path, flags, fi=None):
        pass

    def open(self, path, flags):
        pass

    def truncate(self, path, length, fh=None):
        pass

    def unlink(self, path):
        pass

    def release(self, path, fh):
        pass

    def chmod(self, path, mode):
        pass


def run(
    fs,
    path,
    mount_point,
    foreground=True,
    threads=False,
    ready_file=False,
    ops_class=FUSEr,
):
    """Mount stuff in a local directory

    This uses fusepy to make it appear as if a given path on an fsspec
    instance is in fact resident within the local file-system.

    This requires that fusepy by installed, and that FUSE be available on
    the system (typically requiring a package to be installed with
    apt, yum, brew, etc.).

    Parameters
    ----------
    fs: file-system instance
        From one of the compatible implementations
    path: str
        Location on that file-system to regard as the root directory to
        mount. Note that you typically should include the terminating "/"
        character.
    mount_point: str
        An empty directory on the local file-system where the contents of
        the remote path will appear.
    foreground: bool
        Whether or not calling this function will block. Operation will
        typically be more stable if True.
    threads: bool
        Whether or not to create threads when responding to file operations
        within the mounter directory. Operation will typically be more
        stable if False.
    ready_file: bool
        Whether the FUSE process is ready. The ``.fuse_ready`` file will
        exist in the ``mount_point`` directory if True. Debugging purpose.
    ops_class: FUSEr or Subclass of FUSEr
        To override the default behavior of FUSEr. For Example, logging
        to file.

    """
    pass


def main(args):
    """Mount filesystem from chained URL to MOUNT_POINT.

    Examples:

    python3 -m fsspec.fuse memory /usr/share /tmp/mem

    python3 -m fsspec.fuse local /tmp/source /tmp/local \\
            -l /tmp/fsspecfuse.log

    You can also mount chained-URLs and use special settings:

    python3 -m fsspec.fuse 'filecache::zip::file://data.zip' \\
            / /tmp/zip \\
            -o 'filecache-cache_storage=/tmp/simplecache'

    You can specify the type of the setting by using `[int]` or `[bool]`,
    (`true`, `yes`, `1` represents the Boolean value `True`):

    python3 -m fsspec.fuse 'simplecache::ftp://ftp1.at.proftpd.org' \\
            /historic/packages/RPMS /tmp/ftp \\
            -o 'simplecache-cache_storage=/tmp/simplecache' \\
            -o 'simplecache-check_files=false[bool]' \\
            -o 'ftp-listings_expiry_time=60[int]' \\
            -o 'ftp-username=anonymous' \\
            -o 'ftp-password=xieyanbo'
    """

    class RawDescriptionArgumentParser(argparse.ArgumentParser):
        def format_help(self):
            pass

    parser = RawDescriptionArgumentParser(prog="fsspec.fuse", description=main.__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("url", type=str, help="fs url")
    parser.add_argument("source_path", type=str, help="source directory in fs")
    parser.add_argument("mount_point", type=str, help="local directory")
    parser.add_argument(
        "-o",
        "--option",
        action="append",
        help="Any options of protocol included in the chained URL",
    )
    parser.add_argument(
        "-l", "--log-file", type=str, help="Logging FUSE debug info (Default: '')"
    )
    parser.add_argument(
        "-f",
        "--foreground",
        action="store_false",
        help="Running in foreground or not (Default: False)",
    )
    parser.add_argument(
        "-t",
        "--threads",
        action="store_false",
        help="Running with threads support (Default: False)",
    )
    parser.add_argument(
        "-r",
        "--ready-file",
        action="store_false",
        help="The `.fuse_ready` file will exist after FUSE is ready. "
        "(Debugging purpose, Default: False)",
    )
    args = parser.parse_args(args)

    kwargs = {}
    for item in args.option or []:
        key, sep, value = item.partition("=")
        if not sep:
            parser.error(message=f"Wrong option: {item!r}")
        val = value.lower()
        if val.endswith("[int]"):
            value = int(value[: -len("[int]")])
        elif val.endswith("[bool]"):
            value = val[: -len("[bool]")] in ["1", "yes", "true"]

        if "-" in key:
            fs_name, setting_name = key.split("-", 1)
            if fs_name in kwargs:
                kwargs[fs_name][setting_name] = value
            else:
                kwargs[fs_name] = {setting_name: value}
        else:
            kwargs[key] = value

    if args.log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            filename=args.log_file,
            format="%(asctime)s %(message)s",
        )

        class LoggingFUSEr(FUSEr, LoggingMixIn):
            pass

        fuser = LoggingFUSEr
    else:
        fuser = FUSEr

    fs, url_path = url_to_fs(args.url, **kwargs)
    logger.debug("Mounting %s to %s", url_path, str(args.mount_point))
    run(
        fs,
        args.source_path,
        args.mount_point,
        foreground=args.foreground,
        threads=args.threads,
        ready_file=args.ready_file,
        ops_class=fuser,
    )


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
