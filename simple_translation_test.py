#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單翻譯測試
"""

def test_google_translate():
    """測試Google翻譯"""
    try:
        from googletrans import Translator
        translator = Translator()
        
        test_text = "Hello, this is a test message for translation. How are you today?"
        print(f"原文: {test_text}")
        
        result = translator.translate(test_text, src='en', dest='zh-tw')
        print(f"翻譯結果: {result.text}")
        return True
    except Exception as e:
        print(f"Google翻譯失敗: {e}")
        return False

def test_google_translate_advanced():
    """測試Google翻譯進階功能"""
    try:
        from googletrans import Translator
        translator = Translator()
        
        # 測試包含連結的文本
        test_text = "Check out this link: https://example.com and this image: https://example.com/image.jpg"
        print(f"測試文本: {test_text}")
        
        result = translator.translate(test_text, src='en', dest='zh-tw')
        print(f"翻譯結果: {result.text}")
        return True
    except Exception as e:
        print(f"Google翻譯進階測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🧪 簡單翻譯測試")
    print("=" * 40)
    
    print("\n1. 測試Google翻譯基本功能:")
    google_basic_ok = test_google_translate()
    
    print("\n2. 測試Google翻譯進階功能:")
    google_advanced_ok = test_google_translate_advanced()
    
    print("\n" + "=" * 40)
    if google_basic_ok:
        print("✅ Google翻譯基本功能可用")
        if google_advanced_ok:
            print("✅ Google翻譯進階功能也正常")
        print("🎉 程式應該可以正常運作")
    else:
        print("❌ Google翻譯服務不可用")