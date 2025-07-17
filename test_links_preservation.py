#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試連結和圖片保留功能
"""

from translation_proofreader import TranslationProofreader

def test_links_preservation():
    """測試連結和圖片的保留功能"""
    print("🧪 測試連結和圖片保留功能")
    print("=" * 50)
    
    proofreader = TranslationProofreader()
    
    # 測試包含連結和圖片的翻譯文本
    test_cases = [
        {
            "name": "包含圖片連結的文本",
            "text": """您好，請檢查附件文件中的软件更新信息。。

### 🖼️ 圖片連結

1. ![圖片1](https://example.com/screenshot1.png)
2. ![圖片2](https://example.com/diagram.jpg)

### 📎 相關連結

1. https://example.com/download
2. https://support.example.com/help"""
        },
        {
            "name": "只有相關連結的文本",
            "text": """我們的网络程序有一些的的問題，需要更新硬件配置。

### 📎 相關連結

1. https://github.com/project/issues
2. https://docs.example.com/troubleshooting"""
        },
        {
            "name": "沒有連結的普通文本",
            "text": "這個系统已經安裝完成，请检查网站功能是否正常運作。"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📧 測試案例 {i}: {case['name']}")
        print("原文:")
        print(case['text'])
        print("-" * 60)
        
        # 測試分離功能
        main_content, links_section = proofreader._separate_content_and_links(case['text'])
        print(f"主要內容: {main_content}")
        print(f"連結區塊: {links_section}")
        print()
        
        # 測試完整校對功能
        result = proofreader.enhance_translation_quality("", case['text'])
        
        print("校對結果:")
        print(result['proofread'])
        
        if result['improvements']:
            print(f"\n改進項目 ({len(result['improvements'])} 項):")
            for improvement in result['improvements']:
                print(f"  - {improvement}")
        
        # 檢查連結是否被保留
        original_has_images = "🖼️ 圖片連結" in case['text']
        original_has_links = "📎 相關連結" in case['text']
        result_has_images = "🖼️ 圖片連結" in result['proofread']
        result_has_links = "📎 相關連結" in result['proofread']
        
        print(f"\n連結保留檢查:")
        print(f"  圖片連結: 原文{'有' if original_has_images else '無'} → 結果{'有' if result_has_images else '無'} {'✅' if original_has_images == result_has_images else '❌'}")
        print(f"  相關連結: 原文{'有' if original_has_links else '無'} → 結果{'有' if result_has_links else '無'} {'✅' if original_has_links == result_has_links else '❌'}")
        
        print("=" * 60)
    
    print("\n✅ 連結和圖片保留測試完成！")

def test_separation_function():
    """測試內容分離功能"""
    print("\n🔧 測試內容分離功能")
    print("=" * 30)
    
    proofreader = TranslationProofreader()
    
    test_texts = [
        "簡單文本，沒有連結",
        """有連結的文本

### 📎 相關連結

1. https://example.com""",
        """有圖片的文本

### 🖼️ 圖片連結

1. ![圖片](https://example.com/image.png)""",
        """完整的文本

### 🖼️ 圖片連結

1. ![圖片1](https://example.com/image1.png)

### 📎 相關連結

1. https://example.com/link1
2. https://example.com/link2"""
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n測試 {i}:")
        print(f"原文: {repr(text)}")
        
        main_content, links_section = proofreader._separate_content_and_links(text)
        print(f"主要內容: {repr(main_content)}")
        print(f"連結區塊: {repr(links_section)}")
        
        # 重新組合測試
        if links_section:
            reconstructed = main_content + "\n\n" + links_section
        else:
            reconstructed = main_content
        
        print(f"重組結果: {repr(reconstructed)}")
        print(f"是否一致: {'✅' if reconstructed.strip() == text.strip() else '❌'}")
        print("-" * 40)

if __name__ == "__main__":
    print("🚀 連結和圖片保留功能測試")
    print("=" * 50)
    
    # 測試1: 內容分離功能
    test_separation_function()
    
    # 測試2: 完整的連結保留功能
    test_links_preservation()
    
    print("\n🎉 所有測試完成！")