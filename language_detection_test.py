#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
語言偵測和翻譯功能測試
測試自動偵測不同語言並翻譯成繁體中文的功能
"""

def test_language_detection():
    """測試語言偵測和翻譯功能"""
    try:
        from googletrans import Translator
        translator = Translator()
        
        # 測試文本 - 不同語言
        test_texts = {
            "英文": "Hello, this is a test message. How are you today?",
            "日文": "こんにちは、これはテストメッセージです。今日はいかがですか？",
            "韓文": "안녕하세요, 이것은 테스트 메시지입니다. 오늘 어떻게 지내세요?",
            "法文": "Bonjour, ceci est un message de test. Comment allez-vous aujourd'hui?",
            "德文": "Hallo, das ist eine Testnachricht. Wie geht es Ihnen heute?",
            "西班牙文": "Hola, este es un mensaje de prueba. ¿Cómo estás hoy?",
            "義大利文": "Ciao, questo è un messaggio di prova. Come stai oggi?",
            "俄文": "Привет, это тестовое сообщение. Как дела сегодня?",
            "繁體中文": "你好，這是一個測試訊息。你今天好嗎？",
            "簡體中文": "你好，这是一个测试消息。你今天好吗？"
        }
        
        print("🧪 開始測試語言偵測和翻譯功能...\n")
        print("=" * 60)
        
        for lang_name, text in test_texts.items():
            print(f"\n📝 測試語言: {lang_name}")
            print(f"原文: {text}")
            
            try:
                # 偵測語言
                detected = translator.detect(text)
                confidence = detected.confidence if detected.confidence is not None else 0.0
                print(f"🔍 偵測結果: {detected.lang} (信心度: {confidence:.2f})")
                
                # 如果已經是繁體中文，跳過翻譯
                if detected.lang == 'zh-tw' or (detected.lang == 'zh' and '繁體' in lang_name):
                    print("✅ 已經是繁體中文，無需翻譯")
                    continue
                
                # 翻譯成繁體中文
                result = translator.translate(text, src='auto', dest='zh-tw')
                print(f"🔄 翻譯結果: {result.text}")
                
            except Exception as e:
                print(f"❌ 處理失敗: {e}")
            
            print("-" * 40)
        
        print("\n✅ 語言偵測測試完成！")
        return True
        
    except ImportError:
        print("❌ 需要安裝 googletrans 套件")
        print("💡 執行: pip install googletrans==4.0.0rc1")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_mixed_language():
    """測試混合語言文本"""
    try:
        from googletrans import Translator
        translator = Translator()
        
        print("\n🌐 測試混合語言文本...")
        
        mixed_text = """
        Hello everyone! 今天天気がいいですね。
        Bonjour mes amis. 안녕하세요!
        This is a mixed language test message.
        """
        
        print(f"混合語言文本: {mixed_text}")
        
        # 偵測主要語言
        detected = translator.detect(mixed_text)
        confidence = detected.confidence if detected.confidence is not None else 0.0
        print(f"🔍 主要語言: {detected.lang} (信心度: {confidence:.2f})")
        
        # 翻譯整段文本
        result = translator.translate(mixed_text, src='auto', dest='zh-tw')
        print(f"🔄 翻譯結果: {result.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 混合語言測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 語言偵測和翻譯功能測試")
    print("=" * 50)
    
    # 基本語言偵測測試
    success1 = test_language_detection()
    
    # 混合語言測試
    success2 = test_mixed_language()
    
    if success1 and success2:
        print("\n🎉 所有測試通過！")
        print("✅ 自動語言偵測功能已準備就緒")
    else:
        print("\n⚠️ 部分測試失敗，請檢查設定")