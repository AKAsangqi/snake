import os
import subprocess
import sys
import time
import socket
import urllib.request

def check_internet_connection():
    """检查互联网连接"""
    try:
        # 尝试连接到GitHub
        socket.create_connection(("github.com", 443), timeout=5)
        return True
    except OSError:
        return False

def run_command(command, max_retries=3, retry_delay=2):
    """运行命令并打印输出，支持重试"""
    print(f"执行: {command}")
    
    for attempt in range(max_retries):
        if attempt > 0:
            print(f"重试 ({attempt}/{max_retries-1})...")
            time.sleep(retry_delay)
            
        process = subprocess.run(command, shell=True, text=True, capture_output=True, encoding='utf-8')
        
        if process.stdout:
            print(process.stdout)
            
        if process.stderr:
            print(f"错误: {process.stderr}")
            
        if process.returncode == 0:
            return True
        elif "Connection was reset" in process.stderr or "timed out" in process.stderr:
            print("网络连接问题，准备重试...")
            continue
        else:
            # 其他错误，不重试
            break
            
    return False

def check_git_installed():
    """检查Git是否已安装"""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def init_git_repo():
    """初始化Git仓库"""
    if os.path.exists(".git"):
        print("Git仓库已存在")
        return True
    
    return run_command("git init")

def add_files():
    """添加文件到Git仓库"""
    return run_command("git add .")

def commit_changes(message="初始提交贪吃蛇游戏"):
    """提交更改"""
    process = subprocess.run(f'git commit -m "{message}"', shell=True, text=True, capture_output=True, encoding='utf-8')
    if process.stdout:
        print(process.stdout)
    if process.stderr:
        print(f"错误: {process.stderr}")
    
    # 检查是否是因为没有更改而无法提交
    if "nothing to commit" in process.stdout:
        print("没有新的更改需要提交，继续执行...")
        return True
    
    return process.returncode == 0

def check_remote_exists():
    """检查远程仓库是否已存在"""
    process = subprocess.run("git remote -v", shell=True, text=True, capture_output=True, encoding='utf-8')
    return "origin" in process.stdout

def remove_remote():
    """删除已存在的远程仓库"""
    return run_command("git remote remove origin")

def add_remote(repo_url):
    """添加远程仓库"""
    # 检查远程仓库是否已存在
    if check_remote_exists():
        print("远程仓库'origin'已存在")
        choice = input("是否更新远程仓库URL? (y/n): ").strip().lower()
        if choice == 'y':
            if not remove_remote():
                print("删除已存在的远程仓库失败")
                return False
        else:
            print("保留现有远程仓库")
            return True
    
    return run_command(f"git remote add origin {repo_url}")

def check_git_credentials():
    """检查Git凭据是否已配置"""
    name_process = subprocess.run("git config --global user.name", shell=True, text=True, capture_output=True, encoding='utf-8')
    email_process = subprocess.run("git config --global user.email", shell=True, text=True, capture_output=True, encoding='utf-8')
    
    has_name = name_process.stdout.strip() != ""
    has_email = email_process.stdout.strip() != ""
    
    return has_name and has_email

def configure_git_credentials():
    """配置Git凭据"""
    print("\n您需要配置Git用户名和邮箱才能推送到GitHub")
    name = input("请输入您的Git用户名: ").strip()
    email = input("请输入您的Git邮箱: ").strip()
    
    if name and email:
        run_command(f'git config --global user.name "{name}"')
        run_command(f'git config --global user.email "{email}"')
        print("Git凭据配置成功!")
        return True
    else:
        print("错误: 用户名和邮箱不能为空")
        return False

