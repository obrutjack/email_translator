# 📋 配置管理使用指南

## 🎯 概述

新的配置管理系統讓你可以：
- 獨立管理郵件搜尋條件
- 儲存多組搜尋條件供重複使用
- 集中管理所有程式設定
- 輕鬆切換不同的搜尋場景

## 📁 配置檔案說明

### `config.json.example` - 範例配置檔案
包含所有可用設定的範例，可以複製並修改使用。

### `config.json` - 實際配置檔案
程式會自動建立，包含你的實際設定（已加入.gitignore保護）。

## 🚀 快速開始

### 1. 初始化配置
```bash
# 執行配置管理器
python config_manager.py
```

### 2. 設定Telegram資訊
在配置管理器中選擇「4. 更新Telegram設定」，輸入：
- Bot Token
- Chat ID

### 3. 新增搜尋條件
選擇「2. 新增搜尋條件」，例如：
```
名稱: work_reports
主旨: weekly report
寄件者: boss@company.com
日期: 2024/12/01
```

### 4. 執行程式
```bash
# 使用預設搜尋條件
python email_translator.py

# 使用特定搜尋條件
python email_translator.py work_reports
```

## 🔧 配置管理器功能

### 互動式選單
```bash
python config_manager.py
```

功能包括：
1. **查看所有搜尋條件** - 列出所有可用的搜尋條件
2. **新增搜尋條件** - 建立新的搜尋條件
3. **刪除搜尋條件** - 移除不需要的搜尋條件
4. **更新Telegram設定** - 設定Bot Token和Chat ID
5. **更新預設搜尋條件** - 修改預設的搜尋條件
6. **測試搜尋條件** - 預覽搜尋條件的內容

## 📧 搜尋條件設定

### 支援的搜尋參數
- **subject** - 郵件主旨關鍵字
- **sender** - 寄件者郵件地址
- **date_after** - 日期篩選（格式：YYYY/MM/DD）

### 搜尋條件範例

#### 工作報告
```json
{
  "subject": "weekly report",
  "sender": "boss@company.com",
  "date_after": "2024/12/01"
}
```

#### 帳單郵件
```json
{
  "subject": "invoice",
  "sender": "billing@company.com"
}
```

#### 電子報
```json
{
  "sender": "newsletter@example.com",
  "date_after": "2024/12/01"
}
```

## 🎮 使用方式

### 方法1: 使用預設搜尋條件
```bash
python email_translator.py
```

### 方法2: 指定搜尋條件
```bash
python email_translator.py work_reports
python email_translator.py invoices
python email_translator.py newsletters
```

### 方法3: 動態管理
```bash
# 開啟配置管理器
python config_manager.py

# 新增搜尋條件
# 執行程式
python email_translator.py new_search
```

## 📋 配置檔案結構

```json
{
  "telegram": {
    "bot_token": "your_bot_token",
    "chat_id": "your_chat_id"
  },
  "translation": {
    "deepl_api_key": "",
    "target_language": "zh-TW"
  },
  "pdf": {
    "chinese_font_path": "/System/Library/Fonts/PingFang.ttc"
  },
  "email_search": {
    "default_criteria": {
      "subject": "default_keyword",
      "sender": "",
      "date_after": ""
    },
    "saved_searches": {
      "work_reports": {
        "subject": "weekly report",
        "sender": "boss@company.com",
        "date_after": "2024/12/01"
      },
      "invoices": {
        "subject": "invoice",
        "sender": "billing@company.com"
      }
    }
  }
}
```

## 💡 使用技巧

### 1. 批次處理不同類型郵件
```bash
# 處理工作報告
python email_translator.py work_reports

# 處理帳單
python email_translator.py invoices

# 處理電子報
python email_translator.py newsletters
```

### 2. 定期任務設定
可以結合cron或其他排程工具：
```bash
# 每週一處理工作報告
0 9 * * 1 cd /path/to/email_translator && python email_translator.py work_reports

# 每月1號處理帳單
0 10 1 * * cd /path/to/email_translator && python email_translator.py invoices
```

### 3. 快速切換場景
為不同的使用場景建立專用的搜尋條件：
- `urgent` - 緊急郵件
- `daily` - 日常郵件
- `monthly` - 月報
- `client_a` - 特定客戶郵件

## 🔒 安全性

- `config.json` 已加入 `.gitignore`，不會被版本控制
- 敏感資訊（如Bot Token）只儲存在本地
- 可以使用 `config.json.example` 作為範本分享設定結構

## 🆘 故障排除

### 問題1: 找不到搜尋條件
```
⚠️ 找不到搜尋條件 'xxx'，使用預設條件
```
**解決方法**: 執行 `python config_manager.py` 檢查可用的搜尋條件

### 問題2: 搜尋條件為空
```
❌ 搜尋條件為空，請先設定搜尋條件
```
**解決方法**: 使用配置管理器新增或更新搜尋條件

### 問題3: Telegram設定錯誤
```
❌ 請先設定Telegram Bot Token
```
**解決方法**: 在配置管理器中更新Telegram設定

## 📈 進階用法

### 程式化配置管理
```python
from config_manager import ConfigManager

# 建立配置管理器
config = ConfigManager()

# 新增搜尋條件
config.add_search_criteria('new_search', {
    'subject': 'important',
    'sender': 'vip@company.com'
})

# 取得搜尋條件
criteria = config.get_search_criteria('new_search')
```

---

🎉 **享受更靈活的郵件搜尋管理！**