#!/usr/bin/env python3
# coding=utf-8
"""
QriaDrama JavaScript API 模块
提供前端与后端交互的接口，包括剧本数据获取等功能
"""

import json
import base64
import colorlog
from pathlib import Path

# 配置彩色日志记录器
logger = colorlog.getLogger("QriaDrama")
logger.setLevel("DEBUG")
log_handler = colorlog.StreamHandler()
log_handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",        # 调试信息使用青色
            "INFO": "green",        # 一般信息使用绿色
            "WARNING": "yellow",    # 警告信息使用黄色
            "ERROR": "red",         # 错误信息使用红色
            "CRITICAL": "red,bg_white",  # 严重错误使用红底白字
        },
    )
)
logger.addHandler(log_handler)
logger.info("QriaDrama starting...")


def get_cover_base64(cover_path: str | Path) -> str:
    """
    将封面图片转换为Base64编码的数据URL

    Args:
        cover_path: 封面图片的路径，可以是字符串或Path对象

    Returns:
        str: Base64编码的数据URL，可直接用于HTML img标签的src属性
    """
    # 确保路径是Path对象
    cover_path = Path(cover_path)
    # 读取图片二进制数据
    data = cover_path.read_bytes()
    # 转换为Base64编码
    b64 = base64.b64encode(data).decode("utf-8")
    # 返回数据URL格式
    return f"data:image/{cover_path.suffix[1:]};base64,{b64}"


# 获取项目根目录和数据目录
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
# 确保数据目录存在，不存在则创建
DATA_DIR.mkdir(exist_ok=True)

# 加载所有剧本数据
DRAMAS: dict[Path, dict] = {
    # 遍历数据目录下所有qd.json文件，加载其内容
    p.parent: json.loads(p.read_text("utf-8")) for p in DATA_DIR.glob("*/qd.json")
}
logger.info(f"加载了 {len(DRAMAS)} 个剧本")


class API:
    """
    JavaScript API类
    提供给前端JavaScript调用的方法，实现前端与后端的数据交互
    """

    def __init__(self) -> None:
        """初始化API类"""
        pass

    def get_dramas(self):
        """
        获取所有剧本数据，用于首页剧本列表展示

        Returns:
            list: 包含剧本标题和封面数据URL的字典列表
        """
        logger.info(f"获取了 {len(DRAMAS)} 个剧本")
        logger.debug(f"返回值：{DRAMAS=}")
        # 返回剧本标题和封面数据URL列表
        return [
            {"title": d["title"], "cover": get_cover_base64(p / d["cover"])}
            for p, d in DRAMAS.items()
        ]

    def get_drama_lines(self, title: str, chapter: str = "") -> dict | None:
        """
        获取指定剧本的台词数据和元数据

        Args:
            title: 剧本标题，对应数据目录下的子目录名
            chapter: 章节名，可选参数，如果未指定则使用元数据中的index文件

        Returns:
            dict or None: 包含剧本元数据和台词数据的字典，如果剧本不存在则返回None
        """
        # 构建剧本根目录路径
        DRAMA_ROOT = DATA_DIR / title
        # 获取剧本元数据
        meta = DRAMAS.get(DRAMA_ROOT)
        if meta is None:
            logger.error(f"未找到剧本 {title}")
            return None

        # 确定要读取的台词文件，如果有指定章节则使用章节文件，否则使用元数据中的index文件
        file = DRAMA_ROOT / (chapter or meta["index"])
        # 读取并解析台词文件
        lines = json.loads(file.read_text("utf-8"))
        logger.info(f"获取了 {title} 的台词和元数据")
        logger.debug(f"返回值：{meta=}, {lines=}")
        # 返回元数据和台词数据
        return {"meta": meta, "lines": lines}
