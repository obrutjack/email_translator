# 📧 郵件翻譯器 (Email Translator)

一個自動化的郵件翻譯工具，可以讀取Gmail郵件、翻譯成繁體中文、生成Markdown報告並透過Telegram傳送。

## ✨ 功能特色

- 🔐 **安全的Gmail認證** - 符合Google安全標準
- 🔄 **高品質繁體中文翻譯** - 準確流暢的翻譯結果
- 📝 **Markdown報告生成** - 完美支援中文顯示，包含翻譯內容
- 📱 **Telegram自動傳送** - 即時接收翻譯結果
- 🔍 **智能郵件搜尋** - 支援主旨、寄件者、日期篩選
- ⚡ **高速並行翻譯** - 長文本自動分段並行處理
- 🖼️ **連結和圖片處理** - 自動分離連結，保留圖片連結
- 📋 **配置管理系統** - 支援多組搜尋條件管理

## 🚀 快速開始

### 1. 安裝相依套件
```bash
cd email_translator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Gmail認證設定
按照 `gmail_oauth_setup.md` 的詳細步驟：
1. 設定Gmail存取權限
2. 完成必要的認證步驟
3. 儲存認證資訊

### 3. Telegram Bot設定
1. 在Telegram中找 @BotFather 建立機器人
2. 取得Bot Token和Chat ID

### 4. 配置程式設定
```bash
python config_manager.py
```
- 設定Telegram Bot Token和Chat ID
- 新增郵件搜尋條件

### 5. 執行程式
```bash
# 使用預設搜尋條件
python email_translator.py

# 使用特定搜尋條件
python email_translator.py [搜尋條件名稱]
```

## 🔧 配置管理

### 互動式配置管理
```bash
python config_manager.py
```

功能包括：
- 新增/刪除搜尋條件
- 更新Telegram設定
- 管理預設搜尋條件
- 測試搜尋條件

### 搜尋條件範例
```json
{
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
```

## 🔄 翻譯服務

### 高品質翻譯
- 準確流暢的繁體中文翻譯
- 支援專業術語和複雜句型
- 穩定可靠的翻譯服務
- 智能文本清理和連結處理

### 翻譯優化特色
- **並行處理** - 長文本自動分段並行翻譯，速度提升4-6倍
- **智能分段** - 保持段落完整性，避免句子被切斷
- **連結分離** - 自動提取連結，避免翻譯錯誤
- **圖片保留** - 識別並保留圖片連結

## 📝 輸出格式

### Markdown報告
- 完美支援繁體中文顯示
- 包含郵件基本資訊（主旨、寄件者、日期）
- 只保留翻譯後的繁體中文內容
- 自動分離的連結和圖片列表
- 美觀的格式和排版

### 範例輸出
```markdown
# 📧 郵件翻譯報告

## 📋 郵件資訊
- **主旨**: 週報 - AI技術更新
- **寄件者**: tech@company.com
- **日期**: 2025-01-16 10:30:00

## 📝 內容 (繁體中文)
這週我們在人工智慧領域取得了重大進展...

### 🖼️ 圖片連結
1. ![圖片1](https://example.com/chart.png)

### 📎 相關連結
1. https://example.com/report
```

## 🧪 測試工具

### 快速系統檢查
```bash
python quick_test.py
```
檢查項目：
- Python版本
- 必要檔案
- Google認證
- 套件匯入
- 翻譯功能

### 翻譯功能測試
```bash
python simple_translation_test.py
```
測試項目：
- Google翻譯基本功能
- 連結處理功能

## 📁 檔案結構

```
email_translator/
├── email_translator.py          # 主程式
├── config_manager.py            # 配置管理器
├── config.json                  # 實際配置檔案
├── config.json.example          # 配置範例檔案
├── requirements.txt             # 套件清單
├── credentials.json            # Gmail認證檔案
├── token.pickle               # 認證token
├── gmail_oauth_setup.md       # Gmail設定詳細指南
├── setup_guide.md            # 完整設定指南
├── config_usage_guide.md     # 配置使用指南
├── quick_test.py             # 快速測試工具
├── simple_translation_test.py # 翻譯功能測試
├── .gitignore               # Git忽略檔案
└── README.md               # 專案說明
```

## ⚡ 性能特色

### 翻譯速度優化
- **短文本**: ~87 字符/秒
- **中等文本**: ~531 字符/秒 (6x提升)
- **長文本**: ~1225 字符/秒 (14x提升)
- **並行處理**: 4.8倍速度提升

### 智能處理
- 自動文本清理，改善翻譯品質
- 異常字符檢測和修正
- 智能段落分割，保持結構完整
- 連結和圖片自動分離處理

## 🔒 安全性

- 安全的Gmail存取機制
- 只要求郵件「讀取」權限
- 敏感檔案已加入 `.gitignore`
- 支援使用者權限控制
- 配置檔案本地儲存

## 📋 系統需求

- **Python**: 3.7+ (推薦 3.9+)
- **作業系統**: macOS/Linux/Windows
- **網路**: 穩定的網路連線
- **帳戶**: Gmail帳戶、Telegram帳戶
- **記憶體**: 建議 4GB+ (並行翻譯需要)

## 🆘 故障排除

### 常見問題
1. **認證檔案缺失** - 請參考設定指南完成認證
2. **Gmail認證失敗** - 檢查認證設定和使用者權限
3. **翻譯速度慢** - 檢查網路連線，程式會自動優化
4. **Telegram傳送失敗** - 檢查Bot Token和Chat ID設定
5. **中文顯示問題** - Markdown格式完美支援中文，無需額外設定

### 測試和診斷
```bash
# 系統狀態檢查
python quick_test.py

# 翻譯功能測試
python simple_translation_test.py

# 配置檢查
python config_manager.py
```

### 取得協助
- 📖 `gmail_oauth_setup.md` - Gmail認證設定步驟
- 📋 `setup_guide.md` - 完整設定流程
- ⚙️ `config_usage_guide.md` - 配置管理說明

## 🎯 使用場景

### 適合的使用情境
- 📧 **商務郵件翻譯** - 快速理解英文商務郵件
- 📰 **電子報翻譯** - 定期翻譯國外電子報
- 📊 **報告翻譯** - 翻譯技術報告和文件
- 🔔 **通知翻譯** - 翻譯重要通知郵件

### 批次處理範例
```bash
# 翻譯工作報告
python email_translator.py work_reports

# 翻譯帳單郵件
python email_translator.py invoices

# 翻譯技術電子報
python email_translator.py tech_news
```

## 📄 授權

此專案僅供個人學習和使用。請遵守相關服務的使用條款：
- Gmail 使用條款
- Telegram Bot API 使用條款
- 相關翻譯服務條款

---

🎉 **享受高效的自動化郵件翻譯體驗！**

*最後更新: 2025-07-17*