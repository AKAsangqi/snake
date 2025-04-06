import os
import sys
import subprocess
import importlib.util

def build_exe():
    """
    使用PyInstaller将贪吃蛇游戏打包成可执行文件
    """
    try:
        # 检查PyInstaller是否已安装
        import PyInstaller
        print("PyInstaller已安装，开始打包...")
    except ImportError:
        print("PyInstaller未安装，正在尝试安装...")
        try:
            # 尝试安装PyInstaller
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
            print("PyInstaller安装成功")
        except Exception as e:
            print(f"安装PyInstaller失败: {e}")
            print("请手动安装PyInstaller: pip install pyinstaller")
            return
    
    # 使用Python模块方式运行PyInstaller，而不是依赖命令行命令
    print("开始打包...")
    pyinstaller_args = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=贪吃蛇",
        "--icon=NONE",
        "snake_game.py"
    ]
    print(f"执行命令: {' '.join(pyinstaller_args)}")
    
    try:
        # 执行PyInstaller打包命令
        subprocess.run(pyinstaller_args, check=True)
        print("PyInstaller执行完成")
    except subprocess.CalledProcessError as e:
        print(f"打包过程中出错: {e}")
        print("打包失败，请检查错误信息")
        return
    except FileNotFoundError:
        print("无法找到Python解释器或PyInstaller模块")
        print("请确保PyInstaller已正确安装")
        return
    
    # 检查是否成功生成exe文件
    exe_path = os.path.join("dist", "贪吃蛇.exe")
    if os.path.exists(exe_path):
        print(f"\n打包成功! 可执行文件位于: {os.path.abspath(exe_path)}")
        print("您可以双击该文件运行贪吃蛇游戏")
    else:
        print("\n打包失败，请检查错误信息")

if __name__ == "__main__":
    build_exe()