# 📧 郵件翻譯器設定指南

## 🚀 快速開始

### 1. 安裝相依套件
```bash
cd email_translator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Gmail OAuth 2.0 設定
**詳細步驟請參考**: `gmail_oauth_setup.md`

**快速摘要**:
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案並啟用 Gmail API
3. 設定 OAuth 同意畫面
4. 建立 OAuth 2.0 桌面應用程式認證
5. 下載 `credentials.json` 檔案並放在程式資料夾中

### 3. Telegram Bot 設定
1. 在 Telegram 中搜尋 @BotFather
2. 傳送 `/newbot` 建立新機器人
3. 取得 Bot Token 和 Chat ID

### 4. 配置程式設定
```bash
python config_manager.py
```
- 設定 Telegram Bot Token 和 Chat ID
- 新增郵件搜尋條件

### 5. 執行程式
```bash
# 使用預設搜尋條件
python email_translator.py

# 使用特定搜尋條件
python email_translator.py [搜尋條件名稱]
```

## 🔧 翻譯服務

程式使用 **Google翻譯免費版**：
- 高品質翻譯結果
- 支援繁體中文
- 穩定可靠
- 無需額外API金鑰

## 📝 輸出格式

- 使用 **Markdown格式** 輸出
- 完美支援繁體中文顯示
- 自動分離連結和圖片
- 透過 Telegram 自動傳送

## 🆘 故障排除

### 常見問題
1. **找不到credentials.json** - 請從Google Cloud Console下載
2. **OAuth認證失敗** - 檢查OAuth同意畫面設定
3. **Telegram傳送失敗** - 檢查Bot Token和Chat ID

### 測試工具
```bash
# 快速系統檢查
python quick_test.py

# 翻譯功能測試
python simple_translation_test.py
```

## 📚 更多資訊

- `config_usage_guide.md` - 配置管理詳細說明
- `gmail_oauth_setup.md` - Gmail OAuth 詳細設定步驟
- `README.md` - 完整專案說明