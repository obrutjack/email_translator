# Gmail OAuth 2.0 詳細設定指南

## 🔐 為什麼要使用OAuth 2.0？
Google已經停止支援應用程式密碼的方式，現在需要使用更安全的OAuth 2.0認證。

## 📋 詳細設定步驟

### 步驟1: 建立Google Cloud專案

#### 1.1 進入Google Cloud Console
1. 開啟瀏覽器，前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 使用你的Google帳戶登入（建議使用要讀取郵件的那個Gmail帳戶）

#### 1.2 建立新專案
1. 在頁面頂部，點選專案選擇器（通常顯示「選取專案」或現有專案名稱）
2. 在彈出視窗中，點選右上角的「新增專案」按鈕
3. 填寫專案資訊：
   - **專案名稱**: `郵件翻譯器` 或 `Email Translator`
   - **位置**: 保持預設（無機構）
4. 點選「建立」按鈕
5. 等待專案建立完成（通常需要10-30秒）
6. 確認頁面頂部顯示你剛建立的專案名稱

### 步驟2: 啟用Gmail API

#### 2.1 進入API程式庫
1. 在Google Cloud Console左側選單中，點選「API和服務」
2. 點選「已啟用的API和服務」或「程式庫」
3. 如果看不到左側選單，點選左上角的「☰」（漢堡選單）圖示

#### 2.2 搜尋並啟用Gmail API
1. 在API程式庫頁面，使用搜尋框搜尋「Gmail API」
2. 點選搜尋結果中的「Gmail API」
3. 在Gmail API頁面，點選藍色的「啟用」按鈕
4. 等待API啟用完成
5. 啟用後會自動跳轉到API詳情頁面

### 步驟3: 設定OAuth同意畫面

#### 3.1 進入OAuth同意畫面設定
1. 在左側選單中，點選「API和服務」→「OAuth同意畫面」
2. 如果這是第一次設定，會看到用戶類型選擇頁面

#### 3.2 選擇用戶類型
1. 選擇「外部」（External）
   - **注意**: 即使選擇「外部」，你仍然可以限制只有特定使用者可以使用
   - 「內部」選項只適用於Google Workspace組織
2. 點選「建立」按鈕

#### 3.3 填寫OAuth同意畫面資訊
**第1頁 - 應用程式資訊**:
1. **應用程式名稱**: `郵件翻譯器`
2. **用戶支援電子郵件**: 選擇你的Gmail地址
3. **應用程式標誌**: 可以跳過（非必填）
4. **應用程式首頁**: 可以跳過（非必填）
5. **應用程式隱私權政策連結**: 可以跳過（非必填）
6. **應用程式服務條款連結**: 可以跳過（非必填）
7. **已授權網域**: 可以跳過（非必填）
8. **開發人員聯絡資訊**: 輸入你的Gmail地址
9. 點選「儲存並繼續」

**第2頁 - 範圍（Scopes）**:
1. 這個頁面可以保持空白
2. 我們會在程式碼中指定需要的權限範圍
3. 點選「儲存並繼續」

**第3頁 - 測試使用者**:
1. 點選「+ 新增使用者」
2. 輸入你的Gmail地址（要讀取郵件的那個帳戶）
3. 點選「新增」
4. 點選「儲存並繼續」

**第4頁 - 摘要**:
1. 檢查設定是否正確
2. 點選「返回資訊主頁」

### 步驟4: 建立OAuth 2.0認證

#### 4.1 進入憑證頁面
1. 在左側選單中，點選「API和服務」→「憑證」

#### 4.2 建立OAuth 2.0用戶端ID
1. 點選頁面頂部的「+ 建立憑證」按鈕
2. 從下拉選單中選擇「OAuth 2.0用戶端ID」

#### 4.3 設定應用程式類型
1. **應用程式類型**: 選擇「桌面應用程式」
2. **名稱**: 輸入 `郵件翻譯器桌面版` 或 `Email Translator Desktop`
3. 點選「建立」按鈕

#### 4.4 下載認證檔案
1. 建立完成後會彈出「OAuth用戶端已建立」對話框
2. 點選「下載JSON」按鈕下載認證檔案
3. **重要**: 將下載的檔案重新命名為 `credentials.json`
4. 將 `credentials.json` 檔案移動到你的程式資料夾中（與 `email_translator.py` 同一個資料夾）

### 步驟5: 驗證設定

#### 5.1 檢查檔案結構
確認你的專案資料夾包含以下檔案：
```
your_project/
├── email_translator.py
├── requirements.txt
├── credentials.json          # 剛下載的認證檔案
├── gmail_oauth_setup.md
└── setup_guide.md
```

