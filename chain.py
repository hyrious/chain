#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import builtins


# TODO: fill other magic methods like __bool__
class chain:
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return repr(self.obj)

    def __getattr__(self, name):
        if hasattr(self.obj, name):
            return getattr(self.obj, name)
        elif (
            name.startswith("to_")
            and callable(value := getattr(builtins, name[3:]))
            or callable(value := getattr(builtins, name))
        ):

            def wrapped(*args, **kwargs):
                if len(args) > 0 and callable(args[0]):
                    f, *rest = args
                    return chain(value(f, self.obj, *rest, **kwargs))
                else:
                    return chain(value(self.obj, *args, **kwargs))

            return wrapped
        else:
            return getattr(self.obj, name)


# TODO: rewrite It with class Expr :p
class It:
    def __init__(self, x="x"):
        self.x = x

    def __gt__(self, y):
        return It(f"({self.x}) > {y}")

    def __mul__(self, y):
        return It(f"({self.x}) * {y}")

    def __call__(self, x):
        return eval(self.x)


it = It()

chain(range(10)).filter(it > 3).map(it * 2).to_list().print()
