#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
郵件翻譯器 - 使用Gmail API讀取郵件、翻譯成繁體中文、存成Markdown並透過Telegram傳送
使用OAuth 2.0認證和免費翻譯API
"""

import os
import pickle
import base64
import email
from email.mime.text import MIMEText
import requests
import json
from datetime import datetime
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class EmailTranslator:
    def __init__(self, config):
        """初始化郵件翻譯器"""
        self.config = config
        self.gmail_service = None
        
        # Gmail API權限範圍
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def authenticate_gmail(self):
        """Gmail OAuth 2.0 認證"""
        creds = None
        
        # 檢查是否有已儲存的認證token
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # 如果沒有有效認證或token過期，進行OAuth流程
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Token已更新")
                except Exception as e:
                    print(f"⚠️ Token更新失敗: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists('credentials.json'):
                    print("❌ 找不到 credentials.json 檔案")
                    print("請到 Google Cloud Console 下載OAuth 2.0認證檔案")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ OAuth認證完成")
            
            # 儲存認證token供下次使用
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            # 建立Gmail API服務
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            print("✅ Gmail API連接成功")
            return True
        except Exception as e:
            print(f"❌ Gmail API連接失敗: {e}")
            return False
    
    def search_emails(self, search_criteria):
        """使用Gmail API搜尋郵件"""
        try:
            # 建立搜尋查詢
            query_parts = []
            
            if search_criteria.get('subject'):
                query_parts.append(f'subject:"{search_criteria["subject"]}"')
            
            if search_criteria.get('sender'):
                query_parts.append(f'from:{search_criteria["sender"]}')
            
            if search_criteria.get('date_after'):
                query_parts.append(f'after:{search_criteria["date_after"]}')
            
            query = ' '.join(query_parts) if query_parts else 'in:inbox'
            
            print(f"🔍 搜尋條件: {query}")
            
            # 執行搜尋
            results = self.gmail_service.users().messages().list(
                userId='me', q=query, maxResults=10).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("❌ 找不到符合條件的郵件")
                return []
            
            print(f"📧 找到 {len(messages)} 封郵件")
            return messages
            
        except HttpError as error:
            print(f"❌ Gmail API搜尋錯誤: {error}")
            return []
    
    def get_email_content(self, message_id):
        """取得郵件內容"""
        try:
            # 取得完整郵件
            message = self.gmail_service.users().messages().get(
                userId='me', id=message_id, format='full').execute()
            
            # 解析郵件標頭
            headers = message['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            
            # 取得郵件內容
            content = self.extract_message_content(message['payload'])
            
            return {
                'subject': subject,
                'sender': sender,
                'content': content,
                'date': date
            }
            
        except HttpError as error:
            print(f"❌ 取得郵件內容失敗: {error}")
            return None
    
    def extract_message_content(self, payload):
        """從郵件payload中提取文字內容"""
        content = ""
        
        if 'parts' in payload:
            # 多部分郵件
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        content = base64.urlsafe_b64decode(
                            part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'multipart/alternative':
                    content = self.extract_message_content(part)
                    if content:
                        break
        else:
            # 單一部分郵件
            if payload['mimeType'] == 'text/plain':
                if 'data' in payload['body']:
                    content = base64.urlsafe_b64decode(
                        payload['body']['data']).decode('utf-8')
        
        return content    

    def translate_to_chinese(self, text):
        """自動偵測語言並翻譯成繁體中文 - 使用免費翻譯API"""
        if len(text) > 1000:
            return self.translate_long_text(text)
        
        translation_methods = [
            self.translate_with_google_free     # Google翻譯免費版 (主要且最穩定)
        ]
        
        for method in translation_methods:
            try:
                result = method(text)
                if result and result != text and len(result) > 0:
                    print(f"✅ 翻譯成功使用: {method.__name__}")
                    return result
            except Exception as e:
                print(f"❌ {method.__name__} 失敗: {e}")
                continue
        
        print("⚠️ 所有翻譯服務都失敗，返回原文")
        return text
    
    def translate_long_text(self, text):
        """處理長文本翻譯 - 優化速度版本"""
        # 使用更大的分塊大小，減少API調用次數
        max_chunk_size = 2000  # 增加到2000字符
        
        # 如果文本不是很長，直接翻譯
        if len(text) <= max_chunk_size:
            return self.translate_single_chunk(text)
        
        # 智能分段：優先保持段落完整性
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # 如果加入這個段落後不會超過限制，就加入
            if len(current_chunk + paragraph) <= max_chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                # 如果當前塊不為空，先保存
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # 如果單個段落太長，需要進一步分割
                if len(paragraph) > max_chunk_size:
                    # 按句子分割長段落
                    sentences = self.split_into_sentences(paragraph)
                    temp_chunk = ""
                    
                    for sentence in sentences:
                        if len(temp_chunk + sentence) <= max_chunk_size:
                            temp_chunk += sentence + " "
                        else:
                            if temp_chunk.strip():
                                chunks.append(temp_chunk.strip())
                            temp_chunk = sentence + " "
                    
                    if temp_chunk.strip():
                        current_chunk = temp_chunk
                    else:
                        current_chunk = ""
                else:
                    current_chunk = paragraph + '\n\n'
        
        # 處理最後一個塊
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # 並行翻譯（使用線程池）
        return self.translate_chunks_parallel(chunks)
    
    def translate_chunks_parallel(self, chunks):
        """並行翻譯多個文本塊 - 大幅提升速度"""
        if len(chunks) == 1:
            return self.translate_single_chunk(chunks[0])
        
        print(f"🚀 使用並行翻譯處理 {len(chunks)} 個文本塊...")
        translated_chunks = [''] * len(chunks)  # 預分配結果列表
        
        # 使用線程池並行處理
        max_workers = min(6, len(chunks))  # 增加到6個並行線程，進一步提升速度
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有翻譯任務
            future_to_index = {
                executor.submit(self.translate_single_chunk_with_retry, chunk): i 
                for i, chunk in enumerate(chunks)
            }
            
            # 收集結果
            completed = 0
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    translated_chunks[index] = result
                    completed += 1
                    print(f"✅ 完成 {completed}/{len(chunks)} 個文本塊")
                except Exception as e:
                    print(f"❌ 文本塊 {index+1} 翻譯失敗: {e}")
                    translated_chunks[index] = chunks[index]  # 使用原文
        
        return '\n\n'.join(translated_chunks)
    
    def translate_single_chunk_with_retry(self, text):
        """帶重試機制的單塊翻譯"""
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                result = self.translate_single_chunk(text)
                if result and result != text:
                    return result
            except Exception as e:
                if attempt < max_retries:
                    time.sleep(0.5)  # 短暫延遲後重試
                    continue
                else:
                    raise e
        
        return text  # 所有重試都失敗，返回原文
    
    def split_into_sentences(self, text):
        """將文本分割成句子"""
        # 使用更智能的句子分割
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def group_sentences_into_chunks(self, sentences, max_length=600):
        """將句子組合成適當大小的塊"""
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_single_chunk(self, text):
        """翻譯單個文本塊"""
        # 避免遞歸調用translate_to_chinese
        translation_methods = [
            self.translate_with_google_free     # Google翻譯免費版（唯一且最穩定）
        ]
        
        for method in translation_methods:
            try:
                result = method(text)
                if result and result != text and len(result) > 0:
                    return result
            except Exception as e:
                continue
        
        return text  # 如果所有方法都失敗，返回原文
    

    
    def translate_with_google_free(self, text):
        """使用Google翻譯免費版（透過googletrans套件）- 支援自動語言偵測"""
        try:
            from googletrans import Translator
            translator = Translator()
            
            # 清理文本並提取連結
            cleaned_text, links, image_links = self.clean_text_for_translation(text)
            
            # 自動偵測語言
            detected = translator.detect(cleaned_text)
            detected_lang = detected.lang
            confidence = detected.confidence if detected.confidence is not None else 0.0
            
            print(f"🔍 偵測到語言: {detected_lang} (信心度: {confidence:.2f})")
            
            # 如果已經是繁體中文，直接返回
            if detected_lang == 'zh-tw' or detected_lang == 'zh':
                print("✅ 文本已經是中文，無需翻譯")
                return text
            
            # 執行翻譯 - 自動偵測來源語言
            result = translator.translate(cleaned_text, src='auto', dest='zh-tw')
            
            # 確保返回的是繁體中文
            translated_text = result.text
            
            # 檢查翻譯結果是否包含異常字符
            if self.contains_invalid_chars(translated_text):
                print("⚠️ 翻譯結果包含異常字符，嘗試重新翻譯...")
                # 嘗試使用簡體中文再轉換
                result_cn = translator.translate(cleaned_text, src='auto', dest='zh-cn')
                # 將簡體轉繁體
                result_tw = translator.translate(result_cn.text, src='zh-cn', dest='zh-tw')
                translated_text = result_tw.text
            
            # 處理連結佔位符並添加連結列表
            final_text = self.restore_links_in_translation(translated_text, links, image_links)
            
            return final_text
            
        except ImportError:
            raise Exception("需要安裝 googletrans: pip install googletrans==4.0.0rc1")
        except Exception as e:
            raise Exception(f"Google翻譯失敗: {e}")
    

    def clean_text_for_translation(self, text):
        """清理文本以改善翻譯品質"""
        # 提取並分類連結，避免重複
        links = []
        image_links = []
        seen_links = set()  # 用於追蹤已見過的連結
        seen_images = set()  # 用於追蹤已見過的圖片
        
        # 圖檔連結模式（包含常見圖檔格式）
        image_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.(?:jpg|jpeg|png|gif|bmp|webp|svg)(?:\?[^\s<>"{}|\\^`\[\]]*)?'
        
        # 一般連結模式 - 更寬鬆的匹配
        general_link_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+(?:[^\s<>"{}|\\^`\[\].,;!?\)\]]|[.,;!?](?!\s))*'
        
        def replace_image_link(match):
            link = match.group(0)
            if link not in seen_images:
                seen_images.add(link)
                image_links.append(link)
                return f' [IMAGE_{len(image_links)-1}] '
            else:
                # 如果是重複的圖片連結，找到它的索引
                try:
                    index = image_links.index(link)
                    return f' [IMAGE_{index}] '
                except ValueError:
                    return f' [IMAGE_{len(image_links)-1}] '
        
        def replace_general_link(match):
            link = match.group(0)
            # 檢查是否已經是圖檔連結
            if not re.match(image_pattern, link):
                if link not in seen_links:
                    seen_links.add(link)
                    links.append(link)
                    return f' [LINK_{len(links)-1}] '
                else:
                    # 如果是重複的連結，找到它的索引
                    try:
                        index = links.index(link)
                        return f' [LINK_{index}] '
                    except ValueError:
                        return f' [LINK_{len(links)-1}] '
            return match.group(0)  # 保持圖檔連結不變
        
        # 先處理圖檔連結
        cleaned = re.sub(image_pattern, replace_image_link, text)
        
        # 再處理一般連結
        cleaned = re.sub(general_link_pattern, replace_general_link, cleaned)
        
        # 移除多餘的空白和換行
        cleaned = re.sub(r'\s+', ' ', cleaned.strip())
        
        # 移除特殊字符但保留基本標點和佔位符
        cleaned = re.sub(r'[^\w\s.,!?;:()\-\'"@/\[\]_]', ' ', cleaned)
        
        # 移除多餘空格
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip(), links, image_links
    
    def contains_invalid_chars(self, text):
        """檢查文本是否包含異常字符（如黑色方塊）"""
        # 檢查是否包含替換字符或其他異常字符
        invalid_patterns = [
            r'[\ufffd]',  # 替換字符
            r'[■□▪▫]',   # 方塊字符
            r'[\u2588-\u259f]',  # 方塊字符範圍
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def restore_links_in_translation(self, translated_text, links, image_links=None):
        """在翻譯結果中恢復連結並格式化 - 只顯示實際被引用的連結"""
        result = translated_text
        used_links = []  # 記錄實際被使用的連結
        used_images = []  # 記錄實際被使用的圖片
        link_mapping = {}  # 記錄原始索引到新索引的映射
        
        # 先掃描文本，找出實際存在的連結引用
        import re
        
        # 尋找所有可能的連結引用格式
        link_patterns = [
            r'\[LINK_(\d+)\]',
            r'\[link_(\d+)\]', 
            r'\[Link_(\d+)\]',
            r'\(連結\s*(\d+)\)',
            r'（連結\s*(\d+)）',
            r'\[連結(\d+)\]',
            r'\(連結(\d+)\)',
            r'（連結(\d+)）'
        ]
        
        found_link_indices = set()
        for pattern in link_patterns:
            matches = re.findall(pattern, result)
            for match in matches:
                try:
                    # 將字符串轉換為整數，並調整為0基索引
                    original_index = int(match) - 1 if pattern.startswith(r'\[連結') or '連結' in pattern else int(match)
                    if 0 <= original_index < len(links):
                        found_link_indices.add(original_index)
                except (ValueError, IndexError):
                    continue
        
        # 對找到的索引進行排序
        sorted_indices = sorted(found_link_indices)
        
        # 建立映射關係
        for new_index, original_index in enumerate(sorted_indices):
            link_mapping[original_index] = new_index + 1
            used_links.append(links[original_index])
        
        # 處理圖片連結佔位符
        if image_links:
            image_patterns = [
                r'\[IMAGE_(\d+)\]',
                r'\[image_(\d+)\]',
                r'\[Image_(\d+)\]'
            ]
            
            found_image_indices = set()
            for pattern in image_patterns:
                matches = re.findall(pattern, result)
                for match in matches:
                    try:
                        original_index = int(match)
                        if 0 <= original_index < len(image_links):
                            found_image_indices.add(original_index)
                    except (ValueError, IndexError):
                        continue
            
            sorted_image_indices = sorted(found_image_indices)
            for new_index, original_index in enumerate(sorted_image_indices):
                used_images.append(image_links[original_index])
                
                # 替換圖片佔位符
                placeholders = [
                    f'[IMAGE_{original_index}]',
                    f'[image_{original_index}]',
                    f'[Image_{original_index}]'
                ]
                reference = f'[圖片{new_index + 1}]'
                
                for placeholder in placeholders:
                    if placeholder in result:
                        result = result.replace(placeholder, reference)
                        break
        
        # 替換連結佔位符
        for original_index, new_index in link_mapping.items():
            # 所有可能的佔位符格式
            placeholders = [
                f'[LINK_{original_index}]',
                f'[link_{original_index}]',
                f'[Link_{original_index}]',
                f'(連結 {original_index + 1})',
                f'（連結 {original_index + 1}）',
                f'[連結{original_index + 1}]',
                f'(連結{original_index + 1})',
                f'（連結{original_index + 1}）'
            ]
            
            reference = f'[連結{new_index}]'
            
            for placeholder in placeholders:
                if placeholder in result:
                    result = result.replace(placeholder, reference)
        
        # 清理多餘空格
        result = re.sub(r'\s+', ' ', result.strip())
        
        # 只添加實際被使用的圖檔連結
        if used_images:
            result += "\n\n### 🖼️ 圖片連結\n\n"
            for i, image_link in enumerate(used_images, 1):
                result += f"{i}. ![圖片{i}]({image_link})\n"
        
        # 只添加實際被使用的一般連結
        if used_links:
            result += "\n\n### 📎 相關連結\n\n"
            for i, link in enumerate(used_links, 1):
                result += f"{i}. {link}\n"
        
        return result
    

    
    def create_markdown(self, email_data, translated_content, filename):
        """建立Markdown檔案 - 只包含繁體中文翻譯內容"""
        try:
            # 建立Markdown內容
            markdown_content = f"""# 📧 郵件翻譯報告

