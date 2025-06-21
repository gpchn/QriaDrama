#!/usr/bin/env python3
# coding=utf-8

import tkinter
import tkinter.scrolledtext
import tkinter.messagebox
from css_colors import COLORS


class GUI:
    """
    ZHIF 默认 GUI 前端，使用 tkinter 实现

    Args:
        font (tuple): 字体，默认为 ("微软雅黑", 14)
        fg (str): 前景色，默认为 "black"
        bg (str): 背景色，默认为 "white"
    """

    def __init__(self, default_style: dict):
        font = default_style.get("font") or ("微软雅黑", 14)
        fg = default_style.get("fg") or "black"
        bg = default_style.get("bg") or "white"
        self.root = tkinter.Tk()
        self.root.title("ZHIF")  # 设置窗口标题
        self.root.resizable(False, False)  # 设置窗口大小不可变
        self.root.geometry("400x600")  # 设置窗口大小
        self.root.iconbitmap("zhif.ico")  # 设置窗口图标
        # 绑定按键
        self.root.bind("<Return>", self._next)  # 绑定回车键
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
        menu_about.add_command(label="关于 ZHIF", command=self._menu_about)
        menu.add_cascade(label="关于", menu=menu_about)

        # 设置文本框
        self.st = tkinter.scrolledtext.ScrolledText(self.root, width=400, height=600)
        self.st.configure(font=font, bg=bg, fg=fg, state=tkinter.DISABLED)
        self.st.pack()  # 放置文本框
        self.st.focus_set()  # 获取焦点
        # 适配 CSS 147 个颜色单词
        for color_name, color_value in COLORS.items():
            self.st.tag_configure(color_name, foreground=color_value)
        # 适配全部十六进制颜色
        for i in range(16):
            for j in range(16):
                for k in range(16):
                    color = f"#{i:02x}{j:02x}{k:02x}"
                    self.st.tag_configure(color, foreground=color)
        # 初始化允许输出下一行的标志
        self.need_next = False

    # 输出下一行
    def _next(self, _=None) -> None:
        self.need_next = True

    # 退出
    def _exit(self, _=None) -> None:
        # 确定是否退出
        if tkinter.messagebox.askokcancel("ZHIF", "确定要退出吗？"):
            # * 保存等操作
            self.root.destroy()
            exit(0)

    def _menu_about(self) -> None:
        tkinter.messagebox.showinfo(
            "ZHIF",
            """
ZHIF（ZH_cn Interactive Fiction）是一个中文互动小说引擎，使用 Python 实现。
GitHub：https://github.com/gpchn/zhif
关于作者：
作者：gpchn
网址：https://gpchn.252123.xyz/
邮箱：gpchn@252123.xyz""",
        )

    def _menu_help(self) -> None:
        tkinter.messagebox.showinfo(
            "ZHIF",
            """使用帮助：
1. 打开一个 ZHIF 项目文件夹
2. 按 回车键 输出下一行
3. 按 ESC 键可以退出""",
        )

    # 输出
    def write(self, text: str, color: str | None = None) -> None:
        """
        输出文本到 GUI

        Args:
            text (str): 要输出的文本
            color (str | None, optional): 要使用的颜色。默认值为 None，即不指定颜色。
        """
        self.need_next = False
        self.st.config(state=tkinter.NORMAL)
        if color:
            self.st.insert(tkinter.END, f"{text}\n", color)
        else:
            self.st.insert(tkinter.END, f"{text}\n")
        self.st.config(state=tkinter.DISABLED)
        self.st.see(tkinter.END)

    # 循环
    def mainloop(self) -> None:
        self.root.mainloop()
        self.root.destroy()
