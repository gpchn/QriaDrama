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
# 前景色
FBK = colorama.Fore.BLACK
FBL = colorama.Fore.BLUE
FCY = colorama.Fore.CYAN
FGR = colorama.Fore.GREEN
FMG = colorama.Fore.MAGENTA
FRD = colorama.Fore.RED
FWT = colorama.Fore.WHITE
FYL = colorama.Fore.YELLOW
FLBK = colorama.Fore.LIGHTBLACK_EX
FLBL = colorama.Fore.LIGHTBLUE_EX
FLCY = colorama.Fore.LIGHTCYAN_EX
FLGR = colorama.Fore.LIGHTGREEN_EX
FLMG = colorama.Fore.LIGHTMAGENTA_EX
FLRD = colorama.Fore.LIGHTRED_EX
FLWT = colorama.Fore.LIGHTWHITE_EX
FLYL = colorama.Fore.LIGHTYELLOW_EX
# 背景色
BBK = colorama.Back.BLACK
BBL = colorama.Back.BLUE
BCY = colorama.Back.CYAN
BGR = colorama.Back.GREEN
BMG = colorama.Back.MAGENTA
BRD = colorama.Back.RED
BWT = colorama.Back.WHITE
BYL = colorama.Back.YELLOW
BLBK = colorama.Back.LIGHTBLACK_EX
BLBL = colorama.Back.LIGHTBLUE_EX
BLCY = colorama.Back.LIGHTCYAN_EX
BLGR = colorama.Back.LIGHTGREEN_EX
BLMG = colorama.Back.LIGHTMAGENTA_EX
BLRD = colorama.Back.LIGHTRED_EX
BLWT = colorama.Back.LIGHTWHITE_EX
BLYL = colorama.Back.LIGHTYELLOW_EX
# 样式
B = colorama.Style.BRIGHT
D = colorama.Style.DIM
N = colorama.Style.NORMAL
# 重置
R = colorama.Style.RESET_ALL
FR = colorama.Fore.RESET
BR = colorama.Back.RESET
# 默认颜色
DEFAULT_FORE = FWT
DEFAULT_BACK = BBK
DEFAULT_STYLE = N
# 继续提示符
CONTINUE_PROMPT = f" {R}{D}·{R}"

logging.basicConfig(
    level=logging.INFO,
    format=f"[{FRD}%(levelname)s{R}] %(funcName)s: {FRD}{B}%(message)s{R}",
)

DELAY = 0.1
END = False  # 不能用常规方法退出，会被键盘监听阻塞


def reset_color() -> None:
    """重置颜色"""

    global FORE, BACK, STYLE
    FORE = DEFAULT_FORE
    BACK = DEFAULT_BACK
    STYLE = DEFAULT_STYLE


def update_color() -> None:
    """更新颜色"""

    _print("", "")


reset_color()


def _print(text: str = "", end: str = "\n") -> None:
    """自定义的 print 函数"""
    print(f"{FORE}{BACK}{STYLE}{text}{R}", end=end, flush=True)


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
    _print(f"\n{R}运行已结束，按任意键退出...")
    with Listener(on_press=lambda _: False) as listener:
        listener.join()
    END = True


def typewrite(text: str, end: bool = True) -> None:
    """打字机效果输出"""

    for char in text:
        _print(char, "")
        sleep(DELAY)
    if end:
        _print(CONTINUE_PROMPT, "")
        with Listener(on_press=wait_next) as listener:
            listener.join()  # 直接等待直到监听停止


def parse_color(color: str, type: str = "fore") -> str:
    """解析颜色"""
    match color, type:
        # 前景色
        case "black" | "bk", "fore":
            return FBK
        case "blue" | "bl", "fore":
            return FBL
        case "cyan" | "cy", "fore":
            return FCY
        case "green" | "gr", "fore":
            return FGR
        case "magenta" | "mg", "fore":
            return FMG
        case "red" | "rd", "fore":
            return FGR
        case "white" | "wt", "fore":
            return FWT
        case "yellow" | "yl", "fore":
            return FYL
        case "lightblack" | "lbk", "fore":
            return FLBK
        case "lightblue" | "lbl", "fore":
            return FLBL
        case "lightcyan" | "lcy", "fore":
            return FLCY
        case "lightgreen" | "lgr", "fore":
            return FLGR
        case "lightmagenta" | "lmg", "fore":
            return FLMG
        case "lightred" | "lrd", "fore":
            return FLRD
        case "lightwhite" | "lwt", "fore":
            return FLWT
        case "lightyellow" | "lyl", "fore":
            return FLYL
        # 背景色
        case "black" | "bk", "back":
            return BBK
        case "blue" | "bl", "back":
            return BBL
        case "cyan" | "cy", "back":
            return BCY
        case "green" | "gr", "back":
            return BGR
        case "magenta" | "mg", "back":
            return BMG
        case "red" | "rd", "back":
            return BGR
        case "white" | "wt", "back":
            return BWT
        case "yellow" | "yl", "back":
            return BYL
        case "lightblack" | "lbk", "back":
            return BLBK
        case "lightblue" | "lbl", "back":
            return BLBL
        case "lightcyan" | "lcy", "back":
            return BLCY
        case "lightgreen" | "lgr", "back":
            return BLGR
        case "lightmagenta" | "lmg", "back":
            return BLMG
        case "lightred" | "lrd", "back":
            return BLRD
        case "lightwhite" | "lwt", "back":
            return BLWT
        case "lightyellow" | "lyl", "back":
            return BLYL
        # 样式
        case "bright" | "br", "style":
            return B
        case "dim" | "dm", "style":
            return D
        case "normal" | "nm", "style":
            return N
        case _, _:
            logging.error(f"无效的颜色设置：{color}, {type}")


def parse(line: str) -> None:
    """解析单行"""

    global DELAY, FORE, BACK, STYLE
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
        _print()
        return
    # * 此时的 line: list[str]

    match line:
        # 普通打字效果
        case str() as text:
            typewrite(text, end)
        # 打字效果变速
        case ["delay", str() as delay]:
            DELAY = float(delay)
        # 重置前景色
        case ["color", "fore", "reset"]:
            FORE = DEFAULT_FORE
            _print("", "")
        # 设置前景色
        case ["color", "fore", str() as color]:
            FORE = parse_color(color, "fore")
            _print("", "")
        # 重置背景色
        case ["color", "back", "reset"]:
            BACK = DEFAULT_BACK
            _print("", "")
        # 设置背景色
        case ["color", "back", str() as color]:
            BACK = parse_color(color, "back")
            _print("", "")
        # 重置样式
        case ["color", "style", "reset"]:
            STYLE = DEFAULT_STYLE
            _print("", "")
        # 设置样式
        case ["color", "style", str() as style]:
            STYLE = parse_style(style)
        # 重置所有
        case ["color", "reset"]:
            reset_color()
        # 等待几秒
        case ["sleep", str() as time]:
            sleep(float(time))
        # 结束
        case ["end"]:
            end_game()
        case _:
            logging.error(f"无效语句：{line}")
