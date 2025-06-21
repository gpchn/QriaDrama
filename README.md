# ZHIF - ZH_cn Interactive Fiction (Interpreter)

![ZHIF](https://github.com/gpchn/zhif/blob/main/zhif.ico)

ZHIF 是一个中文互动小说解释器，基于 Python3 实现。

~~（logo 是我拿 Graphics Gale 自己画的。知道很丑，先暂时用着……）~~

## 快速使用

### 使用 UV 运行

运行 `run.bat` 即可。

### 没有安装 UV

需要安装 `pyproject` 中写明的依赖，然后运行 `zhif.py`。

## 如何编写 zhif 游戏

zhif 的游戏目录结构如下：

- \[游戏名称]
  - \[任意名称].zhif _整体入口_
  - \[任意名称].json _游戏的元数据文件_
  - ... _其他剧本文件等_

### \[任意名称].zhif

这是整个游戏项目的初始入口，内容为 UTF-8 编码的文本，指明游戏的元数据文件（必须是相对路径）。例如：`main.json`，非常简短。

### \[任意名称].json

这个文件至关重要，记录了游戏的所有元数据，例如游戏名称、作者、版本等。格式如下：

```json
{
  "name": "HelloWorld", // 游戏名称
  "description": "Example project", // 游戏描述
  "version": "0.1.0", // 游戏版本
  "author": "gpchn", // 作者
  "license": null, // 许可证，null 表示无许可证

  "index": "scripts/1.json", // 游戏剧本的入口文件
  "roles": "roles.json", // 角色定义文件
  "default-style": {
    // 游戏默认样式
    "font": ["微软雅黑", 20], // 字体，默认为 ("微软雅黑", 14)
    "bg": "#111111", // 背景色，默认为 "white"
    "fg": "#777797" // 前景色，默认为 "black"
  }
}
```

请注意：

1. `index` 和 `roles` 是相对路径，相对于游戏根目录。
2. `default-style` 是可选的，如果未定义，则使用默认值。
3. 由于项目正在持续开发中，本文档记录的格式可能和最新的代码不完全一致，请以代码（注释）为准。项目 `games` 目录中有一个 `HelloWorld` 实例项目，这个项目不会出错。

## 其他特性

### 颜色支持

ZHIF 尽量保证在不同输出端（GUI、命令行）的颜色显示一致。目前支持 16 进制颜色和 [CSS 中广泛支持的 147 个颜色名称](https://www.runoob.com/cssref/css-colornames.html)。详见 `css_colors.py`

## 许可证

©Apache2.0 @gpchn