def push_to_github(max_retries=3):
    """推送到GitHub，支持重试和错误处理"""
    # 检查网络连接
    if not check_internet_connection():
        print("错误: 无法连接到互联网，请检查您的网络连接")
        return False
    
    # 尝试推送
    print("正在推送到GitHub...")
    result = run_command("git push -u origin master", max_retries=max_retries)
    
    if not result:
        print("\n推送失败，可能的原因:")
        print("1. 网络连接问题 - 请检查您的网络连接是否稳定")
        print("2. GitHub身份验证问题 - 请确保您已正确配置Git凭据")
        print("3. 防火墙或代理设置 - 可能阻止了与GitHub的连接")
        print("4. GitHub服务器问题 - GitHub可能暂时不可用")
        
        print("\n尝试解决方案:")
        print("- 检查网络连接并重试")
        print("- 确认GitHub仓库URL是否正确")
        print("- 尝试使用SSH而不是HTTPS (需要设置SSH密钥)")
        print("- 检查防火墙设置是否阻止了Git连接")
        print("- 稍后再试")
        
        # 提供使用SSH的选项
        choice = input("\n是否尝试配置SSH密钥? (y/n): ").strip().lower()
        if choice == 'y':
            print("\nSSH密钥配置指南:")
            print("1. 生成SSH密钥: ssh-keygen -t ed25519 -C \"your_email@example.com\"")
            print("2. 将公钥添加到GitHub: https://github.com/settings/keys")
            print("3. 测试SSH连接: ssh -T git@github.com")
            print("4. 更改远程URL: git remote set-url origin git@github.com:username/repository.git")
        
        return False
    
    return True

def main():
    # 检查Git是否已安装
    if not check_git_installed():
        print("错误: 未检测到Git。请先安装Git: https://git-scm.com/downloads")
        return
    
    print("=== 贪吃蛇游戏GitHub上传工具 ===")
    
    # 检查网络连接
    print("检查网络连接...")
    if not check_internet_connection():
        print("警告: 无法连接到互联网，请检查您的网络连接后再继续")
        choice = input("是否继续尝试? (y/n): ").strip().lower()
        if choice != 'y':
            return
    else:
        print("网络连接正常")
    
    # 检查Git凭据
    if not check_git_credentials():
        print("警告: 未检测到Git用户名或邮箱配置")
        if not configure_git_credentials():
            print("未配置Git凭据，可能会影响推送到GitHub的操作")
            choice = input("是否继续? (y/n): ").strip().lower()
            if choice != 'y':
                return
    
    # 初始化Git仓库
    if not init_git_repo():
        print("初始化Git仓库失败")
        return
    
    # 添加文件
    if not add_files():
        print("添加文件失败")
        return
    
    # 提交更改
    commit_message = input("请输入提交信息 (默认: '初始提交贪吃蛇游戏'): ").strip()
    if not commit_message:
        commit_message = "初始提交贪吃蛇游戏"
    
    if not commit_changes(commit_message):
        print("提交更改失败")
        return
    
    # 获取GitHub仓库URL
    while True:
        repo_url = input("请输入GitHub仓库URL (例如: https://github.com/username/snake-game.git): ").strip()
        if not repo_url:
            print("错误: 必须提供GitHub仓库URL")
            continue
        
        # 简单验证URL格式
        if not (repo_url.startswith("https://github.com/") or repo_url.startswith("git@github.com:")):
            print("警告: URL格式可能不正确，请确保使用正确的GitHub仓库URL")
            choice = input("是否继续使用此URL? (y/n): ").strip().lower()
            if choice != 'y':
                continue
        break
    
    # 添加远程仓库
    if not add_remote(repo_url):
        print("添加/更新远程仓库失败")
        return
    
    # 推送到GitHub
    print("\n准备推送到GitHub...")
    print("注意: 如果这是您第一次推送到GitHub，可能会弹出登录窗口要求您输入GitHub凭据")
    input("按回车键继续...")
    
    if not push_to_github():
        print("\n推送失败，是否要尝试使用HTTPS方式重新推送? (y/n): ")
        choice = input().strip().lower()
        if choice == 'y':
            # 如果是SSH URL，尝试转换为HTTPS
            if repo_url.startswith("git@github.com:"):
                https_url = repo_url.replace("git@github.com:", "https://github.com/")
                if https_url.endswith(".git") and not repo_url.endswith(".git"):
                    https_url = https_url[:-4]
                print(f"尝试使用HTTPS URL: {https_url}")
                if remove_remote() and add_remote(https_url) and push_to_github():
                    repo_url = https_url  # 更新成功的URL
                    print("\n成功! 贪吃蛇游戏已上传到GitHub!")
                    print(f"仓库地址: {repo_url}")
                    return
        return
    
    print("\n成功! 贪吃蛇游戏已上传到GitHub!")
    print(f"仓库地址: {repo_url}")

if __name__ == "__main__":
    main()