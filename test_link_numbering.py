#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試連結編號一致性
"""

from email_translator import EmailTranslator

def test_link_numbering():
    """測試連結編號的一致性"""
    print("🧪 測試連結編號一致性")
    print("=" * 50)
    
    # 建立翻譯器實例
    config = {
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'deepl_api_key': ''
    }
    translator = EmailTranslator(config)
    
    # 測試案例：包含多個連結和圖片的文本
    test_cases = [
        {
            "name": "混合連結和圖片",
            "text": """請查看以下資源：
1. 下載頁面：https://example.com/download
2. 說明圖片：https://example.com/screenshot.png
3. 技術文檔：https://docs.example.com/guide
4. 示範影片：https://example.com/demo.mp4
5. 支援論壇：https://forum.example.com/help"""
        },
        {
            "name": "只有一般連結",
            "text": """相關連結：
- https://github.com/project
- https://stackoverflow.com/questions/123
- https://developer.mozilla.org/docs"""
        },
        {
            "name": "只有圖片連結",
            "text": """請參考這些圖片：
https://example.com/chart1.png
https://example.com/diagram.jpg
https://example.com/flowchart.svg"""
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📧 測試案例 {i}: {case['name']}")
        print(f"原文: {case['text']}")
        print("-" * 60)
        
        # 步驟1: 清理文本並提取連結
        cleaned_text, links, image_links = translator.clean_text_for_translation(case['text'])
        print(f"清理後文本: {cleaned_text}")
        print(f"一般連結 ({len(links)} 個): {links}")
        print(f"圖片連結 ({len(image_links)} 個): {image_links}")
        
        # 步驟2: 模擬翻譯（保持佔位符）
        simulated_translation = cleaned_text  # 假設翻譯後佔位符還在
        print(f"模擬翻譯: {simulated_translation}")
        
        # 步驟3: 恢復連結
        final_result = translator.restore_links_in_translation(
            simulated_translation, links, image_links
        )
        
        print(f"\n最終結果:")
        print(final_result)
        
        # 步驟4: 檢查編號一致性
        print(f"\n編號一致性檢查:")
        
        # 檢查文中的引用編號（排除文末的連結區塊）
        import re
        
        # 分離主要內容和連結區塊
        main_content = final_result
        if "### 🖼️ 圖片連結" in final_result:
            main_content = final_result.split("### 🖼️ 圖片連結")[0]
        elif "### 📎 相關連結" in final_result:
            main_content = final_result.split("### 📎 相關連結")[0]
        
        link_refs = re.findall(r'\[連結(\d+)\]', main_content)
        image_refs = re.findall(r'\[圖片(\d+)\]', main_content)
        
        print(f"文中連結引用: {link_refs}")
        print(f"文中圖片引用: {image_refs}")
        
        # 檢查文末的連結編號
        link_section = re.search(r'### 📎 相關連結\n\n(.*?)(?=\n\n###|\Z)', final_result, re.DOTALL)
        image_section = re.search(r'### 🖼️ 圖片連結\n\n(.*?)(?=\n\n###|\Z)', final_result, re.DOTALL)
        
        if link_section:
            link_numbers = re.findall(r'^(\d+)\.', link_section.group(1), re.MULTILINE)
            print(f"文末連結編號: {link_numbers}")
            
            # 檢查一致性
            if link_refs and link_numbers:
                consistent = sorted(link_refs) == sorted(link_numbers)
                print(f"連結編號一致性: {'✅' if consistent else '❌'}")
        
        if image_section:
            image_numbers = re.findall(r'^(\d+)\.', image_section.group(1), re.MULTILINE)
            print(f"文末圖片編號: {image_numbers}")
            
            # 檢查一致性
            if image_refs and image_numbers:
                consistent = sorted(image_refs) == sorted(image_numbers)
                print(f"圖片編號一致性: {'✅' if consistent else '❌'}")
        
        print("=" * 60)
    
    print("\n✅ 連結編號一致性測試完成！")

def test_with_translation():
    """測試實際翻譯中的連結編號"""
    print("\n🔄 測試實際翻譯中的連結編號")
    print("=" * 40)
    
    config = {
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'deepl_api_key': ''
    }
    translator = EmailTranslator(config)
    
    # 英文測試文本，包含連結
    test_text = """Please check the following resources:
1. Download page: https://example.com/download
2. Documentation: https://docs.example.com/guide
3. Screenshot: https://example.com/screenshot.png
4. Support forum: https://forum.example.com/help"""
    
    print(f"原文: {test_text}")
    print("-" * 50)
    
    try:
        # 執行完整翻譯流程
        result = translator.translate_to_chinese(test_text)
        print(f"翻譯結果:")
        print(result)
        
        # 檢查編號一致性（排除文末連結區塊）
        import re
        
        # 分離主要內容
        main_content = result
        if "### 🖼️ 圖片連結" in result:
            main_content = result.split("### 🖼️ 圖片連結")[0]
        elif "### 📎 相關連結" in result:
            main_content = result.split("### 📎 相關連結")[0]
        
        link_refs = re.findall(r'\[連結(\d+)\]', main_content)
        image_refs = re.findall(r'\[圖片(\d+)\]', main_content)
        
        print(f"\n編號檢查:")
        print(f"文中連結引用: {link_refs}")
        print(f"文中圖片引用: {image_refs}")
        
        # 檢查是否有對應的文末連結
        has_link_section = "### 📎 相關連結" in result
        has_image_section = "### 🖼️ 圖片連結" in result
        
        print(f"有相關連結區塊: {'✅' if has_link_section else '❌'}")
        print(f"有圖片連結區塊: {'✅' if has_image_section else '❌'}")
        
    except Exception as e:
        print(f"❌ 翻譯失敗: {e}")

if __name__ == "__main__":
    print("🚀 連結編號一致性測試")
    print("=" * 50)
    
    # 測試1: 基本編號一致性
    test_link_numbering()
    
    # 測試2: 實際翻譯中的編號
    test_with_translation()
    
    print("\n🎉 所有測試完成！")