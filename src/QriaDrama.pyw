#!/usr/bin/env python3
# coding=utf-8

import webview
from jsapi import API


def main():
    window = webview.create_window(
        "QriaDrama",
        "../static/index.html",
        width=1280,
        height=720,
        resizable=True,
        js_api=API(),
    )
    webview.start(ssl=True, debug=True)


if __name__ == "__main__":
    main()
