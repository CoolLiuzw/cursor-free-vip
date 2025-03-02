import os
import sys
import argparse
from colorama import Fore, Style, init
from cursor_auth import CursorAuth

# 初始化colorama
init()

# 定义emoji和颜色常量
EMOJI = {
    'START': '🚀',
    'KEY': '🔐',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'INFO': 'ℹ️'
}

class TokenUpdater:
    def __init__(self, translator=None):
        self.translator = translator
        self.auth_manager = CursorAuth(translator=self.translator)
    
    def update_token(self, email, token):
        """更新 Cursor 的 token
        
        Args:
            email (str): 邮箱地址
            token (str): 访问令牌
        
        Returns:
            bool: 更新是否成功
        """
        try:
            print(f"{Fore.CYAN}{EMOJI['KEY']} {self.translator.get('token_updater.updating_token')}...{Style.RESET_ALL}")
            
            if self.auth_manager.update_auth(email=email, access_token=token, refresh_token=token):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('token_updater.token_updated')}...{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('token_updater.token_update_failed')}...{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('token_updater.error', error=str(e))}{Style.RESET_ALL}")
            return False

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Cursor Token 更新工具')
    parser.add_argument('--email', type=str, help='邮箱地址')
    parser.add_argument('--token', type=str, help='访问令牌')
    return parser.parse_args()

def main(translator=None):
    """主函数，可以从 main.py 调用或直接运行"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['START']} {translator.get('token_updater.title') if translator else 'Cursor Token 更新工具'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # 检查是否有命令行参数
    args = parse_args()
    email = args.email
    token = args.token
    
    # 如果没有命令行参数，则手动输入
    if not email:
        print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('token_updater.enter_email') if translator else '请输入邮箱地址:'}{Style.RESET_ALL}")
        email = input().strip()
    
    if not token:
        print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('token_updater.enter_token') if translator else '请输入访问令牌:'}{Style.RESET_ALL}")
        token = input().strip()
    
    # 验证输入
    if '@' not in email:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('token_updater.invalid_email') if translator else '无效的邮箱地址'}{Style.RESET_ALL}")
        return False
    
    if not token or len(token) < 20:  # 简单验证 token 长度
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('token_updater.invalid_token') if translator else '无效的访问令牌'}{Style.RESET_ALL}")
        return False
    
    # 更新 token
    updater = TokenUpdater(translator)
    result = updater.update_token(email, token)
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} {translator.get('token_updater.press_enter') if translator else '按回车键退出'}...")
    
    return result

if __name__ == "__main__":
    # 如果直接运行此脚本，尝试导入 main.py 中的 translator
    try:
        from main import translator as main_translator
        main(main_translator)
    except ImportError:
        main(None) 