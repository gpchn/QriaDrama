#!/usr/bin/env python3
# coding=utf-8

import zhif
import gui
from pathlib import Path
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    i = zhif.Interpreter(args.path)
    i.load()
    md = i.main_data
    g = gui.GUI(md["font"], md["fg"], md["bg"])
    i.output = g

    def loop():
        if g.next:
            i.next()
        g.root.after(10, loop)
    g.root.after(10, loop)
    g.mainloop()


if __name__ == "__main__":
    main()
