import json


class JSObject(object):
    def __str__(self):  # pragma: no cover
        raise NotImplementedError("Implement this method")


class Operators(object):
    def __getattr__(self, attribute):
        if not attribute.startswith("__"):
            return ObjectProperty(identifier=attribute, parent=self)
        else:
            raise AttributeError(attribute)

    def __call__(self, *args):
        return Call(args=args, parent=self)


class Identifier(Operators, JSObject):
    def __init__(self, identifier):
        self._identifier = identifier

    def __str__(self):
        return "{}".format(self._identifier)


class ObjectProperty(Operators, JSObject):
    def __init__(self, *, identifier, parent):
        self._identifier = identifier
        self._parent = parent

    def __str__(self):
        return "{}.{}".format(self._parent, self._identifier)


class Call(Operators, JSObject):
    def __init__(self, *, args, parent):
        self._args = args
        self._parent = parent

    @staticmethod
    def is_number(obj):
        try:
            float(obj)
            return True
        except TypeError:
            return False

    @staticmethod
    def encode_arg(arg):
        if isinstance(arg, str) or Call.is_number(arg) or arg is None:
            return str(json.dumps(arg))

        if isinstance(arg, JSObject):
            return str(arg)

        elif isinstance(arg, dict):
            encoded_items = ", ".join(
                "{}: {}".format(json.dumps(k), Call.encode_arg(arg[k])) for k in sorted(arg.keys())
            )
            return "{{{}}}".format(encoded_items)

        elif isinstance(arg, list):
            encoded_items = ", ".join(Call.encode_arg(item) for item in arg)
            return "[{}]".format(encoded_items)

        else:
            raise ValueError("Obj type can't be encoded: {!r}".format(arg))

    def __str__(self):
        repr_args = ", ".join(Call.encode_arg(arg) for arg in self._args)
        return "{}({})".format(self._parent, repr_args)


class GlobalAwait(JSObject):
    def __init__(self, awaitable):
        self._awaitable = awaitable

    def __str__(self):
        return "return (async ()=> {{ return await {}; }})()".format(self._awaitable)
