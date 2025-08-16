#!/usr/bin/env python3
# coding=utf-8

import json
import base64
import colorlog
from pathlib import Path

logger = colorlog.getLogger("QriaDrama")
logger.setLevel("DEBUG")
log_handler = colorlog.StreamHandler()
log_handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
)
logger.addHandler(log_handler)
logger.info("QriaDrama starting...")


def get_cover_base64(cover_path: str | Path) -> str:
    cover_path = Path(cover_path)
    data = cover_path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/{cover_path.suffix[1:]};base64,{b64}"


ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DRAMAS: dict[Path, dict] = {
    p.parent: json.loads(p.read_text("utf-8")) for p in DATA_DIR.glob("*/qd.json")
}
logger.info(f"加载了 {len(DRAMAS)} 个剧本")


class API:
    def __init__(self) -> None:
        pass

    def get_dramas(self):
        """获取所有dramas数据"""
        logger.info(f"获取了 {len(DRAMAS)} 个剧本")
        logger.debug(f"返回值：{DRAMAS=}")
        return [
            {"title": d["title"], "cover": get_cover_base64(p / d["cover"])}
            for p, d in DRAMAS.items()
        ]

    def get_drama_lines(self, title: str, chapter: str = "") -> dict | None:
        """获取指定drama的lines数据和元数据"""
        DRAMA_ROOT = DATA_DIR / title
        meta = DRAMAS.get(DRAMA_ROOT)
        if meta is None:
            logger.error(f"未找到剧本 {title}")
            return None

        file = DRAMA_ROOT / (chapter or meta["index"])
        lines = json.loads(file.read_text("utf-8"))
        logger.info(f"获取了 {title} 的台词和元数据")
        logger.debug(f"返回值：{meta=}, {lines=}")
        return {"meta": meta, "lines": lines}
