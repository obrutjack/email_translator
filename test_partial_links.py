#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試部分連結佔位符沒有被轉換的情況
模擬你遇到的問題：只有連結11和連結12出現在文中，但文末列出1-12個連結
"""

from email_translator import EmailTranslator

def test_partial_link_conversion():
    """測試部分連結轉換的情況"""
    print("🧪 測試部分連結轉換問題")
    print("=" * 50)
    
    translator = EmailTranslator({})
    
    # 模擬你遇到的情況：
    # 1. 原文有12個連結
    # 2. 翻譯後只有部分佔位符被保留（可能因為翻譯過程中被修改）
    
    # 模擬12個連結
    links = [
        'https://twitter.com/i/lists/1585430245762441216',
        'https://twitter.com/i/lists/1585430245762441216',
        'https://news.smol.ai/',
        'https://news.smol.ai/',
        'https://x.com/Smol_AI',
        'https://x.com/nmasc_/status/1945537779061977456',
        'https://x.com/ArfurFrock/status/1945553966495912051?s=46',
        'https://www.youtube.com/watch?v=uIKmG3M0X3M',
        'https://twitter.com/ClementDelangue/status/1945233605745135754',
        'https://twitter.com/ClementDelangue/status/1945233623164006523',
        'https://twitter.com/l2k/status/1945225318928634149',
        'https://twitter.com/Kimi_Moonshot/status/1945462820147249523'
    ]
    
    # 模擬你實際遇到的情況：翻譯後只保留了部分連結引用
    translated_text_with_partial_placeholders = """
Kimi K2 開放機器型挑戰專屬模型：Moonshot AI 的 Kimi K2，一個擁有數兆參數的專家混合型 (MOE)，一直是熱門話題。現在
它可在 CoreWeave ([連結10]) 上進行 Web 推論，並可在 LM Arena ([連結11]) 中使用。
"""
    
    print("模擬情況:")
    print(f"總連結數: {len(links)}")
    print(f"翻譯文本: {translated_text_with_partial_placeholders}")
    print("-" * 60)
    
    # 使用現有的連結恢復函數
    result = translator.restore_links_in_translation(
        translated_text_with_partial_placeholders, 
        links, 
        []
    )
    
    print("處理結果:")
    print(result)
    print("-" * 60)
    
    # 分析結果
    import re
    
    # 檢查文中的連結引用
    main_content = result.split("### 📎 相關連結")[0] if "### 📎 相關連結" in result else result
    link_refs = re.findall(r'\[連結(\d+)\]', main_content)
    
    # 檢查文末的連結數量
    link_section = re.search(r'### 📎 相關連結\n\n(.*?)(?=\n\n###|\Z)', result, re.DOTALL)
    if link_section:
        link_numbers = re.findall(r'^(\d+)\.', link_section.group(1), re.MULTILINE)
    else:
        link_numbers = []
    
    print("分析結果:")
    print(f"文中連結引用: {link_refs}")
    print(f"文末連結數量: {len(link_numbers)}")
    print(f"文末連結編號: {link_numbers}")
    
    # 檢查是否修正了問題
    if len(link_refs) == len(link_numbers):
        print("✅ 問題已修正：文中引用數量與文末連結數量一致")
    else:
        print("❌ 問題仍存在：文中引用數量與文末連結數量不一致")
    
    return len(link_refs) == len(link_numbers)

def test_missing_placeholders():
    """測試佔位符完全丟失的情況"""
    print("\n🔧 測試佔位符丟失的情況")
    print("=" * 40)
    
    translator = EmailTranslator({})
    
    # 模擬佔位符在翻譯過程中完全丟失的情況
    links = ['https://example.com/1', 'https://example.com/2', 'https://example.com/3']
    
    # 翻譯後佔位符完全消失
    translated_text_no_placeholders = "請查看相關資源以獲取更多資訊。"
    
    print(f"原始連結: {links}")
    print(f"翻譯文本: {translated_text_no_placeholders}")
    
    result = translator.restore_links_in_translation(
        translated_text_no_placeholders, 
        links, 
        []
    )
    
    print(f"處理結果: {result}")
    
    # 檢查是否有連結區塊
    has_links = "### 📎 相關連結" in result
    print(f"是否有連結區塊: {'是' if has_links else '否'}")
    
    if not has_links:
        print("✅ 正確處理：沒有佔位符時不顯示連結區塊")
        return True
    else:
        print("❌ 問題：沒有佔位符但仍顯示連結區塊")
        return False

if __name__ == "__main__":
    print("🚀 部分連結轉換問題測試")
    print("=" * 50)
    
    # 測試1: 部分連結轉換
    success1 = test_partial_link_conversion()
    
    # 測試2: 佔位符丟失
    success2 = test_missing_placeholders()
    
    if success1 and success2:
        print("\n🎉 所有測試通過！連結處理邏輯已優化")
    else:
        print("\n⚠️ 部分測試失敗，需要進一步調整")