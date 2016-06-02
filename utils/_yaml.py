try:
    from yaml import CLoader as Loader, CDumper as Dumper
    from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
    from yaml import Loader, Dumper
    from yaml import SafeLoader, SafeDumper
