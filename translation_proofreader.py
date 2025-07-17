#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻譯校對與潤飾模組
使用多種免費方案來改善翻譯品質
"""

import re
import requests
import json
from typing import List, Dict, Optional
import time

class TranslationProofreader:
    def __init__(self):
        """初始化校對器"""
        self.common_errors = {
            # 台灣用語風格修正
            "消息": "訊息",  # 台灣習慣用「訊息」
            "信息": "資訊",  # 台灣習慣用「資訊」
            "文件": "檔案",  # 台灣習慣用「檔案」
            "软件": "軟體",  # 繁體字修正
            "硬件": "硬體",  # 繁體字修正
            "网络": "網路",  # 台灣習慣用「網路」
            "网站": "網站",  # 繁體字修正
            "计算机": "電腦",  # 台灣習慣用「電腦」
            "手机": "手機",  # 繁體字修正
            "程序": "程式",  # 台灣習慣用「程式」
            "数据": "資料",  # 台灣習慣用「資料」
            "视频": "影片",  # 台灣習慣用「影片」
            "音频": "音訊",  # 台灣習慣用「音訊」
        }
        
        self.punctuation_fixes = {
            # 標點符號修正
            "。。": "。",
            "？？": "？",
            "！！": "！",
            "，，": "，",
        }
    
    def proofread_translation(self, text: str, method: str = "multi") -> Dict[str, str]:
        """
        校對翻譯文本
        
        Args:
            text: 需要校對的翻譯文本
            method: 校對方法 ('basic', 'gemini', 'multi')
        
        Returns:
            包含原文、校對後文本和改進建議的字典
        """
        result = {
            "original": text,
            "proofread": text,
            "improvements": [],
            "method_used": method
        }
        
        if method == "basic":
            result = self._basic_proofreading(result)
        elif method == "gemini":
            result = self._gemini_proofreading(result)
        elif method == "multi":
            # 先基本校對，再用 AI 校對
            result = self._basic_proofreading(result)
            result = self._gemini_proofreading(result)
        
        return result
    
    def _basic_proofreading(self, result: Dict[str, str]) -> Dict[str, str]:
        """基本校對：修正常見錯誤和格式問題"""
        text = result["proofread"]
        improvements = result["improvements"]
        
        # 1. 修正常見翻譯錯誤
        for wrong, correct in self.common_errors.items():
            if wrong in text:
                text = text.replace(wrong, correct)
                improvements.append(f"用詞統一：{wrong} → {correct}")
        
        # 2. 修正標點符號
        for wrong, correct in self.punctuation_fixes.items():
            if wrong in text:
                text = text.replace(wrong, correct)
                improvements.append(f"標點修正：{wrong} → {correct}")
        
        # 3. 移除多餘空格
        original_text = text
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'\s*([，。！？；：])\s*', r'\1', text)
        if text != original_text:
            improvements.append("移除多餘空格和標點前後空格")
        
        # 4. 修正常見語法問題
        grammar_fixes = [
            (r'的的', '的'),
            (r'了了', '了'),
            (r'在在', '在'),
            (r'是是', '是'),
        ]
        
        for pattern, replacement in grammar_fixes:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
                improvements.append(f"語法修正：{pattern} → {replacement}")
        
        result["proofread"] = text
        result["improvements"] = improvements
        return result
    
    def _gemini_proofreading(self, result: Dict[str, str]) -> Dict[str, str]:
        """使用 Google Gemini 進行 AI 校對"""
        try:
            # 嘗試從環境變數或配置檔案取得 API Key
            import os
            api_key = os.getenv('GEMINI_API_KEY')
            
            # 如果環境變數沒有，嘗試從配置檔案讀取
            if not api_key:
                try:
                    with open('gemini_apikey.json', 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        api_key = config.get('api_key')
                except FileNotFoundError:
                    pass
            
            if not api_key or api_key == "your_gemini_api_key_here":
                print("⚠️ 未設定 GEMINI_API_KEY，跳過 AI 校對")
                print("💡 請設定環境變數或建立 gemini_apikey.json 檔案")
                return result
            
            text = result["proofread"]
            
            # 構建校對提示
            prompt = f"""
請幫我校對以下繁體中文翻譯，改善語法、用詞和流暢度，使用台灣地區的用語習慣：

原文：
{text}

請提供：
1. 校對後的文本
2. 主要改進點

台灣用語要求：
- 使用「資訊」而非「信息」
- 使用「訊息」而非「消息」  
- 使用「檔案」而非「文件」
- 使用「軟體」而非「軟件」
- 使用「網路」而非「網絡」
- 使用「電腦」而非「計算機」
- 使用「程式」而非「程序」
- 使用「資料」而非「數據」
- 使用「影片」而非「視頻」
- 使用繁體中文字形
- 語言自然流暢，符合台灣人說話習慣
- 保持原意不變

