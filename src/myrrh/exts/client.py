import contextlib
import urllib.parse
import typing

import urllib.request
import urllib.error

from .misc import URI
from .interfaces import ExtSessionT, IMyrrhExt


class ExtClient(typing.Generic[ExtSessionT]):

    def __init__(self, serv: IMyrrhExt):
        self.serv = serv
        self._uri = ""

    def seturi(self, uri):
        self._uri = uri

    def uri(self, uri=None):
        if uri is None:
            uri = self._uri

        uri_ = URI(uri)

        return uri_

    @contextlib.contextmanager
    def open(self, uri: str | None = None, *, req: urllib.request.Request | None = None) -> typing.Generator[ExtSessionT, None, None]:
        uri_ = self.uri(uri)

        session = self.serv.open(uri_.uri, req=req)

        try:
            yield session
        finally:
            session.close()

    def get(self, uri: str | None = None, *, req: urllib.request.Request | None = None) -> typing.Any:
        uri_ = self.uri(uri)

        with self.open(uri_.uri, req=req) as session:
            return session.query(uri_.split.query)

    def push(self, uri: str | None = None, data: typing.Any = None, *, req: urllib.request.Request | None = None) -> typing.Any:
        uri_ = self.uri(uri)

        with self.open(uri_.uri, req=req) as session:
            return session.request(uri_.split.query, data)
