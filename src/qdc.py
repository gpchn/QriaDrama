#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path
from argparse import ArgumentParser


def load_roles():
    """
    从当前目录的qd.json加载角色列表

    Returns:
        角色名称集合
    """
    config_path = Path("qd.json")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return set(config["roles"].keys())
    except Exception as e:
        print(f"警告: 无法加载角色配置: {e}")
        return set()  # 返回空集合


def parse_drama_file(input_path: Path):
    """
    解析戏剧脚本文件

    Args:
        input_path: 输入文件路径

    Returns:
        解析后的脚本列表，每个元素是一个字典 {角色: 文本}
    """
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"错误: 读取输入文件时出错: {e}")
        raise IOError(f"读取输入文件时出错: {e}")

    # 从配置文件加载角色列表
    roles = load_roles()

    result = []
    for line in lines:
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith("#"):
            continue

        # 分割行内容
        parts = line.split(" ", 1)

        # 检查是否有角色（第一个单词在角色列表中）
        if len(parts) == 2 and parts[0] in roles:
            role, text = parts
            result.append({role: text})
        else:
            # 没有角色，使用默认旁白
            result.append({"": line})

    return result


def compile_drama(input_path: Path, output_path: Path) -> bool:
    """
    编译戏剧脚本

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径

    Returns:
        编译是否成功
    """
    try:
        # 确保输出目录存在
        output_dir = output_path.parent
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
            print(f"创建输出目录: {output_dir}")

        # 解析输入文件
        parsed_data = parse_drama_file(input_path)

        # 写入输出文件
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        print(f"编译成功，输出文件: {output_path}")
        return True

    except Exception as e:
        print(f"编译失败: {e}")
        return False


def main():
    """主函数"""
    parser = ArgumentParser(
        description="QriaDrama 编译器 - 将简化 TXT 编译成标准 JSON 格式",
    )

    parser.add_argument("input", type=Path, help="输入脚本文件路径")
    parser.add_argument("output", nargs="?", type=Path, help="输出 JSON 文件路径")
    parser.add_argument(
        "--version", action="version", version="QriaDrama Compiler 1.0.0"
    )

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

    if success:
        print("编译成功!")
        sys.exit(0)
    else:
        print("编译失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
