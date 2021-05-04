from arg import Arg, ArgCacheKey


class Dat:

    def __init__(self):
        self._arg_cache = {}

    @property
    def _codegen_info(self):
        ...

    def to_arg(self, map):
        """Create a DatArg from this Dat.

        :arg map:
            A mapping.

        The Arg is cached on the Dat for reuse.
        """
        cache_key = ArgCacheKey(self.codegen_info, map)
        arg = DatArg(self._codegen_info, map, data=self)
        return self._arg_cache.setdefault(cache_key, arg)


class DatArg(Arg):
    ...