import abc
import urllib.parse
import json
import typing

from .interfaces import IExtSession


class StdExtSession(IExtSession):

    def __init__(self, interface: type[abc.ABC]):
        self.queries = frozenset(m for m in interface.__abstractmethods__ if not m.startswith("_") and m not in IExtSession.__abstractmethods__)
        self.rd_queries = frozenset(m for m in self.queries if getattr(getattr(interface, m), "__access__", "").startswith("rd"))

    def _method(self, attr):
        m_name = attr.pop("", None)

        if m_name in self.queries:
            return getattr(self, m_name), m_name in self.rd_queries

        if m_name == "__proto__" :
            return getattr(self, m_name), True

    def _attr(self, attr):
        attrs = dict()
        for name, value in attr.items():
            if name.endswith("[js]"):
                value = json.loads(value)
                name = name[: len["[js]"]]
            attrs[name] = value
        return attrs

    def close(self):
        pass

    def query(self, query: str):
        attr = dict(urllib.parse.parse_qsl(query))
        method, rdonly = self._method(attr)
        attrs = self._attr(attr)

        if rdonly:
            return method(**attrs)

    def request(self, query: str, data: typing.Any | None = None):
        attr = dict(urllib.parse.parse_qsl(query))
        method, rdonly = self._method(attr)

        if rdonly:
            return self.query(query)

        attrs = self._attr(attr)

        return method(**attrs, data=data)

    def __proto__(self):
        return  list(self.queries)