## 📋 郵件資訊

- **主旨**: {email_data['subject']}
- **寄件者**: {email_data['sender']}
- **日期**: {email_data['date']}
- **翻譯時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📝 內容 (繁體中文)

{translated_content}

---

*由郵件翻譯器自動生成*
"""
            
            # 寫入檔案
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ Markdown檔案已建立: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ 建立Markdown檔案失敗: {e}")
            return False
    
    def send_telegram_message(self, file_path):
        """透過Telegram傳送檔案"""
        try:
            bot_token = self.config['telegram_bot_token']
            chat_id = self.config['telegram_chat_id']
            
            # 判斷檔案類型
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.md':
                file_type = 'Markdown檔案'
                emoji = '📝'
            else:
                file_type = 'PDF檔案'
                emoji = '📄'
            
            message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            message_data = {
                'chat_id': chat_id,
                'text': f'📧 郵件翻譯完成！{emoji} {file_type}如下：'
            }
            requests.post(message_url, data=message_data)
            
            document_url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {'chat_id': chat_id}
                response = requests.post(document_url, files=files, data=data)
            
            if response.status_code == 200:
                print(f"✅ {file_type}已成功透過Telegram傳送")
                return True
            else:
                print(f"❌ Telegram傳送失敗: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram傳送錯誤: {e}")
            return False
    
    def process_email(self, search_criteria):
        """主要處理流程"""
        print("🚀 開始處理郵件...")
        
        # 1. Gmail認證
        if not self.authenticate_gmail():
            return False
        
        try:
            # 2. 搜尋郵件
            messages = self.search_emails(search_criteria)
            if not messages:
                return False
            
            # 取得最新的郵件
            latest_message = messages[0]
            print(f"📧 處理最新的郵件")
            
            # 3. 讀取郵件內容
            email_data = self.get_email_content(latest_message['id'])
            if not email_data:
                return False
            
            print(f"📖 正在處理郵件: {email_data['subject']}")
            
            # 4. 翻譯內容
            print("🔄 正在翻譯...")
            translated_content = self.translate_to_chinese(email_data['content'])
            
            # 5. 校對與潤飾翻譯
            print("📝 正在校對翻譯...")
            try:
                from translation_proofreader import TranslationProofreader
                proofreader = TranslationProofreader()
                proofread_result = proofreader.enhance_translation_quality(
                    email_data['content'], translated_content
                )
                translated_content = proofread_result['proofread']
                
                if proofread_result['improvements']:
                    print(f"✅ 翻譯校對完成，改進了 {len(proofread_result['improvements'])} 個地方")
                    for improvement in proofread_result['improvements'][:3]:  # 只顯示前3個改進
                        print(f"   - {improvement}")
                else:
                    print("✅ 翻譯品質良好，無需校對")
            except ImportError:
                print("⚠️ 校對模組未找到，跳過校對步驟")
            except Exception as e:
                print(f"⚠️ 校對過程出錯，使用原翻譯: {e}")
            
            # 5. 建立Markdown檔案
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            markdown_filename = f"email_translation_{timestamp}.md"
            print(f"� 正在建立PMarkdown檔案: {markdown_filename}")
            
            if self.create_markdown(email_data, translated_content, markdown_filename):
                print("✅ Markdown檔案建立成功")
                
                # 6. 透過Telegram傳送
                print("📤 正在透過Telegram傳送...")
                if self.send_telegram_message(markdown_filename):
                    print("🎉 處理完成！")
                    return True
                else:
                    print("❌ Telegram傳送失敗")
                    return False
            else:
                print("❌ Markdown檔案建立失敗")
                return False
                
        except Exception as e:
            print(f"❌ 處理過程發生錯誤: {e}")
            return False

def main():
    """主程式"""
    import sys
    from config_manager import ConfigManager
    
    # 載入配置
    config_manager = ConfigManager()
    
    # 檢查命令列參數
    search_name = None
    if len(sys.argv) > 1:
        search_name = sys.argv[1]
        print(f"🔍 使用搜尋條件: {search_name}")
    else:
        print("🔍 使用預設搜尋條件")
        print("💡 提示: 可以使用 python email_translator.py [搜尋條件名稱] 來指定特定搜尋條件")
    
    # 取得搜尋條件
    search_criteria = config_manager.get_search_criteria(search_name)
    
    # 檢查搜尋條件是否有效
    if not any(search_criteria.values()):
        print("❌ 搜尋條件為空，請先設定搜尋條件")
        print("💡 執行 python config_manager.py 來設定搜尋條件")
        return
    
    print("📧 使用的搜尋條件:")
    for key, value in search_criteria.items():
        if value:
            print(f"   {key}: {value}")
    
    # 建立程式配置
    telegram_config = config_manager.get_telegram_config()
    translation_config = config_manager.get_translation_config()
    
    config = {
        'telegram_bot_token': telegram_config.get('bot_token', ''),
        'telegram_chat_id': telegram_config.get('chat_id', ''),
        'deepl_api_key': translation_config.get('deepl_api_key', '')
    }
    
    # 檢查必要設定
    if not config['telegram_bot_token'] or config['telegram_bot_token'] == '[your_bot_token]':
        print("❌ 請先設定Telegram Bot Token")
        print("💡 執行 python config_manager.py 來設定Telegram資訊")
        return
    
    if not config['telegram_chat_id'] or config['telegram_chat_id'] == '[your_chat_id]':
        print("❌ 請先設定Telegram Chat ID")
        print("💡 執行 python config_manager.py 來設定Telegram資訊")
        return
    
    # 建立翻譯器並執行
    translator = EmailTranslator(config)
    success = translator.process_email(search_criteria)
    
    if success:
        print("🎊 郵件翻譯和傳送完成！")
    else:
        print("💥 處理過程中發生錯誤")

if __name__ == "__main__":
    main()