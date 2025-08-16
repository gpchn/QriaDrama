#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QriaDrama 编译器 (QriaDrama Compiler)
用于将简化格式的TXT脚本文件编译成标准的JSON格式，供QriaDrama阅读器使用
"""

import json
import sys
from pathlib import Path
from argparse import ArgumentParser


def load_roles():
    """
    从当前目录的qd.json加载角色列表

    Returns:
        set: 角色名称集合
    """
    config_path = Path("qd.json")

    try:
        # 尝试打开并读取配置文件
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        # 返回角色名称集合
        return set(config["roles"].keys())
    except Exception as e:
        print(f"警告: 无法加载角色配置: {e}")
        return set()  # 返回空集合


def parse_drama_file(input_path: Path):
    """
    解析戏剧脚本文件

    将简化格式的TXT文件解析为QriaDrama阅读器可用的JSON格式
    简化格式要求：每行以角色名开头，后跟空格和对话内容
    如果行首不是角色名，则视为旁白

    Args:
        input_path: 输入文件路径

    Returns:
        list: 解析后的脚本列表，每个元素是一个字典 {角色: 文本}

    Raises:
        FileNotFoundError: 当输入文件不存在时
        IOError: 当读取输入文件出错时
    """
    # 检查输入文件是否存在
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    try:
        # 读取输入文件内容
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"错误: 读取输入文件时出错: {e}")
        raise IOError(f"读取输入文件时出错: {e}")

    # 从配置文件加载角色列表
    roles = load_roles()

    result = []
    for line in lines:
        # 去除行首尾空白字符
        line = line.strip()

        # 跳过空行和注释（以#开头的行）
        if not line or line.startswith("#"):
            continue

        # 分割行内容为两部分：角色和对话内容
        parts = line.split(" ", 1)

        # 检查是否有角色（第一个单词在角色列表中）
        if len(parts) == 2 and parts[0] in roles:
            role, text = parts
            result.append({role: text})
        else:
            # 没有角色，使用默认旁白（空字符串作为角色名）
            result.append({"": line})

    return result


def compile_drama(input_path: Path, output_path: Path) -> bool:
    """
    编译戏剧脚本

    将简化格式的TXT脚本文件编译成标准的JSON格式

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径

    Returns:
        bool: 编译是否成功
    """
    try:
        # 确保输出目录存在，不存在则创建
        output_dir = output_path.parent
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
            print(f"创建输出目录: {output_dir}")

        # 解析输入文件
        parsed_data = parse_drama_file(input_path)

        # 将解析后的数据写入输出文件，使用UTF-8编码，不转义ASCII字符，格式化缩进
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        print(f"编译成功，输出文件: {output_path}")
        return True

    except Exception as e:
        print(f"编译失败: {e}")
        return False


def main():
    """
    主函数
    处理命令行参数并调用编译函数
    """
    # 创建命令行参数解析器
    parser = ArgumentParser(
        description="QriaDrama 编译器 - 将简化 TXT 编译成标准 JSON 格式",
    )

    # 添加命令行参数
    parser.add_argument("input", type=Path, help="输入脚本文件路径")
    parser.add_argument("output", nargs="?", type=Path, help="输出 JSON 文件路径")
    parser.add_argument(
        "--version", action="version", version="QriaDrama Compiler 1.0.0"
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 处理输入输出路径
    input_path = Path(args.input)

    if args.output:
        output_path = Path(args.output)
    else:
        # 如果未指定输出路径，使用输入文件名，但扩展名改为 .json
        output_path = input_path.with_suffix(".json")

    print(f"输入文件: {input_path}")
    print(f"输出文件: {output_path}")

    # 编译脚本
    success = compile_drama(input_path, output_path)

    # 根据编译结果退出程序
    if success:
        print("编译成功!")
        sys.exit(0)
    else:
        print("编译失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
