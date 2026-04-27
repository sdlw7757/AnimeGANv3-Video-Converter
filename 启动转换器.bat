@echo off
chcp 65001
title AnimeGAN 精美UI转换器
color 0B

echo ==============================================
echo      AnimeGANv3 动漫视频转换器 一键启动
echo ==============================================
echo.
echo 当前目录：%CD%
echo.
echo 正在启动程序...
echo.

if not exist "AnimeGAN_Beauty_UI.py" (
    echo 错误：找不到 AnimeGAN_Beauty_UI.py 文件！
    echo 请确保启动脚本和 Python 文件在同一目录
    echo.
    pause
    exit /b 1
)

set "PYTHON_PATH="

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310"
) else if exist "C:\Program Files\Python310\python.exe" (
    set "PYTHON_PATH=C:\Program Files\Python310"
) else if exist "C:\Program Files (x86)\Python310\python.exe" (
    set "PYTHON_PATH=C:\Program Files (x86)\Python310"
)

if defined PYTHON_PATH (
    echo 找到 Python 安装：%PYTHON_PATH%
    echo 临时添加到环境变量...
    set "PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"
    
    python --version
    if %errorlevel% equ 0 (
        echo Python 验证成功，正在检查依赖...
        
        echo 正在检查依赖库...
        python -c "import cv2; import numpy; import onnxruntime; import customtkinter" >nul 2>&1
        
        if %errorlevel% neq 0 (
            echo 缺少依赖库，正在安装...
            echo 正在升级 pip...
            python -m pip install --upgrade pip >nul 2>&1
            echo.
            
            pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python numpy onnxruntime-gpu onnxruntime-directml customtkinter
            if %errorlevel% neq 0 (
                echo 错误：依赖库安装失败！
                echo 正在尝试使用 --user 选项安装...
                pip install --user -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python numpy onnxruntime-gpu onnxruntime-directml customtkinter
                if %errorlevel% neq 0 (
                    echo 错误：依赖库安装失败！
                    echo 请手动运行：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python numpy onnxruntime-gpu onnxruntime-directml customtkinter
                    echo.
                    pause
                    exit /b 1
                )
            )
        ) else (
            echo 依赖库已安装，跳过安装步骤
        )
        
        echo 依赖库检查通过
        echo 正在启动程序...
        python AnimeGAN_Beauty_UI.py
    ) else (
        echo 错误：Python 验证失败！
        echo 请手动添加 Python 到系统环境变量
        echo.
        pause
        exit /b 1
    )
) else (
    echo 错误：未找到 Python 3.10 安装！
    echo 请先安装 Python 3.7+ 并添加到系统环境变量
    echo 或从官网下载：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo 程序已退出，按任意键关闭窗口
pause >nul