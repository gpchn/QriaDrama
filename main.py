#!/usr/bin/env python3
# coding=utf-8

import orjson
from pathlib import Path


class Interpreter:
    def __init__(self, path: Path):
        if not path.is_dir():  # 检查路径是否为目录
            raise ValueError("path must be a directory")
        if not (path / "main.json").is_file():  # 检查 main.json 文件是否存在
            raise ValueError("main.json not found")
        self.path = path.resolve()  # 获取绝对路径
        self.main_data = None  # main.json 数据
        self.output = None  # * 输出需在 main.py 中定义

        self.curr_line = 1  # 当前行号

    def __repr__(self):
        return f"Interpreter({self.path})"

    # 读取项目
    def load(self):
        # 读取 main.json
        self.main_path = self.path / "main.json"
        main_data = self.main_path.read_text("utf-8")
        main_data = orjson.loads(main_data)
        self.main_data = main_data

        # 读取入口文件
        self.index_path = Path(self.path / self.main_data["index"]).resolve()
        self.index = orjson.loads(self.index_path.read_text("utf-8"))

        # 初始化
        self.lines = self.index["lines"]
        self.line = 0
        self.lines_count = len(self.lines)
        self.roles = self.main_data["roles"]

    # 角色说话
    def role_says(self, name: str, text: str):
        role = self.roles[name]
        self.output.write(f"{name}: {text}", role["color"])

    # 下一行
    def next(self):
        if self.main_data is None:
            raise ValueError("data not loaded")
        if self.line >= self.lines_count:
            return

        line = self.lines[self.line]
        if type(line) == str:  # 如果是字符串，则直接输出
            self.output.write(line)
        elif type(line) == list:  # 如果是列表，则以角色输出
            role = line[0]
            text = line[1]
            self.role_says(role, text)
        self.line += 1
