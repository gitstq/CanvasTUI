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
  <strong>強大的終端 JSON Canvas (.canvas) 檢視器與編輯器</strong>
</p>

<p align="center">
  直接在終端機中檢視、導航和編輯 Obsidian Canvas 檔案
</p>

---

## 🎉 專案介紹

**CanvasTUI** 是一款功能豐富的終端使用者介面（TUI）應用程式，專為檢視和編輯 JSON Canvas 檔案而設計。JSON Canvas 是一種開放的無限畫布資料檔案格式，由 Obsidian 推廣普及。

### 為什麼選擇 CanvasTUI？

- 🔒 **隱私優先**：無需開啟 Obsidian 即可檢視畫布檔案
- ⚡ **極速響應**：終端機中即時載入和導航
- 🖥️ **跨平台支援**：支援 Linux、macOS 和 Windows
- 🔍 **強大搜尋**：快速在所有節點中查找內容
- 📦 **零依賴**：提供單一可執行檔

### 靈感來源

本專案的靈感來源於在不啟動 Obsidian 的情況下快速檢視和搜尋畫布檔案的需求。它為生活在終端機中的開發者和進階使用者提供了一個輕量級的替代方案。

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📝 **節點檢視** | 檢視所有節點類型：文字、檔案、連結和群組節點 |
| 🔗 **連接展示** | 視覺化節點之間的連接關係 |
| 🔍 **快速搜尋** | 即時搜尋所有節點內容 |
| 📊 **畫布資訊** | 取得畫布檔案的統計資訊 |
| 📤 **匯出選項** | 匯出為 JSON、Markdown 或 Mermaid 圖表 |
| 👀 **即時監聽** | 檔案變更時自動重新載入 |
| 🎨 **色彩支援** | 完整的 24 位元色彩終端支援 |
| ⌨️ **鍵盤驅動** | 高效的純鍵盤導航 |

---

## 🚀 快速開始

### 環境需求

- Python 3.10 或更高版本
- 支援 ANSI 顏色的終端機

### 安裝方式

```bash
# 使用 pip 安裝
pip install canvastui

# 使用 pipx 安裝（推薦用於 CLI 工具）
pipx install canvastui

# 從原始碼安裝
git clone https://github.com/gitstq/CanvasTUI.git
cd CanvasTUI
pip install -e .
```

### 快速指令

```bash
# 在互動模式下開啟畫布檔案
canvastui open my-canvas.canvas

# 顯示檔案資訊
canvastui info my-canvas.canvas

# 列出所有節點
canvastui list my-canvas.canvas

# 搜尋節點
canvastui search my-canvas.canvas "搜尋關鍵字"

# 建立新畫布
canvastui new my-new-canvas.canvas

# 匯出為不同格式
canvastui export my-canvas.canvas output.md --format markdown
canvastui export my-canvas.canvas diagram.md --format mermaid
```

---

## 📖 詳細使用指南

### 互動模式

使用以下指令啟動互動式 TUI：

```bash
canvastui open my-canvas.canvas
```

#### 鍵盤快速鍵

| 按鍵 | 操作 |
|------|------|
| `q` | 結束程式 |
| `s` | 開啟搜尋 |
| `n` | 新建節點 |
| `e` | 編輯選中節點 |
| `d` | 刪除選中節點 |
| `w` | 切換檔案監聽 |
| `j/k` | 導航節點 |
| `Enter` | 選擇節點 |
| `Esc` | 清除選擇 |
| `?` | 顯示說明 |

### 命令列選項

#### `canvastui open`

在互動式 TUI 模式下開啟畫布檔案。

```bash
canvastui open [檔案路徑] [選項]

選項:
  --watch, -w    監聽檔案變更並自動重新載入
```

#### `canvastui info`

顯示畫布檔案的統計資訊。

```bash
canvastui info 檔案路徑
```

輸出包括：
- 節點數量
- 連接數量
- 畫布邊界
- 節點類型分佈

#### `canvastui list`

列出畫布檔案中的所有節點。

```bash
canvastui list 檔案路徑 [選項]

選項:
  --type, -t 文字    依節點類型篩選（text、file、link、group）
```

#### `canvastui search`

在節點中搜尋內容。

```bash
canvastui search 檔案路徑 查詢內容
```

搜尋不區分大小寫，搜尋範圍包括：
- 節點文字內容
- 節點標籤
- 檔案路徑
- URL 連結

#### `canvastui export`

將畫布匯出為不同格式。

```bash
canvastui export 檔案路徑 輸出路徑 [選項]

選項:
  --format, -f 文字    輸出格式：json、markdown、mermaid
```

### 範例：匯出為 Mermaid 圖表

```bash
canvastui export my-canvas.canvas diagram.md --format mermaid
```

輸出：
```mermaid
graph LR
    node1["介紹"]
    node2["特性"]
    node1 --> node2
```

---

## 💡 設計理念與發展藍圖

### 設計理念

CanvasTUI 遵循以下設計原則：

1. **簡潔性**：乾淨、直觀的介面
2. **高效能**：快速載入和響應式導航
3. **可擴展性**：易於新增功能和匯出格式
4. **相容性**：完全支援 JSON Canvas 規範

### 技術選型

- **Textual**：現代 TUI 框架，提供出色的元件支援
- **Rich**：精美的終端格式化和渲染
- **Pydantic**：強大的資料驗證
- **Click**：直觀的命令列介面

### 發展藍圖

| 版本 | 功能 |
|------|------|
| v1.1 | 節點編輯功能 |
| v1.2 | 連接建立和修改 |
| v1.3 | 多畫布分頁 |
| v1.4 | 自訂匯出器外掛系統 |
| v1.5 | 協作功能 |

---

## 📦 建置與部署

### 從原始碼建置

```bash
# 複製儲存庫
git clone https://github.com/gitstq/CanvasTUI.git
cd CanvasTUI

# 安裝開發相依性
pip install -e ".[dev]"

# 執行測試
pytest

# 建置套件
python -m build
```

### 建立獨立可執行檔

```bash
# 使用 PyInstaller
pip install pyinstaller
pyinstaller --onefile canvastui/cli.py --name canvastui
```

### Docker 支援

```dockerfile
FROM python:3.10-slim
RUN pip install canvastui
ENTRYPOINT ["canvastui"]
```

---

## 🤝 貢獻指南

我們歡迎各種形式的貢獻！以下是入門步驟：

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

### 提交規範

我們遵循 [約定式提交](https://www.conventionalcommits.org/zh-hant/) 規範：

- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 維護任務

---

## 📄 開源授權

本專案採用 MIT 授權條款開源 - 詳情請查看 [LICENSE](LICENSE) 檔案。

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
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 製作
</p>
