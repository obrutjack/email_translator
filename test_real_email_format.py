#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試真實郵件格式的連結處理
基於你提供的實際郵件內容
"""

from email_translator import EmailTranslator

def test_real_email_content():
    """測試真實郵件內容的處理"""
    print("🧪 測試真實郵件內容處理")
    print("=" * 50)
    
    # 模擬你提供的實際郵件內容
    real_email_content = """a quiet day

AI News for 7/15/2025-7/16/2025. We checked 9 subreddits, 449 Twitters and 29 Discords (226 channels, and 5810 messages) for you. Estimated reading time saved (at 200wpm): 481 minutes. Our new website is now up with full metadata search and beautiful vibe coded presentation of all past issues. See https://news.smol.ai/ for the full news breakdowns and give us feedback on @smol_ai!

there was a eyebrow raising HR move if you care about Claude Code's future or Anthropic's $100b fundraise, Fal's leaked $1.5b Series C, or otherwise you could just tune in to the first ever podcast with Cline.

AI Twitter Recap

Model Releases, Performance & Benchmarks

• Mistral Releases Voxtral Speech Recognition Models: @MistralAI announced the release of Voxtral, which they claim are the "world's best [and open] speech recognition models." They provided links to try the models via API, on Le Chat, or download from Hugging Face.

• Kimi K2 Open Model Challenges Proprietary Models: Moonshot AI's Kimi K2, a trillion-parameter Mixture-of-Experts (MoE) model, has been a major topic. It is now live on W&B Inference via CoreWeave and available in the LM Arena. Cline showed a demo of Kimi K2 running on Groq, achieving speeds of 200 tokens/second, significantly faster than Claude Sonnet-4's typical ~60 TPS. On benchmarks, All-Hands AI reported that Kimi-K2 achieved"""
    
    translator = EmailTranslator({})
    
    print("原始郵件內容:")
    print(real_email_content[:500] + "...")
    print("-" * 60)
    
    # 測試連結提取
    cleaned_text, links, image_links = translator.clean_text_for_translation(real_email_content)
    
    print(f"提取的連結數量: {len(links)}")
    print(f"提取的圖片連結數量: {len(image_links)}")
    print()
    
    print("提取的連結:")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")
    
    print()
    print("清理後的文本:")
    print(cleaned_text[:500] + "...")
    
    # 測試翻譯流程
    print("\n" + "=" * 60)
    print("🔄 測試翻譯流程...")
    
    try:
        result = translator.translate_to_chinese(real_email_content)
        print("翻譯結果:")
        print(result[:800] + "...")
        
        # 檢查連結處理
        if "### 📎 相關連結" in result:
            print("\n✅ 找到相關連結區塊")
            link_section = result.split("### 📎 相關連結")[1]
            link_count = len([line for line in link_section.split('\n') if line.strip() and line.strip()[0].isdigit()])
            print(f"文末連結數量: {link_count}")
        else:
            print("\n❌ 沒有找到相關連結區塊")
            
    except Exception as e:
        print(f"❌ 翻譯失敗: {e}")

def analyze_email_structure():
    """分析郵件結構，了解連結的實際格式"""
    print("\n🔍 分析郵件結構")
    print("=" * 30)
    
    # 從你的截圖中可以看到的連結文字
    embedded_links = [
        "449 Twitters",
        "eyebrow raising HR move", 
        "$1.5b Series C",
        "first ever podcast with Cline",
        "@MistralAI",
        "try the models via API, on Le Chat, or download from Hugging Face",
        "live on W&B Inference via CoreWeave",
        "LM Arena",
        "Cline showed a demo of Kimi K2 running on Groq",
        "All-Hands AI reported that Kimi-K2 achieved"
    ]
    
    print("郵件中的內嵌連結文字:")
    for i, link_text in enumerate(embedded_links, 1):
        print(f"{i}. {link_text}")
    
    print(f"\n總共識別出 {len(embedded_links)} 個可能的內嵌連結")
    print("這些連結在 Gmail API 中可能以不同格式出現")

if __name__ == "__main__":
    print("🚀 真實郵件格式測試")
    print("=" * 50)
    
    # 測試1: 真實郵件內容處理
    test_real_email_content()
    
    # 測試2: 分析郵件結構
    analyze_email_structure()
    
    print("\n💡 建議:")
    print("1. 檢查 Gmail API 提取的原始郵件內容格式")
    print("2. 可能需要處理 HTML 格式的郵件內容")
    print("3. 內嵌連結可能需要不同的處理方式")