#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終綜合測試 - 驗證所有問題是否都已解決
"""

from email_translator import EmailTranslator
from translation_proofreader import TranslationProofreader

def test_all_issues_resolved():
    """測試所有問題是否都已解決"""
    print("🧪 最終綜合測試 - 驗證所有問題解決狀況")
    print("=" * 60)
    
    config = {'telegram_bot_token': '', 'telegram_chat_id': '', 'deepl_api_key': ''}
    translator = EmailTranslator(config)
    proofreader = TranslationProofreader()
    
    # 模擬複雜的多語言郵件，包含重複連結和需要校對的內容
    test_email = """
    Hello! Please check these resources:
    1. Main site: https://example.com/
    2. Documentation: https://docs.example.com/guide
    3. Again, visit: https://example.com/
    4. Support: https://support.example.com/
    5. Screenshot: https://example.com/screenshot.png
    6. Another image: https://example.com/diagram.jpg
    7. Duplicate doc link: https://docs.example.com/guide
    
    Also check this Japanese text: こんにちは、これは重要な情報です。
    And this Korean: 안녕하세요, 중요한 정보입니다.
    """
    
    print("📧 測試郵件內容:")
    print(test_email)
    print("-" * 60)
    
    results = {}
    
    # 測試1: 多語言偵測和翻譯
    print("🔄 測試1: 多語言偵測和翻譯")
    try:
        translated = translator.translate_to_chinese(test_email)
        results['translation'] = '✅ 成功'
        print("翻譯結果預覽:")
        print(translated[:300] + "...")
    except Exception as e:
        results['translation'] = f'❌ 失敗: {e}'
        print(f"❌ 翻譯失敗: {e}")
        return results
    
    # 測試2: 台灣用語校對
    print("\n📝 測試2: 台灣用語校對")
    try:
        # 模擬包含大陸用語的翻譯結果
        test_translation = "請檢查這些资源：软件更新信息在文件中。"
        proofread_result = proofreader.enhance_translation_quality("", test_translation)
        
        if "資訊" in proofread_result['proofread'] and "軟體" in proofread_result['proofread']:
            results['taiwan_terms'] = '✅ 成功'
            print("✅ 台灣用語校對正常")
        else:
            results['taiwan_terms'] = '❌ 台灣用語未正確轉換'
            print("❌ 台灣用語校對有問題")
    except Exception as e:
        results['taiwan_terms'] = f'❌ 失敗: {e}'
        print(f"❌ 校對失敗: {e}")
    
    # 測試3: 連結編號一致性
    print("\n🔗 測試3: 連結編號一致性")
    try:
        # 檢查文中連結引用和文末連結的對應關係
        import re
        
        # 分離主要內容和連結區塊
        if "### 📎 相關連結" in translated:
            main_content = translated.split("### 📎 相關連結")[0]
            link_section = translated.split("### 📎 相關連結")[1]
            
            # 找出文中的連結引用
            link_refs = re.findall(r'\[連結(\d+)\]', main_content)
            
            # 找出文末的連結編號
            link_numbers = re.findall(r'^(\d+)\.', link_section, re.MULTILINE)
            
            # 檢查文中引用的編號是否都在文末連結範圍內
            unique_refs = list(set(link_refs))
            max_ref = max([int(ref) for ref in unique_refs]) if unique_refs else 0
            max_link = len(link_numbers)
            
            if max_ref <= max_link and set(unique_refs) <= set(link_numbers):
                results['link_consistency'] = '✅ 成功'
                print(f"✅ 連結編號一致：文中引用 {unique_refs} 都在文末範圍 {link_numbers} 內")
            else:
                results['link_consistency'] = '❌ 編號不一致'
                print(f"❌ 連結編號不一致：文中引用 {unique_refs}，文末範圍 {link_numbers}")
                print(f"   文中所有引用: {link_refs}")
        else:
            results['link_consistency'] = '⚠️ 無連結區塊'
            print("⚠️ 沒有找到連結區塊")
    except Exception as e:
        results['link_consistency'] = f'❌ 失敗: {e}'
        print(f"❌ 連結檢查失敗: {e}")
    
    # 測試4: 重複連結處理
    print("\n🔄 測試4: 重複連結處理")
    try:
        # 檢查是否有重複連結
        if "### 📎 相關連結" in translated:
            link_section = translated.split("### 📎 相關連結")[1]
            links = re.findall(r'\d+\.\s+(https?://[^\s]+)', link_section)
            
            unique_links = list(set(links))
            if len(links) == len(unique_links):
                results['duplicate_links'] = '✅ 成功'
                print(f"✅ 無重複連結：{len(links)} 個連結都是唯一的")
            else:
                results['duplicate_links'] = '❌ 有重複連結'
                print(f"❌ 發現重複連結：總數 {len(links)}，唯一 {len(unique_links)}")
                
                # 找出重複的連結
                seen = set()
                duplicates = []
                for link in links:
                    if link in seen:
                        duplicates.append(link)
                    else:
                        seen.add(link)
                print(f"重複的連結: {duplicates}")
        else:
            results['duplicate_links'] = '⚠️ 無連結區塊'
            print("⚠️ 沒有找到連結區塊")
    except Exception as e:
        results['duplicate_links'] = f'❌ 失敗: {e}'
        print(f"❌ 重複連結檢查失敗: {e}")
    
    # 測試5: 連結和圖片保留
    print("\n🖼️ 測試5: 連結和圖片保留")
    try:
        has_images = "### 🖼️ 圖片連結" in translated
        has_links = "### 📎 相關連結" in translated
        
        if has_images and has_links:
            results['link_preservation'] = '✅ 成功'
            print("✅ 連結和圖片區塊都已保留")
        elif has_links:
            results['link_preservation'] = '⚠️ 部分成功'
            print("⚠️ 只有連結區塊，沒有圖片區塊")
        else:
            results['link_preservation'] = '❌ 失敗'
            print("❌ 連結和圖片區塊都沒有保留")
    except Exception as e:
        results['link_preservation'] = f'❌ 失敗: {e}'
        print(f"❌ 連結保留檢查失敗: {e}")
    
    return results

def print_final_summary(results):
    """打印最終總結"""
    print("\n" + "=" * 60)
    print("🎯 最終測試結果總結")
    print("=" * 60)
    
    test_items = [
        ("多語言翻譯", "translation"),
        ("台灣用語校對", "taiwan_terms"),
        ("連結編號一致性", "link_consistency"),
        ("重複連結處理", "duplicate_links"),
        ("連結和圖片保留", "link_preservation")
    ]
    
    passed = 0
    total = len(test_items)
    
    for name, key in test_items:
        status = results.get(key, '❌ 未測試')
        print(f"{name}: {status}")
        if status.startswith('✅'):
            passed += 1
    
    print("-" * 60)
    print(f"總體結果: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("🎉 所有問題都已解決！")
        return True
    else:
        print("⚠️ 還有問題需要處理")
        return False

if __name__ == "__main__":
    print("🚀 最終綜合測試")
    print("檢查之前討論的所有問題是否都已解決")
    print("=" * 60)
    
    results = test_all_issues_resolved()
    all_passed = print_final_summary(results)
    
    if all_passed:
        print("\n✨ 恭喜！你的郵件翻譯器已經完全優化！")
        print("現在可以放心使用 python email_translator.py 處理實際郵件了")
    else:
        print("\n💡 建議檢查失敗的項目並進行修正")