import numpy as np


class DataCarrierMixin:

    _data_attrs = ()
    """Iterable of attributes that hold references to data. These will be
    extracted when :func:`strip_data` is called. Any :class:`DataCarrierMixin`
    objects listed here will be recursively stripped.
    """

    def __init__(self):
        self._is_stripped = False

    def strip_data(self):
        """Strip data references and return a mapping.

        :returns:
            A mapping of (obj, attr_name) -> attr.
        """
        if self._is_stripped:
            raise ValueError("DataCarrierMixin object must not already be stripped")

        datamap = {}
        for attr_name in self._data_attrs:
            attr = getattr(self, attr_name)

            # If attr is another data carrier then it is stripped and the data
            # refs are added to the datamap but it is not deleted because it
            # still carries symbolic information.
            if isinstance(attr, DataCarrierMixin):
                datamap |= attr.strip_data()
            else:
                datamap[self, attr_name] = attr
                delattr(self, attr_name)

        self._is_stripped = True
        return datamap

    def attach_data(self, datamap):
        """Attach data references from a mapping.

        :arg datamap:
            A mapping of (obj, attr_name) -> attr.
        """
        if not self._is_stripped:
            raise ValueError("DataCarrierMixin object must be stripped to attach data to it")

        for attr_name in self._data_attrs:
            if hasattr(self, attr_name):
                attr = getattr(self, attr_name)
                assert isinstance(attr, DataCarrierMixin)
                attr.attach_data(datamap)
            else:
                attr = datamap[self, attr_name]
                setattr(self, attr_name, attr)

        self._is_stripped = False


class Function(DataCarrierMixin):
    _data_attrs = ("vec", "function_space")

    def __init__(self):
        super().__init__()
        self.vec = Vector()
        self.function_space = FunctionSpace()


class FunctionSpace(DataCarrierMixin):
    _data_attrs = ("dat",)

    def __init__(self):
        super().__init__()
        self.dat = np.empty(100)


class Vector(DataCarrierMixin):
    _data_attrs = ("dat",)

    def __init__(self):
        super().__init__()
        self.dat = np.empty(100)


def strip_form_data(self, form):
    """Strip the data from a form.

    :arg form:
        The :class:`~ufl.Form` object to be stripped. Note that it will be
        modified after calling this function.
    :returns:
        A mapping (:class:`dict`) from :class:`DataCarrierMixin` objects ->
        data structures.
    """
    datamap = {}
    for coeff in form.coefficients():
        datamap |= coeff.strip_data()
    return datamap


def attach_form_data(self, form, datamap):
    """Attach data back to a form.

    :arg form:
        The :class:`~ufl.Form` to have data attached to.
    :arg datamap:
        A mapping (:class:`dict`) from :class:`DataCarrierMixin` objects ->
        data structures.
    """
    for coeff in form.coefficients():
        coeff.attach_data(datamap)


if __name__ == "__main__":
    import pdb; pdb.set_trace()

    myfunc = Function()
    datamap = myfunc.strip_data()
    myfunc.attach_data(datamap)
