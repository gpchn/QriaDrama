#!/usr/bin/env python3
# coding=utf-8
"""
QriaDrama 主程序入口
负责创建应用程序窗口并启动webview
"""

import webview
from jsapi import API


def main():
    """
    主函数，创建并启动QriaDrama应用程序窗口

    创建一个webview窗口，加载index.html作为主界面，
    设置窗口大小为1280x720，允许调整窗口大小，
    并将API类实例作为JavaScript接口提供给前端
    """
    # 创建应用程序窗口
    window = webview.create_window(
        "QriaDrama",  # 窗口标题
        "../static/index.html",  # 加载的HTML文件
        width=1280,  # 窗口宽度
        height=720,  # 窗口高度
        resizable=True,  # 允许调整窗口大小
        js_api=API(),  # 提供给前端JavaScript的API接口
    )
    # 启动webview，启用SSL
    webview.start(ssl=True)


if __name__ == "__main__":
    main()
