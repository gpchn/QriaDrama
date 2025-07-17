#!/usr/bin/env python3
# coding=utf-8

from os import _exit
from pathlib import Path
from orjson import loads
from tkinter import Tk, Label, Button
from tkinter.messagebox import showinfo, showwarning, showerror

import gui

GAME_PATH = Path(__file__).parent / "games"


def main() -> None:
    # 搜索游戏
    games = [str(p) for p in GAME_PATH.glob("*")]
    # 显示主界面
    main_window = Tk()
    main_window.title("QriaDrama")
    main_window.geometry("300x400")
    main_window.resizable(False, False)
    main_window.iconbitmap("icon.ico")

    # 如果没有游戏
    if len(games) == 0:
        Label(
            main_window,
            text="您还没有添加游戏，请导入一个\n .qdpkg 格式的游戏包。",
            font=("微软雅黑", 14),
        ).place(x=0, y=0)
    # 如果有游戏，遍历每个游戏显示按钮
    else:
        for game in games:
            Button(
                main_window,
                text=Path(game).name,
                command=lambda game=game: not main_window.destroy() and load_game(game),
                font=("微软雅黑", 20),
            ).pack()

    main_window.mainloop()


def load_game(name: str) -> None:
    """
    加载/运行游戏

    Args:
        name (str): 游戏名称（文件夹名称）
    """
    # 隐藏主界面
    # 搜索游戏文件夹下的 qd 文件
    root = GAME_PATH / Path(name)
    indexes = list(root.glob("*.qd"))
    # 如果没有找到
    if len(indexes) == 0:
        showerror("错误", f"项目 {name} 没有 .qd 索引文件！")
        raise FileNotFoundError(f"Project {name} does not have .qd index file!")

    index_path = indexes[0]
    # 如果找到多个
    if len(indexes) > 1:
        showwarning(
            "警告", f"项目 {name} 有多个 qd 索引文件！选取了第一个：{index_path}"
        )

    metadata_file = root / index_path.read_text(encoding="utf-8")
    metadata = loads(metadata_file.read_text(encoding="utf-8"))
    style = metadata.get("default-style") or {}

    g = gui.GUI(style)
    i = Interpreter(root, metadata, g)

    # 循环检测阻塞是否解除
    def loop():
        if g.need_next and not i.next():
            _exit(0)
        g.root.after(10, loop)

    g.root.after(10, loop)
    g.mainloop()


class Interpreter:
    """
    解释器

    Args:
        root (Path): 游戏根目录
        metadata (dict): 游戏元数据
        output: 输出（GUI）
    """

    def __init__(self, root: Path, metadata: dict, output):
        self.root = root.resolve()  # 游戏根目录
        self.metadata = metadata  # 游戏元数据
        self.index_file = root / metadata["index"]  # 入口文件
        self.roles_file = root / metadata["roles"]  # 角色列表文件
        self.output = output  # 输出

        # 初始化解释器
        self.index = loads(self.index_file.read_text(encoding="utf-8"))  # 读取入口文件
        self.roles = loads(self.roles_file.read_text(encoding="utf-8"))  # 读取角色列表
        self.lines = self.index["lines"]  # 获取所有台词
        self.line = 0  # 当前行号
        self.lines_count = len(self.lines)  # 总行数
        # 默认值
        self.default_fg = self.metadata.get("default-style", {}).get("fg") or "#000000"
        self.default_bg = self.metadata.get("default-style", {}).get("bg") or "#ffffff"
        self.default_delay = self.metadata.get("default-style", {}).get("delay", 0.05)

    def __repr__(self):
        return f"Interpreter({self.root.name})"

    # 解析后输出
    def parse_out(self, line: dict):
        text = line.get("text")
        role = line.get("role")
        delay = line.get("delay") or self.default_delay
        fg = line.get("fg")
        bg = line.get("bg")

        role = self.roles.get(role, {"format": "{text}"})
        color = role.get("color") or self.default_fg
        text = role["format"].format(text=text)

        if fg:
            color = fg
        if bg:
            self.output.bg = bg

        self.output.write(text, color, delay)

    # 解释下一行内容
    def next(self) -> bool:
        # 如果已经到达最后一行，则退出
        if self.line >= self.lines_count:
            showinfo("QriaDrama", "游戏结束！")
            return False
        # 获取当前台词
        current_line = self.lines[self.line]
        if type(current_line) == str:  # 如果是字符串，则直接输出
            self.output.write(current_line, self.default_fg, self.default_delay)
        elif type(current_line) == dict:  # 包含参数
            self.parse_out(current_line)
        # 更新行号
        self.line += 1
        return True


if __name__ == "__main__":
    main()
