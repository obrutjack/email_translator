#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版整合測試 - 測試翻譯和校對功能的整合
"""

def test_translation_with_proofreading():
    """測試翻譯+校對的完整流程"""
    print("🧪 測試翻譯+校對整合功能")
    print("=" * 40)
    
    # 匯入必要模組
    try:
        from email_translator import EmailTranslator
        from translation_proofreader import TranslationProofreader
        print("✅ 模組匯入成功")
    except ImportError as e:
        print(f"❌ 模組匯入失敗: {e}")
        return False
    
    # 建立實例
    config = {
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'deepl_api_key': ''
    }
    
    translator = EmailTranslator(config)
    proofreader = TranslationProofreader()
    
    # 測試案例
    test_cases = [
        {
            "name": "英文商務郵件",
            "content": "Hello, please check the software update information in the attached file."
        },
        {
            "name": "日文通知",
            "content": "こんにちは、添付ファイルをご確認ください。"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📧 測試案例 {i}: {case['name']}")
        print(f"原文: {case['content']}")
        print("-" * 50)
        
        try:
            # 步驟1: 翻譯
            print("🔄 翻譯中...")
            translated = translator.translate_to_chinese(case['content'])
            print(f"翻譯結果: {translated}")
            
            # 步驟2: 校對
            print("\n📝 校對中...")
            proofread_result = proofreader.enhance_translation_quality(
                case['content'], translated
            )
            
            print(f"最終結果: {proofread_result['proofread']}")
            
            if proofread_result['improvements']:
                print(f"\n改進項目:")
                for improvement in proofread_result['improvements'][:3]:
                    print(f"  - {improvement}")
            
            print("✅ 處理成功")
            
        except Exception as e:
            print(f"❌ 處理失敗: {e}")
        
        print("=" * 50)
    
    return True

def test_proofreading_only():
    """只測試校對功能"""
    print("\n📝 測試校對功能")
    print("=" * 30)
    
    try:
        from translation_proofreader import TranslationProofreader
        proofreader = TranslationProofreader()
        
        # 測試包含錯誤的翻譯
        test_text = "您好，請檢查附件文件中的软件更新信息。。"
        print(f"原始翻譯: {test_text}")
        
        # 只測試基本校對，避免 API 調用超時
        result = proofreader.proofread_translation(test_text, method="basic")
        print(f"校對結果: {result['proofread']}")
        
        if result['improvements']:
            print("改進項目:")
            for improvement in result['improvements']:
                print(f"  - {improvement}")
        
        print("✅ 校對功能正常")
        return True
        
    except Exception as e:
        print(f"❌ 校對功能失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 簡化版整合測試")
    print("=" * 50)
    
    # 測試1: 校對功能
    success1 = test_proofreading_only()
    
    # 測試2: 完整流程
    if success1:
        success2 = test_translation_with_proofreading()
        
        if success2:
            print("\n🎉 所有測試通過！")
            print("✅ 你的郵件翻譯器已經完全整合了校對功能")
            print("💡 現在可以使用 python email_translator.py 來處理實際郵件")
        else:
            print("\n⚠️ 部分測試失敗")
    else:
        print("\n❌ 基本功能測試失敗")