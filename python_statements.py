from __future__ import print_function
import os
import sys
import six

from time import time
from random import choice
from types import CodeType, FunctionType
from functools import wraps
from string import Formatter
from string import ascii_letters
from inspect import currentframe

six.moves.builtins.std_print = print

string_formatter = Formatter()


def random_string(length=20):
    """
    generate a random string of given length
    """
    return "".join(choice(ascii_letters)
                   for _ in range(length))


def print_with_eval(text, **kwargs):
    caller = currentframe().f_back
    keywords = {kw for _, kw, _, _
                in string_formatter.parse(text) if kw}

    for keyword in keywords:
        value = eval(keyword, caller.f_globals, caller.f_locals)
        text = text.replace("{{{}}}".format(keyword), str(value))

    std_print(text, **kwargs)


class TextObject(object):
    __slots__ = ["code", "text"]

    def __init__(self, text, code):
        self.text = text
        self.code = code

    @classmethod
    def from_text(cls, text):
        keywords = {random_string(): kw for _, kw, _, _
                    in string_formatter.parse(text) if kw}

        code = ["__keywords={}"]
        line_code = "__keywords[\"{kw_name}\"] = {kw_statement}"
        for key, value in six.iteritems(keywords):
            code.append(line_code.format(kw_name=key,
                                         kw_statement=value))
            text = text.replace("{{{}}}".format(value),
                                "{{{}}}".format(key))

        return cls(text=text,
                   code="\n".join(code))

    @classmethod
    def compile(cls, text):
        obj = cls.from_text(text)
        compiled = compile(obj.code, '<string>', 'exec')
        return cls(code=compiled, text=obj.text)


exec_memoize = {}


def print_with_exec(text, **kwargs):
    caller = currentframe().f_back

    text_obj = exec_memoize.get(text)
    if not text_obj:
        exec_memoize[text] = text_obj = TextObject.from_text(text)

    exec(text_obj.code, caller.f_globals, caller.f_locals)
    std_print(text_obj.text.format(**caller.f_locals["__keywords"]), **kwargs)

compile_memoize = {}


def print_with_compiled_exec(text, **kwargs):
    caller = currentframe().f_back

    text_obj = compile_memoize.get(text)
    if not text_obj:
        compile_memoize[text] = text_obj = TextObject.compile(text)

    exec(text_obj.code, caller.f_globals, caller.f_locals)
    std_print(text_obj.text.format(**caller.f_locals["__keywords"]), **kwargs)


class OptimizedTextObject(object):
    __slots__ = ["code", "locals", "globals"]

    def __init__(self, caller, code):
        self.code = code
        self.locals = caller.f_locals
        self.globals = caller.f_globals

    @staticmethod
    def get_keywords(text):
        return {random_string(): kw for _, kw, _, _
                in string_formatter.parse(text) if kw}

    @classmethod
    def from_text(cls, caller, text):
        keywords = cls.get_keywords(text)
        code = ["def awesome_print(text, **kwargs):"]
        line_code = "   {kw_name} = {kw_statement}"
        for key, value in six.iteritems(keywords):
            text = text.replace("{{{}}}".format(value),
                                "{{{}}}".format(key))

        code.append("   text = \"{}\"".format(text))
        args = ", ".join("{0}=({1})".format(key, val)
                         for key, val in six.iteritems(keywords))

        print_line = "   std_print(text.format({}), **kwargs)".format(args)
        code.append(print_line)
        return cls(caller=caller,
                   code="\n".join(code))

    @classmethod
    def compile(cls, caller, text):
        keywords = cls.get_keywords(text)
        if not keywords:
            return cls(code=std_print, caller=caller)

        obj = cls.from_text(caller, text)
        exec(obj.code, caller.f_locals, caller.f_locals)
        return cls(code=caller.f_locals.pop("awesome_print"), caller=caller)


optimized_compile_memoize = {}


def print_with_optimized_compiled_exec(text, **kwargs):
    text_obj = optimized_compile_memoize.get(text)
    if not text_obj:
        frame = currentframe()
        text_obj = OptimizedTextObject.compile(frame.f_back,
                                               text)
        optimized_compile_memoize[text] = text_obj
        del frame
    text_obj.code(text, **kwargs)


def print_as_std(text, **kwargs):
    std_print(text.format(**{"name": "oded",
                             "2*3": 2 * 3}),
              **kwargs)


fn_map = {
    "std": print_as_std,
    "eval": print_with_eval,
    "exec": print_with_exec,
    "compile": print_with_compiled_exec,
    "optimized-compile": print_with_optimized_compiled_exec,
}

devnull = open(os.devnull, 'w')


def main(argv):
    if len(argv) != 2:
        print("usage: {} <iterations>".format(sys.argv[0]))
        sys.exit(1)

    iterations = int(argv[1])
    name = "oded"
    for fn_name, fn in six.iteritems(fn_map):
        t = time()
        for _ in six.moves.range(iterations):
            fn("a non formatted string", file=devnull)
            fn("my name is {name} and 2*3={2*3}",
               file=devnull)
        std_print("block took {0:.3f} seconds [{1}]".format((time() - t),
                                                            fn_name))

if __name__ == "__main__":
    main(sys.argv)
0Looking
