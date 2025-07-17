#!/usr/bin/env python3
# coding=utf-8

import tkinter
import tkinter.scrolledtext
import tkinter.messagebox
from time import sleep
from css_colors import COLORS
from re import match


class GUI:
    """
    QriaDrama 默认 GUI 前端，使用 tkinter 实现

    Args:
        default_style (dict): 默认样式
    """

    def __init__(self, default_style: dict):
        font = default_style.get("font") or ("微软雅黑", 14)
        fg = default_style.get("fg", "#000000")
        bg = default_style.get("bg", "#ffffff")

        self.root = tkinter.Tk()
        self.root.title("QriaDrama")  # 设置窗口标题
        self.root.resizable(False, False)  # 设置窗口大小不可变
        self.root.geometry("800x600")  # 设置窗口大小
        self.root.iconbitmap("icon.ico")  # 设置窗口图标
        # 绑定按键
        self.root.bind("<Return>", self._next)  # 绑定回车键
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

        # 设置文本框
        self.st = tkinter.scrolledtext.ScrolledText(self.root, width=400, height=600)
        fg = self.handle_color(fg)
        bg = self.handle_color(bg)
        self.st.configure(font=font, bg=bg, fg=fg, state=tkinter.DISABLED)
        self.st.pack()  # 放置文本框
        self.st.focus_set()  # 获取焦点
        # 初始化允许输出下一行的标志
        self.need_next: bool = False

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

    def handle_color(self, color: str) -> str:
        """
        处理颜色

        Args:
            color (str): 要使用的颜色

        Returns:
            str: 处理后的颜色
        """

        # RGB 颜色转十六进制
        def rgb2hex(rgb: str) -> str:
            r, g, b = rgb.replace("rgb(", "").replace(")", "").split(",")
            return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

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
        self.st.insert(tkinter.END, " ·\n", "gray")
        self.st.update_idletasks()
        self.st.config(state=tkinter.DISABLED)
        self.st.see(tkinter.END)

    # 循环
    def mainloop(self) -> None:
        self.root.mainloop()
        self.root.destroy()