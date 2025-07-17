#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API Key 設定工具
"""

import json
import os

def setup_gemini_api():
    """設定 Gemini API Key"""
    print("🔧 Gemini API Key 設定工具")
    print("=" * 40)
    
    # 檢查是否已經有設定
    existing_key = None
    
    # 檢查環境變數
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        print(f"✅ 環境變數中已有 API Key: {env_key[:10]}...")
        existing_key = env_key
    
    # 檢查配置檔案
    try:
        with open('gemini_apikey.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            file_key = config.get('api_key')
            if file_key and file_key != "your_gemini_api_key_here":
                print(f"✅ 配置檔案中已有 API Key: {file_key[:10]}...")
                existing_key = file_key
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    if existing_key:
        choice = input("\n是否要更新現有的 API Key？(y/N): ").lower()
        if choice != 'y':
            print("✅ 保持現有設定")
            return True
    
    print("\n📝 請輸入你的 Gemini API Key:")
    print("🔗 取得免費 API Key: https://makersuite.google.com/app/apikey")
    print("💡 提示: API Key 通常以 'AIza' 開頭")
    
    api_key = input("\nAPI Key: ").strip()
    
    if not api_key:
        print("❌ API Key 不能為空")
        return False
    
    if not api_key.startswith('AIza'):
        print("⚠️ 警告: API Key 通常以 'AIza' 開頭，請確認是否正確")
        confirm = input("是否繼續？(y/N): ").lower()
        if confirm != 'y':
            return False
    
    # 選擇設定方式
    print("\n🎯 選擇設定方式:")
    print("1. 儲存到配置檔案 (推薦)")
    print("2. 設定環境變數")
    
    choice = input("請選擇 (1/2): ").strip()
    
    if choice == '1':
        # 儲存到配置檔案
        config = {
            "api_key": api_key,
            "note": "此檔案包含敏感資訊，請勿分享或上傳到版本控制系統"
        }
        
        try:
            with open('gemini_apikey.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("✅ API Key 已儲存到 gemini_apikey.json")
            print("⚠️ 注意: 此檔案已加入 .gitignore，不會被上傳到 Git")
            
        except Exception as e:
            print(f"❌ 儲存失敗: {e}")
            return False
            
    elif choice == '2':
        # 設定環境變數
        print(f"\n💡 請執行以下命令設定環境變數:")
        print(f"export GEMINI_API_KEY='{api_key}'")
        print("\n或加入到你的 shell 配置檔案 (~/.zshrc 或 ~/.bashrc):")
        print(f"echo 'export GEMINI_API_KEY=\"{api_key}\"' >> ~/.zshrc")
        
    else:
        print("❌ 無效選擇")
        return False
    
    # 測試 API Key
    print("\n🧪 測試 API Key...")
    try:
        from translation_proofreader import TranslationProofreader
        proofreader = TranslationProofreader()
        
        test_result = proofreader.proofread_translation(
            "這是一個測試消息。", method="gemini"
        )
        
        if len(test_result['improvements']) > 0:
            print("✅ API Key 測試成功！")
            print(f"測試結果: {test_result['proofread']}")
        else:
            print("✅ API Key 有效，但測試文本無需改進")
            
    except Exception as e:
        print(f"⚠️ API Key 測試失敗: {e}")
        print("💡 請檢查 API Key 是否正確，或稍後再試")
    
    return True

def check_gemini_status():
    """檢查 Gemini 設定狀態"""
    print("🔍 檢查 Gemini API 設定狀態")
    print("=" * 30)
    
    # 檢查環境變數
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        print(f"✅ 環境變數: {env_key[:10]}...")
    else:
        print("❌ 環境變數: 未設定")
    
    # 檢查配置檔案
    try:
        with open('gemini_apikey.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            file_key = config.get('api_key')
            if file_key and file_key != "your_gemini_api_key_here":
                print(f"✅ 配置檔案: {file_key[:10]}...")
            else:
                print("❌ 配置檔案: 無效的 API Key")
    except FileNotFoundError:
        print("❌ 配置檔案: 不存在")
    except json.JSONDecodeError:
        print("❌ 配置檔案: 格式錯誤")
    
    # 檢查 .gitignore
    try:
        with open('.gitignore', 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
            if 'gemini_apikey.json' in gitignore_content:
                print("✅ .gitignore: 已保護 API Key 檔案")
            else:
                print("⚠️ .gitignore: 建議加入 gemini_apikey.json")
    except FileNotFoundError:
        print("⚠️ .gitignore: 檔案不存在")

if __name__ == "__main__":
    print("🚀 Gemini API 設定工具")
    print("=" * 50)
    
    while True:
        print("\n選擇操作:")
        print("1. 設定 API Key")
        print("2. 檢查設定狀態")
        print("3. 測試 API 功能")
        print("4. 退出")
        
        choice = input("\n請選擇 (1-4): ").strip()
        
        if choice == '1':
            setup_gemini_api()
        elif choice == '2':
            check_gemini_status()
        elif choice == '3':
            os.system('python test_gemini_proofreading.py')
        elif choice == '4':
            print("👋 再見！")
            break
        else:
            print("❌ 無效選擇，請重新輸入")