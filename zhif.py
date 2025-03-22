#!/usr/bin/env python3
# coding=utf-8

import click
import main
from pathlib import Path


@click.group()
def _main():
    pass


@_main.command()
@click.argument("path", type=click.Path(), default="default.zhif")
def load(path: Path):
    data = main.load_zhif(Path(path))
    for line in data.splitlines():
        main.parse(line)


@_main.command()
@click.argument("input_path", type=click.Path())
@click.argument("output_path", type=click.Path(), required=False)
def save(input_path: Path, output_path: Path):
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path.with_suffix(".zhif")
    main.save_zhif(input_path, output_path)


if __name__ == "__main__":
    main.set_cmd_font()
    _main()
