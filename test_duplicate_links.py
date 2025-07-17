#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試重複連結問題
"""

from email_translator import EmailTranslator

def test_duplicate_links():
    """測試重複連結的處理"""
    print("🧪 測試重複連結處理")
    print("=" * 50)
    
    translator = EmailTranslator({})
    
    # 測試包含重複連結的文本
    test_cases = [
        {
            "name": "包含重複連結的文本",
            "text": """請查看以下資源：
1. 官網：https://example.com/
2. 文檔：https://docs.example.com/
3. 再次提到官網：https://example.com/
4. 支援：https://support.example.com/
5. 又一次提到文檔：https://docs.example.com/"""
        },
        {
            "name": "大量重複連結",
            "text": """多次提到：
https://news.smol.ai/ 
https://news.smol.ai/
https://x.com/Smol_AI
https://news.smol.ai/
https://x.com/Smol_AI
https://news.smol.ai/"""
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📧 測試案例 {i}: {case['name']}")
        print(f"原文: {case['text']}")
        print("-" * 60)
        
        # 測試連結提取
        cleaned_text, links, image_links = translator.clean_text_for_translation(case['text'])
        
        print(f"提取的連結數量: {len(links)}")
        print(f"連結列表:")
        for j, link in enumerate(links):
            print(f"  {j}: {link}")
        
        print(f"\n清理後文本: {cleaned_text}")
        
        # 檢查是否有重複
        unique_links = list(set(links))
        print(f"去重後連結數量: {len(unique_links)}")
        
        if len(links) != len(unique_links):
            print("❌ 發現重複連結！")
            # 找出重複的連結
            seen = set()
            duplicates = set()
            for link in links:
                if link in seen:
                    duplicates.add(link)
                else:
                    seen.add(link)
            print(f"重複的連結: {list(duplicates)}")
        else:
            print("✅ 沒有重複連結")
        
        # 測試翻譯流程
        print("\n🔄 測試翻譯流程...")
        try:
            result = translator.translate_to_chinese(case['text'])
            print("翻譯結果:")
            print(result[:500] + ("..." if len(result) > 500 else ""))
            
            # 檢查文末連結數量
            if "### 📎 相關連結" in result:
                link_section = result.split("### 📎 相關連結")[1]
                final_link_count = len([line for line in link_section.split('\n') if line.strip() and line.strip()[0].isdigit()])
                print(f"文末連結數量: {final_link_count}")
                
                if final_link_count != len(unique_links):
                    print(f"⚠️ 文末連結數量 ({final_link_count}) 與去重後連結數量 ({len(unique_links)}) 不符")
                else:
                    print("✅ 文末連結數量正確")
            
        except Exception as e:
            print(f"❌ 翻譯失敗: {e}")
        
        print("=" * 60)

def test_link_deduplication_logic():
    """測試連結去重邏輯"""
    print("\n🔧 測試連結去重邏輯")
    print("=" * 30)
    
    translator = EmailTranslator({})
    
    # 直接測試 clean_text_for_translation 函數
    test_text = """
    重複連結測試：
    https://example.com/page1
    https://example.com/page2  
    https://example.com/page1
    https://example.com/page3
    https://example.com/page2
    https://example.com/page1
    """
    
    print(f"測試文本: {test_text}")
    
    cleaned_text, links, image_links = translator.clean_text_for_translation(test_text)
    
    print(f"清理後文本: {cleaned_text}")
    print(f"提取的連結: {links}")
    print(f"連結數量: {len(links)}")
    
    # 檢查去重效果
    unique_links = []
    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    
    print(f"應該的去重結果: {unique_links}")
    print(f"應該的連結數量: {len(unique_links)}")
    
    if len(links) == len(unique_links) and links == unique_links:
        print("✅ 連結去重邏輯正常工作")
    else:
        print("❌ 連結去重邏輯有問題")
        print(f"實際: {links}")
        print(f"期望: {unique_links}")

if __name__ == "__main__":
    print("🚀 重複連結問題測試")
    print("=" * 50)
    
    # 測試1: 重複連結處理
    test_duplicate_links()
    
    # 測試2: 去重邏輯
    test_link_deduplication_logic()
    
    print("\n💡 如果發現重複連結問題，需要檢查:")
    print("1. clean_text_for_translation 函數的去重邏輯")
    print("2. restore_links_in_translation 函數的連結處理")
    print("3. 翻譯過程中佔位符的處理")