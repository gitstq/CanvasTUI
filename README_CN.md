<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🎨 CanvasTUI</h1>

<p align="center">
  <strong>强大的终端 JSON Canvas (.canvas) 查看器和编辑器</strong>
</p>

<p align="center">
  直接在终端中查看、导航和编辑 Obsidian Canvas 文件
</p>

---

## 🎉 项目介绍

**CanvasTUI** 是一款功能丰富的终端用户界面（TUI）应用程序，专为查看和编辑 JSON Canvas 文件而设计。JSON Canvas 是一种开放的无穷画布数据文件格式，由 Obsidian 推广普及。

### 为什么选择 CanvasTUI？

- 🔒 **隐私优先**：无需打开 Obsidian 即可查看画布文件
- ⚡ **极速响应**：终端中即时加载和导航
- 🖥️ **跨平台支持**：支持 Linux、macOS 和 Windows
- 🔍 **强大搜索**：快速在所有节点中查找内容
- 📦 **零依赖**：提供单文件可执行程序

### 灵感来源

本项目的灵感来源于在不启动 Obsidian 的情况下快速查看和搜索画布文件的需求。它为生活在终端中的开发者和高级用户提供了一个轻量级的替代方案。

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📝 **节点查看** | 查看所有节点类型：文本、文件、链接和分组节点 |
| 🔗 **连接展示** | 可视化节点之间的连接关系 |
| 🔍 **快速搜索** | 即时搜索所有节点内容 |
| 📊 **画布信息** | 获取画布文件的统计信息 |
| 📤 **导出选项** | 导出为 JSON、Markdown 或 Mermaid 图表 |
| 👀 **实时监听** | 文件变化时自动重新加载 |
| 🎨 **色彩支持** | 完整的 24 位色彩终端支持 |
| ⌨️ **键盘驱动** | 高效的纯键盘导航 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本
- 支持 ANSI 颜色的终端

### 安装方式

```bash
# 使用 pip 安装
pip install canvastui

# 使用 pipx 安装（推荐用于 CLI 工具）
pipx install canvastui

# 从源码安装
git clone https://github.com/gitstq/CanvasTUI.git
cd CanvasTUI
pip install -e .
```

### 快速命令

```bash
# 在交互模式下打开画布文件
canvastui open my-canvas.canvas

# 显示文件信息
canvastui info my-canvas.canvas

# 列出所有节点
canvastui list my-canvas.canvas

# 搜索节点
canvastui search my-canvas.canvas "搜索关键词"

# 创建新画布
canvastui new my-new-canvas.canvas

# 导出为不同格式
canvastui export my-canvas.canvas output.md --format markdown
canvastui export my-canvas.canvas diagram.md --format mermaid
```

---

## 📖 详细使用指南

### 交互模式

使用以下命令启动交互式 TUI：

```bash
canvastui open my-canvas.canvas
```

#### 键盘快捷键

| 按键 | 操作 |
|------|------|
| `q` | 退出应用 |
| `s` | 打开搜索 |
| `n` | 新建节点 |
| `e` | 编辑选中节点 |
| `d` | 删除选中节点 |
| `w` | 切换文件监听 |
| `j/k` | 导航节点 |
| `Enter` | 选择节点 |
| `Esc` | 清除选择 |
| `?` | 显示帮助 |

### 命令行选项

#### `canvastui open`

在交互式 TUI 模式下打开画布文件。

```bash
canvastui open [文件路径] [选项]

选项:
  --watch, -w    监听文件变化并自动重新加载
```

#### `canvastui info`

显示画布文件的统计信息。

```bash
canvastui info 文件路径
```

输出包括：
- 节点数量
- 连接数量
- 画布边界
- 节点类型分布

#### `canvastui list`

列出画布文件中的所有节点。

```bash
canvastui list 文件路径 [选项]

选项:
  --type, -t 文本    按节点类型筛选（text、file、link、group）
```

#### `canvastui search`

在节点中搜索内容。

```bash
canvastui search 文件路径 查询内容
```

搜索不区分大小写，搜索范围包括：
- 节点文本内容
- 节点标签
- 文件路径
- URL 链接

#### `canvastui export`

将画布导出为不同格式。

```bash
canvastui export 文件路径 输出路径 [选项]

选项:
  --format, -f 文本    输出格式：json、markdown、mermaid
```

### 示例：导出为 Mermaid 图表

```bash
canvastui export my-canvas.canvas diagram.md --format mermaid
```

输出：
```mermaid
graph LR
    node1["介绍"]
    node2["特性"]
    node1 --> node2
```

---

## 💡 设计理念与路线图

### 设计理念

CanvasTUI 遵循以下设计原则：

1. **简洁性**：干净、直观的界面
2. **高性能**：快速加载和响应式导航
3. **可扩展性**：易于添加新功能和导出格式
4. **兼容性**：完全支持 JSON Canvas 规范

### 技术选型

- **Textual**：现代 TUI 框架，提供出色的组件支持
- **Rich**：精美的终端格式化和渲染
- **Pydantic**：强大的数据验证
- **Click**：直观的命令行界面

### 发展路线

| 版本 | 功能 |
|------|------|
| v1.1 | 节点编辑功能 |
| v1.2 | 连接创建和修改 |
| v1.3 | 多画布标签页 |
| v1.4 | 自定义导出器插件系统 |
| v1.5 | 协作功能 |

---

## 📦 构建与部署

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/CanvasTUI.git
cd CanvasTUI

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 构建包
python -m build
```

### 创建独立可执行文件

```bash
# 使用 PyInstaller
pip install pyinstaller
pyinstaller --onefile canvastui/cli.py --name canvastui
```

### Docker 支持

```dockerfile
FROM python:3.10-slim
RUN pip install canvastui
ENTRYPOINT ["canvastui"]
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！以下是入门步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

### 提交规范

我们遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 规范：

- `feat:` 新功能
- `fix:` 错误修复
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 维护任务

---

## 📄 开源协议

本项目采用 MIT 协议开源 - 详情请查看 [LICENSE](LICENSE) 文件。

```
MIT License

Copyright (c) 2026 gitstq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 制作
</p>
