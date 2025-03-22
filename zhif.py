#!/usr/bin/env python3
# coding=utf-8

import click
import functions
from pathlib import Path


@click.group()
def main():
    pass


@main.command()
@click.argument("path", type=click.Path(), default="default.zhif")
def load(path: Path):
    data = functions.load_zhif(Path(path))
    for line in data.splitlines():
        functions.parse(line)


@main.command()
@click.argument("input_path", type=click.Path())
@click.argument("output_path", type=click.Path(), required=False)
def save(input_path: Path, output_path: Path):
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path.with_suffix(".zhif")
    functions.save_zhif(input_path, output_path)


if __name__ == "__main__":
    functions.set_cmd_font()
    main()
