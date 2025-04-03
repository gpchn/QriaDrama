#!/usr/bin/env python3
# coding=utf-8

import click
import main
from pathlib import Path
from sys import platform
from os import devnull, system


@click.group()
def parser():
    pass


@parser.command()
@click.argument("project_path", type=click.Path())
@click.option("-o", "--output", type=click.Path(), required=False, help="输出路径")
def release(project_path: Path, output: Path):
    project_path = Path(project_path)
    output = Path(output) if output else Path(f"{project_path}.zhifpkg")
    main.release_zhifpkg(project_path, output)


@parser.command()
@click.argument("zhifpkg_path", type=click.Path())
@click.option("-o", "--output", type=click.Path(), required=False, help="输出路径")
def extract(zhifpkg_path: Path, output: Path):
    zhifpkg_path = Path(zhifpkg_path)
    output = Path(output) if output else Path(zhifpkg_path.parent)
    main.extract_zhifpkg(zhifpkg_path, output)


@parser.command()
@click.argument("zhifpkg_path", type=click.Path())
def load(zhifpkg_path: Path):
    zhifpkg_path = Path(zhifpkg_path)
    main.load_zhifpkg(zhifpkg_path)


if __name__ == "__main__":
    # 设置终端样式
    if platform == "win32":
        system(f"mode con: cols=50 lines=30")  # 设置行列
        system(f"chcp 65001 > {devnull}")  # 设置编码为 UTF-8
    parser()
