import typing
import urllib.request
import urllib.error
import abc

from ..protocol import StdExtSession
from ..misc import URI, singleton
from ..errors import ReadOnlyPath, InvalidPath
from ..interfaces import ExtSessionT, IMyrrhExt, IExtSession, uri_rd

from .registry import Registry


class IExtRegistrySession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def findall(self, prefix: str | None = None): ...

    @uri_rd
    @abc.abstractmethod
    def loaded(self): ...


@singleton
class ExtRegistrySession(StdExtSession, IExtRegistrySession, typing.Generic[ExtSessionT]):

    def __init__(self):
        super().__init__(interface=IExtRegistrySession)

    def findall(self, prefix: str | None = None):
        return Registry().findall(prefix=prefix)

    def loaded(self):
        return list(Registry().loaded)


class ExtRegistry(IMyrrhExt[ExtRegistrySession]):

    _path = "."

    def open(self, uri: str, *, req: urllib.request.Request | None = None) -> ExtRegistrySession:

        if str(URI(uri).path) != self._path:
            raise InvalidPath(URI(uri).path)

        return ExtRegistrySession()

    def basepath(self, path: str):
        self._path = path

    def extend(self, path: str, obj: typing.Any):
        raise ReadOnlyPath(self._path)