#### 5.2 檢查credentials.json內容
1. 用文字編輯器開啟 `credentials.json`
2. 確認檔案包含類似以下結構的JSON內容：
```json
{
  "installed": {
    "client_id": "your-client-id.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

### 步驟6: 重要注意事項

#### 6.1 安全性
- **絕對不要**將 `credentials.json` 檔案分享給他人
- **絕對不要**將此檔案上傳到公開的程式碼庫（如GitHub）
- 建議在 `.gitignore` 檔案中加入 `credentials.json` 和 `token.pickle`

#### 6.2 測試使用者限制
- 由於應用程式處於「測試」狀態，只有你加入的測試使用者可以使用
- 如果需要其他人使用，需要將他們的Gmail地址加入測試使用者清單
- 或者申請Google的應用程式驗證（適用於公開發布的應用程式）

#### 6.3 權限範圍
- 我們的程式只要求「只讀」Gmail權限
- 程式無法修改、刪除或傳送郵件
- 這是最安全的權限設定

### 步驟7: 常見問題排除

#### 問題1: 找不到「API和服務」選單
**解決方法**: 點選左上角的「☰」圖示展開選單

#### 問題2: 無法建立專案
**解決方法**: 
- 確認已登入正確的Google帳戶
- 檢查帳戶是否有建立專案的權限
- 嘗試使用不同的專案名稱

#### 問題3: Gmail API啟用失敗
**解決方法**:
- 確認已選擇正確的專案
- 重新整理頁面後再試一次
- 檢查網路連線

#### 問題4: OAuth同意畫面設定錯誤
**解決方法**:
- 確認選擇「外部」用戶類型
- 必填欄位都要填寫
- 測試使用者必須加入你的Gmail地址

#### 問題5: 下載的JSON檔案無法使用
**解決方法**:
- 確認檔案名稱是 `credentials.json`
- 確認檔案內容是有效的JSON格式
- 重新下載認證檔案

### 步驟5: 安裝相依套件
```bash
pip install -r requirements.txt
```

### 步驟6: 修改程式設定
編輯 `email_translator.py` 中的設定：
```python
config = {
    # Telegram設定
    'telegram_bot_token': 'your_actual_bot_token',
    'telegram_chat_id': 'your_actual_chat_id',
    
    # 可選設定
    'deepl_api_key': '',  # DeepL免費API (可選)
    'chinese_font_path': '/System/Library/Fonts/PingFang.ttc'
}

search_criteria = {
    'subject': 'your_email_subject_keyword',
    'sender': 'sender@example.com',  # 可選
    # 'date_after': '2024/12/01'  # 可選
}
```

### 步驟7: 首次執行認證
```bash
python email_translator.py
```

首次執行時會：
1. 自動開啟瀏覽器
2. 要求你登入Google帳戶
3. 顯示權限請求畫面
4. 點選「允許」授權程式讀取Gmail
5. 認證完成後，會自動儲存token供下次使用

## 📁 檔案結構
執行後你的資料夾應該包含：
```
your_project/
├── email_translator.py
├── requirements.txt
├── credentials.json          # Google OAuth認證檔案
├── token.pickle             # 自動產生的認證token
├── gmail_oauth_setup.md
└── setup_guide.md
```

## 🔍 搜尋語法說明

### 基本搜尋
```python
# 按主旨搜尋
search_criteria = {'subject': 'invoice'}

# 按寄件者搜尋  
search_criteria = {'sender': 'noreply@company.com'}

# 按日期搜尋 (YYYY/MM/DD格式)
search_criteria = {'date_after': '2024/12/01'}
```

### 組合搜尋
```python
search_criteria = {
    'subject': 'monthly report',
    'sender': 'boss@company.com',
    'date_after': '2024/12/01'
}
```

### Gmail搜尋運算子
你也可以使用Gmail的進階搜尋語法：
- `has:attachment` - 有附件的郵件
- `is:unread` - 未讀郵件
- `is:important` - 重要郵件
- `label:inbox` - 收件匣中的郵件

## ⚠️ 常見問題

### 問題1: 找不到credentials.json
- 確認已從Google Cloud Console下載OAuth認證檔案
- 檔案名稱必須是 `credentials.json`
- 檔案必須放在程式的同一個資料夾

### 問題2: OAuth認證失敗
- 確認已啟用Gmail API
- 確認已設定OAuth同意畫面
- 確認你的Gmail地址已加入測試使用者

### 問題3: 權限被拒絕
- 檢查OAuth同意畫面的設定
- 確認應用程式狀態不是「需要驗證」
- 重新執行認證流程

### 問題4: Token過期
- 程式會自動更新token
- 如果自動更新失敗，刪除 `token.pickle` 重新認證

## 🔒 安全性說明
- `credentials.json` 包含敏感資訊，不要分享給他人
- `token.pickle` 包含你的認證token，也不要分享
- 建議將這些檔案加入 `.gitignore` 如果你使用版本控制

## 🎯 優點
- ✅ 更安全的認證方式
- ✅ 不需要應用程式密碼
- ✅ 支援自動token更新
- ✅ 符合Google最新安全標準
- ✅ 可以精確控制權限範圍