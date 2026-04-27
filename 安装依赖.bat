@echo off
chcp 65001
echo ==============================================
echo      AnimeGANv3 依赖库安装器
echo ==============================================
echo.
echo 正在安装全部依赖库...
echo.

:: 自动检测 Python 安装位置
set "PYTHON_PATH="

:: 检查默认安装路径
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310"
) else if exist "C:\Program Files\Python310\python.exe" (
    set "PYTHON_PATH=C:\Program Files\Python310"
) else if exist "C:\Program Files (x86)\Python310\python.exe" (
    set "PYTHON_PATH=C:\Program Files (x86)\Python310"
)

:: 检查 Python 是否可用
if defined PYTHON_PATH (
    echo 找到 Python 安装：%PYTHON_PATH%
    echo 临时添加到环境变量...
    set "PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"
    
    :: 显示 Python 版本
    python --version
    echo.
    
    :: 升级 pip
    echo 正在升级 pip...
    python -m pip install --upgrade pip
    echo.
    
    :: 安装依赖库
    echo 正在安装依赖库...
    pip install --force-reinstall opencv-python numpy onnxruntime-gpu onnxruntime-directml customtkinter
    echo.
    
    :: 验证安装
    echo 正在验证安装...
    python -c "import cv2; import numpy; import onnxruntime; import customtkinter; print('cv2 版本:', cv2.__version__); print('numpy 版本:', numpy.__version__); print('onnxruntime 版本:', onnxruntime.__version__); print('customtkinter 版本:', customtkinter.__version__); print('所有依赖安装成功！')"
    if %errorlevel% equ 0 (
        echo.
        echo 安装完成！
    ) else (
        echo.
        echo 安装失败，请手动运行：
        echo pip install opencv-python numpy onnxruntime customtkinter
    )
) else (
    echo 错误：未找到 Python 3.10 安装！
    echo 请先安装 Python 3.7+ 并添加到系统环境变量
    echo 或从官网下载：https://www.python.org/downloads/
)

echo.
echo 按任意键退出...
pause >nul