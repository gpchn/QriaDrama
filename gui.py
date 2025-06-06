#!/usr/bin/env python3
# coding=utf-8

import tkinter
import tkinter.scrolledtext
import tkinter.messagebox


class GUI:
    def __init__(self, font=("微软雅黑", 14), fg="black", bg="white"):
        self.root = tkinter.Tk()
        self.root.title("ZHIF")  # 设置窗口标题
        self.root.resizable(False, False)  # 设置窗口大小不可变
        self.root.geometry("400x600")  # 设置窗口大小
        self.root.attributes("-topmost", True)  # 设置窗口置顶
        # 绑定按键
        self.root.bind("<Return>", self._next)  # 绑定回车键
        self.root.bind("<Escape>", self._exit)  # 绑定 ESC 键
        self.root.protocol("WM_DELETE_WINDOW", self._exit)  # 绑定关闭窗口
        # 设置窗口菜单
        menu = tkinter.Menu(self.root)
        self.root.config(menu=menu)
        menu_file = tkinter.Menu(menu, tearoff=False)
        menu_file.add_command(label="打开", command=self._menu_open)
        menu_file.add_command(label="退出", command=self._exit)
        menu.add_cascade(label="文件", menu=menu_file)
        menu_about = tkinter.Menu(menu, tearoff=False)
        menu_about.add_command(label="关于 ZHIF", command=self._menu_about)
        menu_about.add_command(label="关于作者", command=self._menu_about_author)
        menu_about.add_command(label="帮助", command=self._menu_help)
        menu.add_cascade(label="关于", menu=menu_about)

        # 设置文本框
        self.st = tkinter.scrolledtext.ScrolledText(self.root, width=400, height=600)
        self.st.configure(font=font, bg=bg, fg=fg, state=tkinter.DISABLED)
        self.st.pack()  # 放置文本框
        self.st.focus_set()  # 获取焦点
        # 设置颜色标签
        self.st.tag_configure("red", foreground="red")
        self.st.tag_configure("blue", foreground="blue")
        self.st.tag_configure("green", foreground="green")
        self.st.tag_configure("yellow", foreground="yellow")
        self.st.tag_configure("purple", foreground="purple")
        self.st.tag_configure("cyan", foreground="cyan")
        self.st.tag_configure("white", foreground="white")
        self.st.tag_configure("black", foreground="black")
        self.st.tag_configure("gray", foreground="gray")
        self.st.tag_configure("orange", foreground="orange")
        self.st.tag_configure("pink", foreground="pink")
        self.st.tag_configure("brown", foreground="brown")
        self.st.tag_configure("gold", foreground="gold")
        self.st.tag_configure("silver", foreground="silver")
        self.st.tag_configure("maroon", foreground="maroon")
        self.st.tag_configure("navy", foreground="navy")
        self.st.tag_configure("lime", foreground="lime")
        self.st.tag_configure("olive", foreground="olive")
        self.st.tag_configure("teal", foreground="teal")
        self.st.tag_configure("aqua", foreground="aqua")
        self.st.tag_configure("fuchsia", foreground="fuchsia")

        self.next = False

    # 输出下一行
    def _next(self, _=None):
        self.next = True

    # 退出
    def _exit(self, _=None):
        # 确定是否退出
        if tkinter.messagebox.askokcancel("ZHIF", "确定要退出吗？"):
            self.root.destroy()
            exit(0)

    # 打开项目
    def _menu_open(self): ...

    def _menu_about(self):
        tkinter.messagebox.showinfo("ZHIF", "")

    def _menu_about_author(self):
        tkinter.messagebox.showinfo("ZHIF", """关于作者：
作者：gpchn
网址：https://gpchn.252123.xyz/
邮箱：gpchn@252123.xyz
Github：https://github.com/gpchn""")

    def _menu_help(self):
        tkinter.messagebox.showinfo("ZHIF", """使用帮助：
1. 打开一个 ZHIF 项目文件夹
2. 按 回车键 输出下一行
3. 按 ESC 键可以退出""")

    # 输出
    def write(self, text: str, color: str = None):
        self.next = False
        self.st.config(state=tkinter.NORMAL)
        if color:
            self.st.insert(tkinter.END, f"{text}\n", color)
        else:
            self.st.insert(tkinter.END, f"{text}\n")
        self.st.config(state=tkinter.DISABLED)
        self.st.see(tkinter.END)

    # 循环
    def mainloop(self):
        self.root.mainloop()
        self.root.destroy()
