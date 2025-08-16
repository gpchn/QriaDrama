# QriaDrama

> 一个轻量级的戏剧脚本阅读器与编译器

QriaDrama 是一个用于阅读和编译戏剧脚本的应用程序，支持将简化格式的TXT脚本文件编译成标准的JSON格式，并通过友好的界面进行阅读。

*注：由于时间紧张，本文档由 AI 生成，仅供参考！*

## 目录

- [背景](#背景)
- [安装](#安装)
- [使用说明](#使用说明)
- [API](#api)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [许可证](#许可证)

## 背景

QriaDrama 旨在为戏剧爱好者提供一个简单易用的脚本阅读和创作工具。通过将简化格式的TXT脚本编译为结构化的JSON格式，用户可以更方便地组织和浏览戏剧内容。应用程序使用webview技术提供跨平台的图形界面，确保在不同操作系统上有一致的用户体验。

## 安装

### 环境要求

- Python 3.12 或更高版本

### 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/QriaDrama-ref.git
   cd QriaDrama-ref
   ```

2. 使用uv安装依赖
   ```bash
   uv sync
   ```

3. 运行应用程序
   ```bash
   python src/QriaDrama.pyw
   ```

## 使用说明

### 阅读剧本

1. 启动应用程序后，主界面会显示所有可用的剧本列表。
2. 点击剧本封面或标题即可打开剧本阅读器。
3. 在阅读器中，您可以浏览剧本内容，不同角色的对话会以不同的颜色显示。

### 编译脚本

QriaDrama 提供了一个命令行工具 `qdc.py`，用于将简化格式的TXT脚本文件编译成标准的JSON格式。

#### 简化格式说明

- 每行以角色名开头，后跟空格和对话内容。
- 如果行首不是角色名，则视为旁白。
- 空行和以#开头的行将被忽略。

#### 示例

假设有一个名为 `script.txt` 的文件，内容如下：

```
# 这是一个示例脚本
一个炎热的午后……
Lucky （擦汗）
Lucky 真倒霉……
Lucky 放假前最后一天留我一个人值日
Lucky 还好有你陪我
Panghu 谁说不是呢
Panghu 害，反正我回去也是闲着无聊，不如和你聊聊天
Panghu 回去记得微信联系
```

#### 创建配置文件

在脚本文件所在目录创建 `qd.json` 文件，定义角色和样式：

```json
{
  "title": "Lucky Lucky",
  "cover": "cover.jpg",
  "roles": {
    "": "color: white;",
    "Lucky": "color: red;",
    "Panghu": "color: orange;",
    "Xiaomin": "color: green;"
  },
  "index": "index.json"
}
```

#### 编译脚本

运行以下命令编译脚本：

```bash
python src/qdc.py script.txt
```

编译完成后，会在同一目录下生成 `script.json` 文件，内容如下：

```json
[
  {"": "一个炎热的午后……"},
  {"Lucky": "（擦汗）"},
  {"Lucky": "真倒霉……"},
  {"Lucky": "放假前最后一天留我一个人值日"},
  {"Lucky": "还好有你陪我"},
  {"Panghu": "谁说不是呢"},
  {"Panghu": "害，反正我回去也是闲着无聊，不如和你聊聊天"},
  {"Panghu": "回去记得微信联系"}
]
```

您也可以指定输出文件路径：

```bash
python src/qdc.py script.txt output.json
```

## API

QriaDrama 提供了JavaScript API，用于前端与后端的数据交互。

### API 类

#### `get_dramas()`

获取所有剧本数据，用于首页剧本列表展示。

**返回值：**
- `list`: 包含剧本标题和封面数据URL的字典列表

#### `get_drama_lines(title, chapter)`

获取指定剧本的台词数据和元数据。

**参数：**
- `title` (str): 剧本标题，对应数据目录下的子目录名
- `chapter` (str, 可选): 章节名，如果未指定则使用元数据中的index文件

**返回值：**
- `dict or None`: 包含剧本元数据和台词数据的字典，如果剧本不存在则返回None

## 维护者

[@yourusername](https://github.com/yourusername)。

## 如何贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

[MIT](LICENSE) © Your Name
