#!/usr/bin/env python3
# coding=utf-8

from sys import argv
from orjson import loads
from pathlib import Path
from zipfile import ZipFile
from tkinter.messagebox import showinfo, showwarning, showerror


def main():
    if len(argv) < 2:
        print("请输入一个文件路径！")
        showerror("QriaDrama Package Importer", "请输入一个qdpkg文件路径！")
        raise ValueError("No file path provided!")
    elif argv[1] == "-h" or argv[1] == "--help":
        print(f"""Usage:
    {argv[0]} <file_path>
    输入一个 qdpkg 文件路径，就可以自动导入。""")
        return
    path = Path(argv[1])
    save_path = Path(__file__).parent / "games"

    # 检查路径是否存在且为文件
    if not path.exists():
        showerror("错误", f"路径 {path.absolute()} 不存在！")
        raise FileNotFoundError(f"Path {path.absolute()} does not exist!")
    elif not path.is_file():
        showerror("错误", f"路径 {path.absolute()} 必须是一个文件！")
        raise FileNotFoundError(f"Path {path.absolute()} is not a file!")
    elif path.suffix != ".qdpkg":
        showwarning("警告", f"文件 {path.absolute()} 不是 qdpkg 文件！")

    # 读取压缩包
    with ZipFile(path, "r") as pkg:
        # 读取配置文件
        with pkg.open("main.json.qd") as f:
            pkg_data = f.read()
        pkg_data = loads(pkg_data)
        # 读取包名
        pkg_author = pkg_data["author"]
        pkg_name = pkg_data["name"]
        # 解压所有内容
        pkg.extractall(path=save_path / f"{pkg_name}_{pkg_author}")

    # 提示用户
    showinfo(f"导入成功！数据已储存在 {path.parent}")


if __name__ == "__main__":
    main()
