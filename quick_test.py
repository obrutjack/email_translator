#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速驗證腳本 - 檢查郵件翻譯器的基本功能
"""

import sys
import os

def check_python_version():
    """檢查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ Python版本過舊，需要Python 3.7或更新版本")
        return False
    else:
        print(f"✅ Python版本: {sys.version.split()[0]}")
        return True

def check_required_files():
    """檢查必要檔案"""
    required_files = [
        'email_translator.py',
        'requirements.txt',
        'gmail_oauth_setup.md',
        'setup_guide.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ 找到檔案: {file}")
        else:
            print(f"❌ 缺少檔案: {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_credentials():
    """檢查Google認證檔案"""
    if os.path.exists('credentials.json'):
        print("✅ 找到 credentials.json")
        return True
    else:
        print("⚠️ 找不到 credentials.json - 需要從Google Cloud Console下載")
        return False

def test_imports():
    """測試套件匯入"""
    packages = [
        ('requests', 'HTTP請求'),
        ('google.auth', 'Google認證'),
        ('googleapiclient', 'Gmail API'),
        ('googletrans', 'Google翻譯')
    ]
    
    success_count = 0
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {description}: {package}")
            success_count += 1
        except ImportError:
            print(f"❌ {description}: {package} - 請執行 pip install -r requirements.txt")
    
    return success_count == len(packages)

def test_translation():
    """測試翻譯功能"""
    try:
        from googletrans import Translator
        
        translator = Translator()
        test_text = "Hello world"
        
        result = translator.translate(test_text, src='en', dest='zh-tw')
        translated = result.text
        
        print(f"✅ 翻譯測試成功: '{test_text}' → '{translated}'")
        return True
        
    except Exception as e:
        print(f"❌ 翻譯測試錯誤: {e}")
        return False

def main():
    """主要檢查流程"""
    print("🔍 郵件翻譯器快速驗證")
    print("=" * 40)
    
    checks = [
        ("Python版本", check_python_version),
        ("必要檔案", check_required_files),
        ("Google認證", check_credentials),
        ("套件匯入", test_imports),
        ("翻譯功能", test_translation)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 檢查 {name}...")
        if check_func():
            passed += 1
        else:
            print(f"   💡 請參考設定指南修復此問題")
    
    print("\n" + "=" * 40)
    print(f"📊 檢查結果: {passed}/{total} 項通過")
    
    if passed == total:
        print("🎉 基本檢查全部通過！")
        print("\n🚀 下一步:")
        print("1. 確保Telegram Bot設定正確")
        print("2. 執行: python email_translator.py")
        return True
    else:
        print("⚠️ 請修復上述問題後重新檢查")
        return False

if __name__ == "__main__":
    main()