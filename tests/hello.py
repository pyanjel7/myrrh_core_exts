import urllib.request
import abc

from myrrh.exts.interfaces import IExtSession, IMyrrhExt, uri_rd
from myrrh.exts.misc import URI
from myrrh.exts.protocol import StdExtSession


class IEchoProtocol(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def hello(self): ...


class HelloSession(StdExtSession, IEchoProtocol):

    def __init__(self, path):
        super().__init__(IEchoProtocol)
        self.path = path

    def hello(self, myname):
        if self.path:
            return f"Hello {myname} from {self.path}"
        return f"Hello {myname}"


class Hello(IMyrrhExt):
    fullpath = ""

    def __init__(self):
        self._dirs = list()

    def open(self, uri: str, *, req: urllib.request.Request | None = None) -> HelloSession:
        path = str(URI(uri).path).removeprefix(self.fullpath)
        return HelloSession(path)

    def basepath(self, path: str):
        self.fullpath = path

    def extend(self, path: str, _obj):
        self._dirs.append(path)
