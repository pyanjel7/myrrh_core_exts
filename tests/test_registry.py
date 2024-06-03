import unittest

from myrrh.exts.core import registry
from hello import Hello


class BasicTests(unittest.TestCase):

    def test_basic_findall(self):
        exts = registry.Registry().findall("myrrh.exts")
        self.assertIn("myrrh.exts:/registry", exts)

    def test_basic_load(self):
        registry.Registry().load("myrrh.exts")

        self.assertIn("myrrh.exts:/registry", registry.Registry().loaded)

    def test_basic_extend(self):
        registry.Registry().extend("myrrh.exts:/hello", Hello())
        with registry.Registry().open("myrrh.exts:/hello?=hello&myname=PyAnjel7") as s:
            v = s.read(1)
        self.assertEqual(v, ["Hello PyAnjel7"])

        registry.Registry().extend("myrrh.exts:/hello/hello2", None)
        with registry.Registry().open("myrrh.exts:/hello/hello2?=hello&myname=PyAnjel7") as s:
            v = s.read(1)
        self.assertEqual(v, ["Hello PyAnjel7 from /hello2"])

        registry.Registry().extend("myrrh.exts:/root", registry.Root())
        registry.Registry().extend("myrrh.exts:/root/hello", Hello())
        registry.Registry().extend("myrrh.exts:/root/hello/hello2", None)
        registry.Registry().extend("myrrh.exts:/root/hello/hello2/hello3", None)

        with registry.Registry().open("myrrh.exts:/root/hello?=hello&myname=PyAnjel7") as s:
            v = s.read(1)
        self.assertEqual(v, ["Hello PyAnjel7"])

        with registry.Registry().open("myrrh.exts:/root/hello/hello2?=hello&myname=PyAnjel7") as s:
            v = s.read(1)

        self.assertEqual(v, ["Hello PyAnjel7 from /hello2"])

        with registry.Registry().open("myrrh.exts:/root/hello/hello2/hello3?=hello&myname=PyAnjel7") as s:
            v = s.read(1)

        self.assertEqual(v, ["Hello PyAnjel7 from /hello2/hello3"])

    def test_basic_client(self):
        registry.Registry().extend("myrrh.exts:/hello", Hello())
        c = registry.Registry().client("myrrh.exts:/hello")

        with c.open() as s:
            v = s.hello("PyAnjel7")

        self.assertEqual(v, "Hello PyAnjel7")
        
    def test_auto_load(self):
        import urllib.request
        registry.Registry().opener = urllib.request.OpenerDirector()
        with registry.Registry().open("myrrh.exts:/registry?=loaded") as s:
            v = s.read(1)       
        self.assertEqual(v, [["myrrh.exts:/registry"]])
        
if __name__ == "__main__":
    unittest.main()
