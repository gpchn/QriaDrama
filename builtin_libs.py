#!/usr/bin/env python3
# coding=utf-8


def choice(args, interpreter):
    if type(args) != dict:
        return
    for opt, arg in args:
        interpreter.output.write("")


funcs: dict = {"choice": choice}