請直接提供校對後的完整文本，然後列出主要改進點。
"""
            
            # 調用 Gemini API (使用最新格式)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 1000
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                if 'candidates' in response_data and len(response_data['candidates']) > 0:
                    ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
                    
                    # 解析 AI 回應
                    improved_text, improvements = self._parse_ai_response(ai_response, text)
                    
                    if improved_text and improved_text != text:
                        result["proofread"] = improved_text
                        result["improvements"].extend(improvements)
                        result["improvements"].append("AI 校對完成")
                    
            else:
                print(f"⚠️ Gemini API 調用失敗: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ AI 校對失敗: {e}")
        
        return result
    
    def _parse_ai_response(self, ai_response: str, original_text: str) -> tuple:
        """解析 AI 回應，提取改進後的文本和改進點"""
        try:
            # 簡單的解析邏輯，可以根據實際回應格式調整
            lines = ai_response.strip().split('\n')
            
            improved_text = ""
            improvements = []
            
            current_section = ""
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if "校對後" in line or "改進後" in line:
                    current_section = "text"
                elif "改進點" in line or "主要改進" in line:
                    current_section = "improvements"
                elif current_section == "text" and not line.startswith(('1.', '2.', '3.', '-', '*')):
                    if len(line) > 10:  # 避免標題行
                        improved_text = line
                elif current_section == "improvements":
                    if line.startswith(('1.', '2.', '3.', '-', '*')):
                        improvements.append(line)
            
            # 如果沒有找到明確的改進文本，嘗試提取最長的句子
            if not improved_text:
                longest_line = max(lines, key=len, default="")
                if len(longest_line) > len(original_text) * 0.5:
                    improved_text = longest_line
            
            return improved_text, improvements
            
        except Exception as e:
            print(f"⚠️ 解析 AI 回應失敗: {e}")
            return "", []
    
    def compare_translations(self, translations: List[str]) -> Dict[str, str]:
        """比較多個翻譯結果，選擇最佳版本"""
        if not translations:
            return {"best": "", "reason": "無翻譯結果"}
        
        if len(translations) == 1:
            return {"best": translations[0], "reason": "僅有一個翻譯結果"}
        
        # 簡單的評分機制
        scores = []
        for trans in translations:
            score = 0
            
            # 長度合理性 (不要太短或太長)
            length_ratio = len(trans) / max(len(t) for t in translations)
            if 0.8 <= length_ratio <= 1.2:
                score += 2
            
            # 標點符號使用
            if re.search(r'[，。！？]', trans):
                score += 1
            
            # 避免重複字詞
            words = list(trans)
            unique_ratio = len(set(words)) / len(words) if words else 0
            score += unique_ratio * 2
            
            # 避免明顯錯誤
            if not re.search(r'[■□▪▫\ufffd]', trans):
                score += 2
            
            scores.append(score)
        
        best_index = scores.index(max(scores))
        best_translation = translations[best_index]
        
        return {
            "best": best_translation,
            "reason": f"評分最高 ({max(scores):.1f}分)",
            "all_scores": dict(zip(translations, scores))
        }
    
    def enhance_translation_quality(self, original_text: str, translated_text: str) -> Dict[str, str]:
        """綜合提升翻譯品質"""
        print("🔍 開始翻譯品質提升...")
        
        # 分離主要內容和連結區塊
        main_content, links_section = self._separate_content_and_links(translated_text)
        
        # 1. 基本校對（只處理主要內容）
        result = self.proofread_translation(main_content, method="basic")
        print(f"✅ 基本校對完成，發現 {len(result['improvements'])} 個改進點")
        
        # 2. 嘗試 AI 校對
        if len(main_content) < 1000:  # 只對較短文本使用 AI 校對
            ai_result = self.proofread_translation(result["proofread"], method="gemini")
            if len(ai_result["improvements"]) > len(result["improvements"]):
                result = ai_result
                print("✅ AI 校對完成")
        
        # 3. 重新組合內容和連結
        final_text = result["proofread"]
        if links_section:
            final_text += "\n\n" + links_section
        
        # 4. 最終檢查
        if len(final_text) < len(translated_text) * 0.5:
            print("⚠️ 校對後文本過短，使用原翻譯")
            final_text = translated_text
            result["improvements"].append("校對後文本異常，保留原翻譯")
        
        result["proofread"] = final_text
        
        print(f"🎉 翻譯品質提升完成！共 {len(result['improvements'])} 個改進")
        
        return result
    
    def _separate_content_and_links(self, text: str) -> tuple:
        """分離主要內容和連結區塊"""
        # 尋找連結區塊的開始位置
        link_patterns = [
            r'\n\n### 🖼️ 圖片連結\n\n',
            r'\n\n### 📎 相關連結\n\n'
        ]
        
        earliest_match = len(text)
        for pattern in link_patterns:
            match = re.search(pattern, text)
            if match:
                earliest_match = min(earliest_match, match.start())
        
        if earliest_match < len(text):
            # 找到連結區塊
            main_content = text[:earliest_match].strip()
            links_section = text[earliest_match:].strip()
            return main_content, links_section
        else:
            # 沒有連結區塊
            return text.strip(), ""

def test_proofreader():
    """測試校對功能"""
    proofreader = TranslationProofreader()
    
    # 測試文本（包含需要修正為台灣用語的內容）
    test_texts = [
        "您好，這是一個測試消息。請查看附件中的文件。。",
        "我們的软件需要更新，請提供更多信息和数据。",
        "這個网络程序的的問題很重要，我們需要了了解更多細節。",
        "請使用计算机打開这个视频文件，並檢查音频品質。",
        "新的硬件已經安裝完成，网站功能正常運作。"
    ]
    
    print("🧪 開始測試翻譯校對功能...")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 測試 {i}:")
        print(f"原文: {text}")
        
        result = proofreader.proofread_translation(text, method="basic")
        
        print(f"校對後: {result['proofread']}")
        if result['improvements']:
            print("改進點:")
            for improvement in result['improvements']:
                print(f"  - {improvement}")
        else:
            print("無需改進")
        
        print("-" * 30)
    
    print("\n✅ 校對功能測試完成！")

if __name__ == "__main__":
    test_proofreader()