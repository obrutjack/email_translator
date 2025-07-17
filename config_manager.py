#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器 - 管理郵件搜尋條件和程式設定
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """載入配置檔案"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print(f"✅ 成功載入配置檔案: {self.config_file}")
            except json.JSONDecodeError as e:
                print(f"❌ 配置檔案格式錯誤: {e}")
                self.create_default_config()
            except Exception as e:
                print(f"❌ 載入配置檔案失敗: {e}")
                self.create_default_config()
        else:
            print(f"⚠️ 找不到配置檔案 {self.config_file}，建立預設配置")
            self.create_default_config()
    
    def create_default_config(self):
        """建立預設配置檔案"""
        default_config = {
            "telegram": {
                "bot_token": "[your_bot_token]",
                "chat_id": "[your_chat_id]"
            },
            "translation": {
                "deepl_api_key": "",
                "target_language": "zh-TW"
            },
            "email_search": {
                "default_criteria": {
                    "subject": "",
                    "sender": "",
                    "date_after": ""
                },
                "saved_searches": {}
            }
        }
        
        self.config = default_config
        self.save_config()
        print(f"✅ 已建立預設配置檔案: {self.config_file}")
    
    def save_config(self):
        """儲存配置檔案"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✅ 配置已儲存到: {self.config_file}")
        except Exception as e:
            print(f"❌ 儲存配置檔案失敗: {e}")
    
    def get_telegram_config(self) -> Dict[str, str]:
        """取得Telegram設定"""
        return self.config.get('telegram', {})
    
    def get_translation_config(self) -> Dict[str, str]:
        """取得翻譯設定"""
        return self.config.get('translation', {})
    
    def get_default_search_criteria(self) -> Dict[str, str]:
        """取得預設搜尋條件"""
        return self.config.get('email_search', {}).get('default_criteria', {})
    
    def get_saved_searches(self) -> Dict[str, Dict[str, str]]:
        """取得所有已儲存的搜尋條件"""
        return self.config.get('email_search', {}).get('saved_searches', {})
    
    def get_search_criteria(self, search_name: Optional[str] = None) -> Dict[str, str]:
        """取得搜尋條件
        
        Args:
            search_name: 搜尋條件名稱，如果為None則使用預設條件
        
        Returns:
            搜尋條件字典
        """
        if search_name:
            saved_searches = self.get_saved_searches()
            if search_name in saved_searches:
                return saved_searches[search_name]
            else:
                print(f"⚠️ 找不到搜尋條件 '{search_name}'，使用預設條件")
        
        return self.get_default_search_criteria()
    
    def add_search_criteria(self, name: str, criteria: Dict[str, str]):
        """新增搜尋條件"""
        if 'email_search' not in self.config:
            self.config['email_search'] = {'saved_searches': {}}
        
        if 'saved_searches' not in self.config['email_search']:
            self.config['email_search']['saved_searches'] = {}
        
        self.config['email_search']['saved_searches'][name] = criteria
        self.save_config()
        print(f"✅ 已新增搜尋條件: {name}")
    
    def remove_search_criteria(self, name: str):
        """刪除搜尋條件"""
        saved_searches = self.get_saved_searches()
        if name in saved_searches:
            del self.config['email_search']['saved_searches'][name]
            self.save_config()
            print(f"✅ 已刪除搜尋條件: {name}")
        else:
            print(f"⚠️ 找不到搜尋條件: {name}")
    
    def list_search_criteria(self):
        """列出所有搜尋條件"""
        print("\n📋 可用的搜尋條件:")
        print("=" * 40)
        
        # 預設條件
        default = self.get_default_search_criteria()
        print("🔹 default (預設條件):")
        for key, value in default.items():
            if value:
                print(f"   {key}: {value}")
        
        # 已儲存的條件
        saved = self.get_saved_searches()
        for name, criteria in saved.items():
            print(f"🔹 {name}:")
            for key, value in criteria.items():
                if value:
                    print(f"   {key}: {value}")
        print()
    
    def update_telegram_config(self, bot_token: str, chat_id: str):
        """更新Telegram設定"""
        if 'telegram' not in self.config:
            self.config['telegram'] = {}
        
        self.config['telegram']['bot_token'] = bot_token
        self.config['telegram']['chat_id'] = chat_id
        self.save_config()
        print("✅ Telegram設定已更新")
    
    def update_default_search(self, criteria: Dict[str, str]):
        """更新預設搜尋條件"""
        if 'email_search' not in self.config:
            self.config['email_search'] = {}
        
        self.config['email_search']['default_criteria'] = criteria
        self.save_config()
        print("✅ 預設搜尋條件已更新")

def main():
    """配置管理器測試和互動介面"""
    config_manager = ConfigManager()
    
    while True:
        print("\n🔧 配置管理器")
        print("=" * 30)
        print("1. 查看所有搜尋條件")
        print("2. 新增搜尋條件")
        print("3. 刪除搜尋條件")
        print("4. 更新Telegram設定")
        print("5. 更新預設搜尋條件")
        print("6. 測試搜尋條件")
        print("0. 退出")
        
        choice = input("\n請選擇操作 (0-6): ").strip()
        
        if choice == '0':
            print("👋 再見！")
            break
        elif choice == '1':
            config_manager.list_search_criteria()
        elif choice == '2':
            name = input("輸入搜尋條件名稱: ").strip()
            if name:
                criteria = {}
                subject = input("郵件主旨關鍵字 (可選): ").strip()
                sender = input("寄件者 (可選): ").strip()
                date_after = input("日期篩選 YYYY/MM/DD (可選): ").strip()
                
                if subject:
                    criteria['subject'] = subject
                if sender:
                    criteria['sender'] = sender
                if date_after:
                    criteria['date_after'] = date_after
                
                if criteria:
                    config_manager.add_search_criteria(name, criteria)
                else:
                    print("⚠️ 至少需要設定一個搜尋條件")
        elif choice == '3':
            config_manager.list_search_criteria()
            name = input("輸入要刪除的搜尋條件名稱: ").strip()
            if name:
                config_manager.remove_search_criteria(name)
        elif choice == '4':
            bot_token = input("輸入Telegram Bot Token: ").strip()
            chat_id = input("輸入Telegram Chat ID: ").strip()
            if bot_token and chat_id:
                config_manager.update_telegram_config(bot_token, chat_id)
        elif choice == '5':
            criteria = {}
            subject = input("預設郵件主旨關鍵字 (可選): ").strip()
            sender = input("預設寄件者 (可選): ").strip()
            date_after = input("預設日期篩選 YYYY/MM/DD (可選): ").strip()
            
            if subject:
                criteria['subject'] = subject
            if sender:
                criteria['sender'] = sender
            if date_after:
                criteria['date_after'] = date_after
            
            config_manager.update_default_search(criteria)
        elif choice == '6':
            config_manager.list_search_criteria()
            search_name = input("輸入搜尋條件名稱 (留空使用預設): ").strip()
            search_name = search_name if search_name else None
            
            criteria = config_manager.get_search_criteria(search_name)
            print(f"\n📧 搜尋條件結果:")
            for key, value in criteria.items():
                print(f"   {key}: {value}")
        else:
            print("❌ 無效的選擇")

if __name__ == "__main__":
    main()