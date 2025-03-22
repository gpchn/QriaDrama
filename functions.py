# coding=utf-8

import pyzstd
import logging
import colorama
from sys import exit
from time import sleep
from pathlib import Path
from os import system, devnull
from pynput.keyboard import Key, Listener

colorama.init()
RD = colorama.Fore.RED
GR = colorama.Fore.GREEN
YL = colorama.Fore.YELLOW
BL = colorama.Fore.BLUE
MG = colorama.Fore.MAGENTA
CY = colorama.Fore.CYAN
R = colorama.Style.RESET_ALL
B = colorama.Style.BRIGHT

logging.basicConfig(
    level=logging.INFO,
    format=f"[{RD}%(levelname)s{R}] %(funcName)s: {RD}{B}%(message)s{R}",
)

DELAY = 0.1
END = False  # 不能用常规方法退出，会被键盘监听阻塞


def set_cmd_font() -> None:
    """设置命令行字体"""

    system("mode con: cols=50 lines=30")
    system(f"chcp 65001 > {devnull}")


def load_zhif(path: Path) -> str:
    """加载 zhif 文件"""

    if not path.suffix == ".zhif":
        path = path.with_suffix(".zhif")

    # 检查文件是否存在
    path.exists() or logging.error(f"文件不存在：{path}") or exit(1)
    data = path.read_bytes()

    # 尝试解压文件
    try:
        data = pyzstd.decompress(data)
        data = data.decode("utf-8")
    except Exception as e:
        logging.error(e)
        exit(1)

    return data


def save_zhif(input_path: Path, output_path: Path) -> None:
    """保存为 zhif 文件"""

    # 将数据写入文件
    data = input_path.read_text("utf-8").encode("utf-8")
    data = pyzstd.compress(data)
    output_path.write_bytes(data)


def wait_next(key) -> None:
    """等待键盘输入"""

    if key == Key.esc:
        end_game()
    elif key == Key.space or key == Key.enter:
        print()
        return False  # 返回 False 停止监听
    else:
        return True


def end_game() -> None:
    """退出游戏"""

    global END
    print(f"\n{R}运行已结束，按任意键退出...")
    with Listener(on_press=lambda _: False) as listener:
        listener.join()
    END = True


def typewrite(text: str, end: bool = True) -> None:
    """打字机效果输出"""

    for char in text:
        print(char, end="", flush=True)
        sleep(DELAY)
    if end:
        sleep(0.1)
        with Listener(on_press=wait_next) as listener:
            listener.join()  # 直接等待直到监听停止


def parse_color(color: str) -> str:
    """解析颜色"""
    match color:
        case "red" | "rd":
            return RD
        case "green" | "gr":
            return GR
        case "yellow" | "yl":
            return YL
        case "blue" | "bl":
            return BL
        case "magenta" | "mg":
            return MG
        case "cyan" | "cy":
            return CY
        case "reset" | "r":
            return R
        case "bright" | "b":
            return B
        case _:
            logging.error(f"无效的颜色：{color}")
            return ""


def parse(line: str) -> None:
    """解析单行"""

    global DELAY
    if END:
        exit(0)

    # * 此时的 line: str
    # 检查是不是没写完一行
    if line.endswith("\\"):
        line = line[:-1]
        end = False
    else:
        end = True
    # 检查是不是空行或注释
    if line.isspace() or not line or line.startswith("#"):
        return
    if line.startswith("/") and len(line) > 1:
        line = line[1:].split(" ")
    # 只有一个 /，表示空行
    elif len(line) == 1:
        print()
        return
    # * 此时的 line: list[str]

    match line:
        # 普通打字效果
        case str() as text:
            typewrite(text, end)
        # 打字效果变速
        case ["delay", str() as delay]:
            DELAY = float(delay)
        case ["color", str() as color]:
            print(parse_color(color), end="")
        # 等待几秒
        case ["sleep", str() as time]:
            sleep(float(time))
        # 结束
        case ["end"]:
            end_game()
        case _:
            logging.error(f"无效语句：{line}")
