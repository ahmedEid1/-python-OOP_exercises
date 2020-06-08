import inspect

from position import *


def auto_repr(cls):
    members = vars(cls)

    if "__repr__" in members:
        raise TypeError(f"{cls.__name__} already defines __repr__")

    if not "__init__" in members:
        raise TypeError(f"{cls.__name__} does not override __init")
    sig = inspect.signature(cls.__init__)
    parameter_names = list(sig.parameters)[1:]

    if not all(
        isinstance(members.get(name, None), property)
        for name in parameter_names
    ):
        raise TypeError(
            f"cannot  apply auto_repr to {cls.__name__} "
            f"because not all __init__ parameters have matching properties"
        )

    def synthesized_repr(self):
        return "{typename}({args})".format(
            typename=typename(self),
            args=", ".join(
                "{name}={value!r}".format(
                    name=name,
                    value=getattr(self, name)
                ) for name in parameter_names
            )
        )

    setattr(cls, "__repr__", synthesized_repr)

    return cls


@auto_repr
class Location:

    def __init__(self, name, position):
        self._name = name
        self._position = position

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    def __str__(self):
        return self.name


hong_kong = Location("Hong Kong", EarthPosition(22.99, 14.16))
