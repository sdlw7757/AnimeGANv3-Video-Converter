# AnimeGANv3 高清动漫转换器

🎨 **AI 驱动的视频动漫风格转换工具** - 将普通视频转换为精美的动漫风格，支持多种风格选择，保留原始音频。

## 📋 项目简介

AnimeGANv3 高清动漫转换器是一款基于深度学习的视频处理工具，能够将普通视频转换为多种动漫风格。该工具使用 ONNX 模型进行推理，支持 GPU 加速，操作简单直观，适合各种视频动漫化需求。

![AnimeGANv3 界面](<img width="840" height="745" alt="AnimeGANv3 动漫视频转换器" src="https://github.com/user-attachments/assets/66684465-4f65-4d13-a78b-4f625b3c78bd">)


## ✨ 功能特性

- **多种动漫风格**：支持 5 种不同的动漫风格转换
- **高清输出**：支持最高 1080p 分辨率输出
- **音频保留**：自动提取并保留原始视频的音频
- **GPU 加速**：支持 CUDA 和 DirectML GPU 加速
- **智能尺寸调整**：自动调整视频尺寸以获得最佳效果
- **用户友好界面**：直观的图形界面，操作简单
- **批量处理**：支持处理任意长度的视频
- **快速转换**：优化的处理算法，转换速度快

## 🚀 快速开始

### 1. 环境要求

- **操作系统**：Windows 10/11
- **Python**：3.7 或更高版本
- **GPU**（可选）：支持 CUDA 或 DirectML 的显卡

### 2. 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/yourusername/AnimeGANv3.git
   cd AnimeGANv3
   ```

2. **安装依赖**
   - 双击运行 `安装依赖.bat` 文件
   - 或手动执行：
     ```bash
     pip install opencv-python numpy onnxruntime-gpu onnxruntime-directml customtkinter
     ```

3. **下载模型**
   - 在 `models` 文件夹中放置 ONNX 模型文件
   - 支持的模型命名格式：
     - `AnimeGANv3_Hayao_*.onnx` - 吉卜力·宫崎骏风格
     - `AnimeGANv3_Shinkai_*.onnx` - 新海诚·唯美日系风格
     - `AnimeGANv3_JP_face_*.onnx` - 二次元人像专用风格
     - `AnimeGANv3_PortraitSketch_*.onnx` - 手绘素描线稿风格
     - `AnimeGANv3_tiny_Cute_*.onnx` - 软萌Q版卡通风格

4. **准备 ffmpeg**（用于音频处理）
   - 下载 ffmpeg.exe 并放置在项目根目录
   - 或从 [ffmpeg 官网](https://ffmpeg.org/download.html) 下载

### 3. 运行程序

- 双击运行 `启动转换器.bat` 文件
- 程序会自动检测环境并启动

## 🎯 使用方法

1. **选择视频**：点击 "选择视频" 按钮，选择要转换的视频文件
2. **选择风格**：从 "动漫风格" 下拉菜单中选择喜欢的风格
3. **设置分辨率**：选择输出视频的分辨率上限
4. **开始转换**：点击 "开始一键转换" 按钮
5. **查看结果**：转换完成后，视频会保存到指定位置

### 风格说明

| 风格选项 | 描述 | 适用场景 |
|---------|------|----------|
| 🌿 吉卜力 · 宫崎骏 | 经典吉卜力动画风格，色彩丰富 | 风景、人物、奇幻场景 |
| ✨ 新海诚 · 唯美日系 | 新海诚电影风格，细腻唯美 | 城市、夜景、情感场景 |
| 👤 二次元人像专用 | 专门针对人物肖像优化 | 人物特写、自拍视频 |
| ✏️ 手绘素描线稿 | 黑白素描风格，艺术感强 | 艺术创作、概念设计 |
| 🐱 软萌Q版卡通 | 可爱Q版风格，适合儿童 | 卡通形象、儿童视频 |

## 🛠️ 技术原理

1. **模型架构**：基于 AnimeGANv3 架构，使用深度学习生成动漫风格
2. **推理引擎**：使用 ONNX Runtime 进行高效推理
3. **加速技术**：支持 CUDA 和 DirectML GPU 加速
4. **视频处理**：
   - 逐帧读取视频
   - 应用风格转换模型
   - 合并原始音频
   - 输出处理后的视频

## ⚡ 性能优化

- **GPU 加速**：优先使用 CUDA 或 DirectML 进行 GPU 加速
- **批量处理**：优化的帧处理流程
- **内存管理**：高效的内存使用，支持处理高清视频
- **尺寸优化**：自动调整视频尺寸以获得最佳效果

## ❓ 常见问题

### Q: 为什么转换速度很慢？
A: 检查是否启用了 GPU 加速。如果显示 "CPU 低速模式"，说明没有成功启用 GPU 加速。

### Q: 为什么转换后的视频没有声音？
A: 确保 ffmpeg.exe 文件存在于项目根目录。如果仍然没有声音，可能是原始视频没有音频轨道。

### Q: 为什么某些风格转换失败？
A: 确保模型文件名称正确，并且尺寸是 32 的倍数。如果问题持续，请尝试使用不同的分辨率设置。

### Q: 支持哪些视频格式？
A: 支持 MP4、AVI、MOV、MKV 等常见视频格式。

### Q: 如何提高转换质量？
A: 选择较高的输出分辨率，使用适合视频内容的风格模型。

## 📁 项目结构

```
AnimeGANv3/
├── AnimeGAN_Beauty_UI.py    # 主程序文件
├── 启动转换器.bat           # 启动脚本
├── 安装依赖.bat             # 依赖安装脚本
├── models/                  # 模型文件夹
│   ├── AnimeGANv3_Hayao_36.onnx
│   ├── AnimeGANv3_Shinkai_36.onnx
│   ├── AnimeGANv3_JP_face_36.onnx
│   ├── AnimeGANv3_PortraitSketch_36.onnx
│   └── AnimeGANv3_tiny_Cute.onnx
├── ffmpeg.exe              # 音频处理工具
└── README.md               # 项目说明
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢 AnimeGAN 团队的开源贡献
- 感谢 ONNX Runtime 提供的高效推理引擎
- 感谢所有支持和使用本项目的用户

---

**享受动漫风格转换的乐趣！** 🎉
