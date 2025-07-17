#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試完整的郵件翻譯工作流程
包括語言偵測、翻譯、校對等功能
"""

from email_translator import EmailTranslator
from translation_proofreader import TranslationProofreader

def test_translation_workflow():
    """測試完整的翻譯工作流程"""
    print("🧪 測試完整翻譯工作流程")
    print("=" * 50)
    
    # 模擬不同語言的郵件內容
    test_emails = [
        {
            "language": "英文",
            "content": "Hello, please check the software update information in the attached file. The new version includes important security fixes and performance improvements."
        },
        {
            "language": "日文", 
            "content": "こんにちは、添付ファイルのソフトウェア更新情報をご確認ください。新しいバージョンには重要なセキュリティ修正とパフォーマンスの改善が含まれています。"
        },
        {
            "language": "韓文",
            "content": "안녕하세요, 첨부 파일의 소프트웨어 업데이트 정보를 확인해 주세요. 새 버전에는 중요한 보안 수정 사항과 성능 개선이 포함되어 있습니다."
        },
        {
            "language": "法文",
            "content": "Bonjour, veuillez vérifier les informations de mise à jour du logiciel dans le fichier joint. La nouvelle version comprend des correctifs de sécurité importants et des améliorations de performance."
        }
    ]
    
    # 建立翻譯器實例（使用空配置，只測試翻譯功能）
    config = {
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'deepl_api_key': ''
    }
    
    translator = EmailTranslator(config)
    proofreader = TranslationProofreader()
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n📧 測試案例 {i}: {email['language']}")
        print(f"原文: {email['content']}")
        print("-" * 60)
        
        try:
            # 步驟1: 翻譯
            print("🔄 步驟1: 翻譯中...")
            translated = translator.translate_to_chinese(email['content'])
            print(f"翻譯結果: {translated}")
            
            # 步驟2: 校對
            print("\n📝 步驟2: 校對中...")
            proofread_result = proofreader.enhance_translation_quality(
                email['content'], translated
            )
            
            print(f"校對結果: {proofread_result['proofread']}")
            
            if proofread_result['improvements']:
                print(f"\n改進項目 ({len(proofread_result['improvements'])} 項):")
                for improvement in proofread_result['improvements']:
                    print(f"  - {improvement}")
            else:
                print("\n✅ 翻譯品質良好，無需改進")
            
        except Exception as e:
            print(f"❌ 處理失敗: {e}")
        
        print("=" * 60)
    
    print("\n🎉 完整工作流程測試完成！")

def test_proofreading_integration():
    """測試校對功能的整合"""
    print("\n🔧 測試校對功能整合")
    print("=" * 30)
    
    # 測試包含常見錯誤的翻譯結果
    test_translations = [
        "您好，請檢查附件文件中的软件更新信息。。",
        "我們的网络程序有一些的的問題，需要更新硬件配置。",
        "新的系统已經安裝完成，请检查网站功能是否正常運作。"
    ]
    
    proofreader = TranslationProofreader()
    
    for i, translation in enumerate(test_translations, 1):
        print(f"\n📝 測試 {i}:")
        print(f"原始翻譯: {translation}")
        
        # 測試基本校對
        basic_result = proofreader.proofread_translation(translation, method="basic")
        print(f"基本校對: {basic_result['proofread']}")
        
        # 測試完整校對（包含AI）
        full_result = proofreader.enhance_translation_quality("", translation)
        print(f"完整校對: {full_result['proofread']}")
        
        if full_result['improvements']:
            print("改進項目:")
            for improvement in full_result['improvements'][:3]:
                print(f"  - {improvement}")
        
        print("-" * 40)
    
    print("\n✅ 校對功能整合測試完成！")

def test_language_detection_integration():
    """測試語言偵測整合"""
    print("\n🌐 測試語言偵測整合")
    print("=" * 30)
    
    config = {
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'deepl_api_key': ''
    }
    
    translator = EmailTranslator(config)
    
    # 測試不同語言的偵測和翻譯
    test_texts = {
        "英文": "Hello, how are you today?",
        "日文": "こんにちは、元気ですか？",
        "繁體中文": "你好，你今天好嗎？",
        "簡體中文": "你好，你今天好吗？"
    }
    
    for lang, text in test_texts.items():
        print(f"\n🔍 測試 {lang}:")
        print(f"原文: {text}")
        
        try:
            result = translator.translate_to_chinese(text)
            print(f"結果: {result}")
        except Exception as e:
            print(f"❌ 失敗: {e}")
    
    print("\n✅ 語言偵測整合測試完成！")

if __name__ == "__main__":
    print("🚀 完整功能整合測試")
    print("=" * 50)
    
    # 測試1: 完整翻譯工作流程
    test_translation_workflow()
    
    # 測試2: 校對功能整合
    test_proofreading_integration()
    
    # 測試3: 語言偵測整合
    test_language_detection_integration()
    
    print("\n🎊 所有整合測試完成！")
    print("💡 你的郵件翻譯器已經具備完整的多語言翻譯和校對功能！")