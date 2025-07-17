#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Gemini AI 校對功能
"""

import os
from translation_proofreader import TranslationProofreader

def test_gemini_proofreading():
    """測試 Gemini AI 校對功能"""
    
    # 檢查是否有設定 API Key
    api_key = os.getenv('GEMINI_API_KEY')
    
    # 如果環境變數沒有，嘗試從配置檔案讀取
    if not api_key:
        try:
            import json
            with open('gemini_apikey.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('api_key')
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("⚠️ 未設定 GEMINI_API_KEY")
        print("💡 方法1: 設定環境變數: export GEMINI_API_KEY='your_api_key'")
        print("💡 方法2: 建立 gemini_apikey.json 檔案")
        print("🔗 取得免費 API Key: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ 找到 API Key: {api_key[:10]}...")  # 只顯示前10個字符
    
    print("🧪 開始測試 Gemini AI 校對功能...")
    print("=" * 50)
    
    # 測試文本 - 包含各種需要校對的問題
    test_texts = [
        # 台灣用語問題
        "這個软件的信息很重要，請查看文件中的数据。",
        
        # 語法和流暢度問題
        "我們的网络程序有一些的的問題，需要更新硬件配置。",
        
        # 標點和格式問題
        "您好，，這是測試消息。。請使用计算机打開视频文件。",
        
        # 混合問題
        "新的系统已經安裝完成，请检查网站功能是否正常運作。所有的的数据都已經備份到云端服务器。"
    ]
    
    proofreader = TranslationProofreader()
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 測試案例 {i}:")
        print(f"原文: {text}")
        print("-" * 40)
        
        # 測試基本校對
        basic_result = proofreader.proofread_translation(text, method="basic")
        print(f"基本校對: {basic_result['proofread']}")
        if basic_result['improvements']:
            print("基本改進:")
            for improvement in basic_result['improvements']:
                print(f"  - {improvement}")
        
        print()
        
        # 測試 AI 校對
        ai_result = proofreader.proofread_translation(text, method="gemini")
        print(f"AI 校對: {ai_result['proofread']}")
        if ai_result['improvements']:
            print("AI 改進:")
            for improvement in ai_result['improvements']:
                print(f"  - {improvement}")
        
        print("=" * 50)
    
    print("\n✅ Gemini AI 校對測試完成！")
    return True

def test_comprehensive_proofreading():
    """測試綜合校對功能"""
    print("\n🚀 測試綜合校對功能...")
    
    proofreader = TranslationProofreader()
    
    # 模擬翻譯結果
    original_email = "Hello, please check the software update information in the attached file."
    translated_text = "您好，請檢查附件文件中的软件更新信息。。"
    
    print(f"原始郵件: {original_email}")
    print(f"翻譯結果: {translated_text}")
    print("-" * 50)
    
    # 使用綜合校對功能
    result = proofreader.enhance_translation_quality(original_email, translated_text)
    
    print(f"最終結果: {result['proofread']}")
    print("\n改進項目:")
    for improvement in result['improvements']:
        print(f"  - {improvement}")
    
    print("\n✅ 綜合校對測試完成！")

if __name__ == "__main__":
    print("🎯 Gemini AI 校對功能測試")
    print("=" * 50)
    
    # 基本 Gemini 測試
    success = test_gemini_proofreading()
    
    if success:
        # 綜合功能測試
        test_comprehensive_proofreading()
    
    print("\n🎉 測試完成！")
    print("💡 提示: 如果要在實際郵件翻譯中使用 AI 校對，")
    print("   請確保已設定 GEMINI_API_KEY 環境變數")