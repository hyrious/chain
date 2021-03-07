#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import builtins

__all__ = ["chain", "it", "slot"]

# TODO: fill other magic methods like __bool__
class chain:
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return repr(self.obj)

    def __iter__(self):
        return iter(self.obj)

    def __bool__(self):
        return bool(self.obj)

    def __getattr__(self, name):
        if hasattr(self.obj, name):
            return getattr(self.obj, name)
        else:
            value, g = None, globals()

            if name.startswith("to_"):
                kname = name[3:]
                value = value or getattr(builtins, kname, None)
                value = value or (g[kname] if kname in g else None)

            value = value or getattr(builtins, name, None)
            value = value or (g[name] if name in g else None)

            if not value:
                return getattr(self.obj, name)

            def wrapped(*_args, **kwargs):
                args, has_slot = [], False
                for arg in _args:
                    if isinstance(arg, Slot):
                        has_slot = True
                        args.append(arg(self.obj))
                    else:
                        args.append(arg)
                if has_slot:
                    return chain(value(*args, **kwargs))
                elif len(args) > 0 and callable(args[0]):
                    f, *rest = args
                    return chain(value(f, self.obj, *rest, **kwargs))
                else:
                    return chain(value(self.obj, *args, **kwargs))

            return wrapped

    def slot(self, *args, **kwargs):
        return chain(self.obj(*args, **kwargs))


# TODO: rewrite It with class Expr :p
class It:
    def __init__(self, x="x"):
        self.x = x

    def __call__(self, x):
        return eval(self.x)

    def __gt__(self, y):
        return type(self)(f"({self.x}) > {y}")

    def __lt__(self, y):
        return type(self)(f"({self.x}) < {y}")

    def __ge__(self, y):
        return type(self)(f"({self.x}) >= {y}")

    def __le__(self, y):
        return type(self)(f"({self.x}) <= {y}")

    def __eq__(self, y):
        return type(self)(f"({self.x}) == {y}")

    def __ne__(self, y):
        return type(self)(f"({self.x}) != {y}")

    def __add__(self, y):
        return type(self)(f"({self.x}) + {y}")

    def __sub__(self, y):
        return type(self)(f"({self.x}) - {y}")

    def __mul__(self, y):
        return type(self)(f"({self.x}) * {y}")

    def __pow__(self, y):
        return type(self)(f"({self.x}) ** {y}")


it = It()


class Slot(It):
    pass


slot = Slot()


if __name__ == "__main__":
    chain(range(10)).filter(it > 3).map(it + 2).to_list().print()
    chain([1, 2, 3, 4, 5, 9, 10]).to_tuple().filter(it == 5).to_list().print()
    chain([1, 2, 3]).map(it ** 2, slot + [1, 2]).to_list().print()

    from operator import add
    from functools import reduce

    chain([1, 2, 3]).add([4, 54, 6], slot).reduce(add, slot).print()

    chain(add).slot(1, 2).print()
