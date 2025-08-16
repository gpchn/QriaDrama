#!/usr/bin/env python3
# coding=utf-8

import tkinter
import tkinter.messagebox
import tkinter.scrolledtext
from re import match
from time import sleep
from pathlib import Path
from css_colors import COLORS
from os import name as OS_NAME, system


def hex2rgb(hex_color: str) -> tuple[int, int, int]:
    """
    将十六进制颜色转换为 RGB 颜色

    Args:
        hex_color (str): 十六进制颜色

    Returns:
        tuple[int, int, int]: RGB 颜色
    """
    hex_color = hex_color.replace("fg_#", "").replace("bg_#", "").replace("#", "")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def rgb2hex(rgb: str) -> str:
    """
    将 RGB 颜色转换为十六进制颜色

    Args:
        rgb (str): RGB 颜色

    Returns:
        str: 十六进制颜色
    """
    r, g, b = rgb.replace("rgb(", "").replace(")", "").split(",")
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


class GUI:
    """
    QriaDrama 默认 GUI 前端，使用 tkinter 实现

    Args:
        name (str): 项目名称
        default_style (dict): 默认样式
    """

    def __init__(self, GAME_PATH: Path, GAME_NAME: str, default_style: dict) -> None:
        font = default_style.get("font") or ("微软雅黑", 14)
        font_path = default_style.get("font-path")
        font_path = GAME_PATH / font_path if font_path else None
        fg = default_style.get("fg", "#000000")
        bg = default_style.get("bg", "#ffffff")
        window_name = default_style.get("window_name", GAME_NAME)
        window_size = default_style.get("window_size", "800x600")
        window_width, window_height = map(int, window_size.split("x"))
        icon = default_style.get("icon")
        if icon:
            icon = GAME_PATH / icon
        else:
            icon = "QriaDrama.ico"

        # 创建窗口
        self.root = tkinter.Tk()
        self.root.title(window_name)  # 设置窗口标题
        self.root.geometry(window_size)  # 设置窗口大小
        self.root.resizable(False, False)  # 设置窗口大小不可变
        self.root.iconbitmap(icon)  # 设置窗口图标

        # 绑定按键
        self.root.bind("<space>", self._next)  # 绑定空格键
        self.root.bind("<Escape>", self._exit)  # 绑定 ESC 键
        self.root.protocol("WM_DELETE_WINDOW", self._exit)  # 绑定关闭窗口

        # 设置窗口菜单
        menu = tkinter.Menu(self.root)
        self.root.config(menu=menu)
        menu_file = tkinter.Menu(menu, tearoff=False)
        menu_file.add_command(label="", command=print)  # todo
        menu_file.add_command(label="退出", command=self._exit)
        menu.add_cascade(label="设置", menu=menu_file)
        menu_about = tkinter.Menu(menu, tearoff=False)
        menu_about.add_command(label="帮助", command=self._menu_help)
        menu_about.add_command(label="关于", command=self._menu_about)
        menu.add_cascade(label="关于", menu=menu_about)

        # 创建输入框
        self.entry = tkinter.Entry(self.root, font=font, justify="center")
        # 创建文本框
        self.st = tkinter.scrolledtext.ScrolledText(self.root)
        # 计算颜色
        self.fg = self.handle_color(fg)
        self.bg = self.handle_color(bg)
        self.dot_color = self.calc_dot_color()  # 根据前景色和背景色自动计算点的颜色
        # 设置输入框
        entry_height = self.entry.cget("height")
        print(entry_height)
        self.entry.place(
            x=0, y=window_height - entry_height, width=window_width, height=entry_height
        )
        self.entry.bind("<Return>", self._enter)  # 绑定回车键
        self.entry_text: str | None = None
        self.entry.config(fg=self.dot_color, bg=self.bg)
        # 设置文本框
        self.st.configure(font=font, bg=self.bg, fg=self.fg, state=tkinter.DISABLED)
        self.st.place(x=0, y=0, width=window_width, height=window_height - entry_height)
        self.st.focus_set()  # 获取焦点

        self.handle_color(self.dot_color)  # 注册点颜色
        self.need_next: bool = False  # 初始化允许输出下一行的标志

        # 安装字体
        font_installed = GAME_PATH / "font_installed"
        if font_path and not font_installed.is_file():
            tkinter.messagebox.showinfo("QriaDrama", f"请操作软件安装字体：{font_path}")
            if OS_NAME == "nt":
                system(f"start {font_path}")
            elif OS_NAME == "posix" or OS_NAME == "darwin":
                system(f"open {font_path}")
            font_installed.touch()

    # 获取输入
    def _enter(self, _=None):
        self.entry_text = self.entry.get() or None
        self.entry.delete(0, tkinter.END)

    # 输出下一行
    def _next(self, _=None) -> None:
        self.need_next = True

    # 退出
    def _exit(self, _=None) -> None:
        # 确定是否退出
        if tkinter.messagebox.askokcancel("QriaDrama", "确定要退出吗？"):
            # * 保存等操作
            self.root.destroy()
            exit(0)

    def _menu_about(self) -> None:
        tkinter.messagebox.showinfo(
            "QriaDrama",
            """
QriaDrama 是一个中文互动小说引擎，使用 Python 实现。
GitHub：https://github.com/gpchn/QriaDrama
关于作者：
作者：gpchn
网址：https://gpchn.252123.xyz/
邮箱：gpchn@252123.xyz""",
        )

    def _menu_help(self) -> None:
        tkinter.messagebox.showinfo(
            "QriaDrama",
            """使用帮助：
1. 打开一个 QriaDrama 项目文件夹
2. 按 回车键 输出下一行
3. 按 ESC 键可以退出""",
        )

    def calc_dot_color(self) -> str:
        """
        计算点的颜色，储存在 self.dot_color


        Args:
            fg (str): 前景色
            bg (str): 背景色
        """

        # 获取前景色和背景色的RGB值
        fg_rgb = hex2rgb(self.fg)
        bg_rgb = hex2rgb(self.bg)

        # 加权平均计算点的颜色（80%背景色，20%前景色）
        dot_r = int(bg_rgb[0] * 0.7 + fg_rgb[0] * 0.3)
        dot_g = int(bg_rgb[1] * 0.7 + fg_rgb[1] * 0.3)
        dot_b = int(bg_rgb[2] * 0.7 + fg_rgb[2] * 0.3)

        # 转换为十六进制格式
        return f"#{dot_r:02x}{dot_g:02x}{dot_b:02x}"

    def handle_color(self, color: str) -> str:
        """
        处理颜色

        Args:
            color (str): 要使用的颜色

        Returns:
            str: 处理后的颜色（十六进制）
        """

        # 十六进制
        if match(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color) or match(
            r"^fg_#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color
        ):
            color = color.replace("fg_", "")
            self.st.tag_configure(color, foreground=color)
        elif match(r"^bg_#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color):
            color = color.replace("bg_", "")
            self.st.tag_configure(color, background=color)
        # CSS 颜色
        elif color in COLORS:
            self.st.tag_configure(color, foreground=COLORS[color])
        # RGB 颜色
        elif match(r"^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$", color) or match(
            r"^fg_rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$", color
        ):
            color_rgb = color.replace("fg_", "")
            color = rgb2hex(color_rgb)
            self.st.tag_configure(color_rgb, foreground=color)
        elif match(r"^bg_rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$", color):
            color_rgb = color.replace("bg_", "")
            color = rgb2hex(color_rgb)
            self.st.tag_configure(color_rgb, background=color)

        return color

    # 输出
    def write(self, text: str, color: str, delay: float) -> None:
        """
        输出文本到 GUI

        Args:
            text (str): 要输出的文本
            color (str | None, optional): 要使用的颜色。默认值为 None，即不指定颜色。
        """
        self.need_next = False
        self.st.config(state=tkinter.NORMAL)
        # 处理颜色
        self.handle_color(color)
        # 输出文本
        for char in text:
            self.st.insert(tkinter.END, char, color)
            self.st.update_idletasks()  # 刷新
            sleep(delay)
        self.st.insert(tkinter.END, " ·\n", self.dot_color)
        self.st.update_idletasks()
        self.st.config(state=tkinter.DISABLED)
        self.st.see(tkinter.END)

    # 循环
    def mainloop(self) -> None:
        self.root.mainloop()
        self.root.destroy()

    def get_input(self): ...
