from abc import ABC
from collections import namedtuple
import weakref


ArgCacheKey = namedtuple("ArgCacheKey", ["codegen_info", "map"])


class Arg(ABC):

    def __init__(self, codegen_info, map, *, data=None):
        if data is not None:
            assert issubclass(data, DataCarrier)

        self._codegen_info = codegen_info
        self._map = map
        self._data = weakref.proxy(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        assert issubclass(value, DataCarrier)
        self._data = weakref.proxy(value)
