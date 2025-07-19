#!/usr/bin/env python3
# coding=utf-8

from pathlib import Path
from orjson import dumps
from colorama import init
from argparse import ArgumentParser
from colorlog import ColoredFormatter
from logging import Logger, StreamHandler


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file", type=CheckedPath, help="The file to be compiled")
    parser.add_argument("-o", "--output", type=Path, help="Output path")
    args = parser.parse_args()

    logger.info(f"Reading {args.file}")
    code = args.file.read_text(encoding="utf-8")

    logger.info(f"Compiling {args.file}")
    obj = compile(code)
    output = args.output if args.output else args.file.with_suffix(".json")
    output.write_bytes(dumps(obj))

    logger.info("Compilation succeeded!")


def CheckedPath(path) -> Path:
    path = Path(path)
    if not path.is_file():
        logger.error(f"File {path} does not exist!")
    return path


def compile(code: str) -> dict:
    lines = []
    for line in code.splitlines():
        if ";;" not in line:
            lines.append(line.replace("\\n", "\n"))
        else:
            parts = line.split(";;")
            parts = ((part.strip().split(" ", 1)) for part in parts)
            lines.append({part[0]: part[1].replace("\\n", "\n") for part in parts})
        logger.debug(lines[-1])
    return {"lines": lines}


class Log(Logger):
    """
    自定义日志类，使用 colorlog 的 ColoredFormatter 格式化日志输出。

    Args:
        level (int): 日志级别，默认为 logging.INFO。
    """

    def __init__(self, level: int = 10):
        super().__init__("QriaDrama Lang", level)
        self.setLevel(level)
        self.formatter = ColoredFormatter(
            "%(log_color)s[%(levelname)s] (%(asctime)s) %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
        self.console_handler = StreamHandler()
        self.console_handler.setLevel(level)
        self.console_handler.setFormatter(self.formatter)
        self.addHandler(self.console_handler)


if __name__ == "__main__":
    init()
    logger = Log()
    logger.debug("日志系统初始化")
    main()
