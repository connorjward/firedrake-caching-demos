from functools import cached_property


class Parloop:
    def __init__(self, kernel, iterset_arg, *args):
        """Create the parloop.

        :arg kernel:
            A Loopy kernel.
        :arg iterset_arg:
            Object holding code generation info for the iterset
            (e.g. extruded). It holds optional weakrefs to any data structures.
        :arg *args:
            Arg objects holding symbolic information about the arguments to
            the kernel. These hold optional weakrefs to data structures.
        """
        self._kernel = kernel
        self._iterset_arg = iterset_arg
        self._args = args

    def execute(self, datamap=None):
        """Execute the parloop.

        :arg datamap:
            Arg -> DataCarrier mapping.
        """
        # Resolve the data mapping
        if datamap is None:
            data = tuple(arg.data for arg in self._args)
        else:
            data = tuple(datamap[arg] for arg in self._args)

        # halo exchanges, compute, reductions, etc

    @cached_property
    def dll(self):
        """Generate and compile the code. This function is cached on the
        parloop instance for repeated use.
        
        :returns:
            Function pointer to the compiled C code.

        N.B. This function is clearly incomplete.
        """
        wrapper = generate(kernel, self._args)  # etc
        c_code = loopy.generate_code_v2(wrapper)
        return compile(c_code)


# Example usage when caching the parloop
if __name__ == "__main__":
    # Retrieve the cached argmap and parloop. Here argmap is a mapping (dict)
    # between each op2.Arg and the UFL coefficient that it corresponds to.
    # To avoid refcycles the coefficients are referenced weakly (argmap is a
    # WeakValueDictionary).
    # This does not include the output tensor (since this can change) so that
    # op2.Arg is returned separately.
    argmap, tensor_arg = form._cache.setdefault("argmap", make_argmap(form))
    parloop = form._cache.setdefault("parloop", make_parloop(argmap))

    # Create a mapping from op2.Arg -> op2.Dat. This needs to be a separate,
    # non-cached step in case the data structures of the form are modified
    # (i.e. it is stripped and then new data is attached).
    datamap = {arg: coeff.dat for arg, coeff in argmap}

    # Add the output tensor
    datamap[tensor_arg] = tensor.dat

    parloop.execute(datamap)
