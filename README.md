About the Myrrh extension package.
=============================

This package is part of the Myrrh project.

It aims to simplify the management and registration of myrrh extensions by using URI.

Requirement
============

* Python: 3.11

Installation
============

To install myrrh-exts, simply execute:

```shell
$ pip install myrrh-exts
```

Getting Started
===============

Myrrh extension package is based on URI, predefined interfaces, and the standard entry point mechanism. 


How to define a myrrh extension?
--------------------------------

First define your extension by creating a protocol class, a session class, and an entry point class.

Declare the extension using the project configuration file, with the extension URI scheme being the group name and the extension URI path being the entry point name.


Sample implementation of extension.
-----------------------------------

myexts/hello.py
```python

from myrrh.exts.interfaces import IExtSession, IMyrrhExt, uri_rd
from myrrh.exts.protocol import StdExtSession
from myrrh.exts.misc import URI
from myrrh.exts.errors import InvalidPath

class IEchoProtocol(IExtProtocol):

    @uri_rd
    @abc.abstractmethod
    def hello(self): ...

class HelloSession(StdExtSession, IEchoProtocol):

    def __init__(self, path):
        super().__init__(IEchoProtocol)

        self.path = path

    def hello(self, myname):
        return f"Hello {myname} from {self.path}"

class Hello(IMyrrhExt):
    fullpath = ''
    
    def open(self, uri: str, *, req: urllib.request.Request | None = None) -> HelloSession:
        path = str(URI(uri).path).removeprefix(self.fullpath)  
        return HelloSession(path)
    
    def basepath(self, path: str):
        self.fullpath = path
        
    def extend(self, path: str, _obj):
        raise InvalidPath(path)

```

myexts/pyproject.toml
```
...

[myproject.exts]
/my/ext/path = "myext.hello:Hello"

...

```

myexts/main.py
```python
from myrrh.exts.core import Registry

Register().loads("myproject.exts")

with Registry().open("myproject.exts:/my/ext/path?=hello&myname=PyAnjel7") as f:
    open_resp = f.read(1)

c = Registry().client("myproject.exts:/my/ext/path")
with c.open():
    client_resp = c.hello('Pyanjel7')

assert open_resp == client_resp
```

Command line tool
-----------------

usage: mexts [-h] {push,get,list} uri

positional arguments:
  {push,get,list}
  uri

options:
  -h, --help       show this help message and exit

```shell
> mexts get "myrrh.exts:/registry?=loaded"
[['myrrh.exts:/registry']]
> mexts get "myrrh.exts:/registry?=__proto__"
[['findall', 'loaded']]
```