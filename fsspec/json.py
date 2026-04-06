import json
from collections.abc import Callable, Mapping, Sequence
from contextlib import suppress
from pathlib import PurePath
from typing import Any, ClassVar

from .registry import _import_class, get_filesystem_class
from .spec import AbstractFileSystem


class FilesystemJSONEncoder(json.JSONEncoder):
    include_password: ClassVar[bool] = True

    def default(self, o: Any) -> Any:
        pass

    def make_serializable(self, obj: Any) -> Any:
        """
        Recursively converts an object so that it can be JSON serialized via
        :func:`json.dumps` and :func:`json.dump`, without actually calling
        said functions.
        """
        pass


class FilesystemJSONDecoder(json.JSONDecoder):
    def __init__(
        self,
        *,
        object_hook: Callable[[dict[str, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        strict: bool = True,
        object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None = None,
    ) -> None:
        self.original_object_hook = object_hook

        super().__init__(
            object_hook=self.custom_object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            strict=strict,
            object_pairs_hook=object_pairs_hook,
        )

    @classmethod
    def try_resolve_path_cls(cls, dct: dict[str, Any]):
        pass

    @classmethod
    def try_resolve_fs_cls(cls, dct: dict[str, Any]):
        pass

    def custom_object_hook(self, dct: dict[str, Any]):
        pass

    def unmake_serializable(self, obj: Any) -> Any:
        """
        Inverse function of :meth:`FilesystemJSONEncoder.make_serializable`.
        """
        pass
