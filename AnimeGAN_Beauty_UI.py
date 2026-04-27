import cv2
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, scrolledtext
import threading
import os
from datetime import datetime
import onnxruntime as ort
import subprocess

STYLE_MAP = {
    "Hayao": "🌿 吉卜力 · 宫崎骏",
    "Shinkai": "✨ 新海诚 · 唯美日系",
    "JP_face": "👤 二次元人像专用",
    "PortraitSketch": "✏️ 手绘素描线稿",
    "tiny_Cute": "🐱 软萌Q版卡通"
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BeautyAnimeUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AnimeGANv3 高清动漫转换器｜最终完美版")
        self.geometry("850x720")
        self.resizable(False, False)

        self.video_path = ctk.StringVar()
        self.save_path = ctk.StringVar()
        self.model_dict = {}
        self.is_running = False

        title = ctk.CTkLabel(self, text="AI 视频转动漫", font=('微软雅黑', 22, 'bold'))
        title.pack(pady=12)

        f1 = ctk.CTkFrame(self)
        f1.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(f1, text="🎬 输入视频", width=100).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(f1, textvariable=self.video_path).grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(f1, text="选择视频", command=self.select_video, width=90).grid(row=0, column=2, padx=10)
        f1.columnconfigure(1, weight=1)

        f2 = ctk.CTkFrame(self)
        f2.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(f2, text="💾 保存位置", width=100).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(f2, textvariable=self.save_path).grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(f2, text="自定义保存", command=self.select_save_path, width=90).grid(row=0, column=2, padx=10)
        f2.columnconfigure(1, weight=1)

        f3 = ctk.CTkFrame(self)
        f3.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(f3, text="🎨 动漫风格", width=100).grid(row=0, column=0, padx=10, pady=10)
        self.style_box = ctk.CTkComboBox(f3, state="readonly")
        self.style_box.grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(f3, text="刷新模型", command=self.scan_models, width=90).grid(row=0, column=2, padx=10)
        f3.columnconfigure(1, weight=1)

        f4 = ctk.CTkFrame(self)
        f4.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(f4, text="📐 输出分辨率", width=100).grid(row=0, column=0, padx=10, pady=10)
        self.res_box = ctk.CTkComboBox(f4, values=["384","512","720","1080 (默认)"], state="readonly")
        self.res_box.set("1080 (默认)")
        self.res_box.grid(row=0, column=1, sticky="ew", padx=5)
        f4.columnconfigure(1, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self, width=780, height=18)
        self.progress_bar.pack(pady=12)
        self.progress_bar.set(0)
        self.progress_text = ctk.CTkLabel(self, text="进度：0%", font=('微软雅黑',12))
        self.progress_text.pack(pady=2)

        self.run_btn = ctk.CTkButton(self, text="🚀 开始一键转换", font=('微软雅黑',14,'bold'), height=45, corner_radius=12, command=self.start_task)
        self.run_btn.pack(pady=15)

        log_label = ctk.CTkLabel(self, text="📋 运行日志（可全选复制）", font=('微软雅黑',12))
        log_label.pack(anchor="w", padx=25)
        self.log_text = scrolledtext.ScrolledText(self, width=105, height=14, bg="#1a1a2e", fg="#98fb98")
        self.log_text.pack(padx=20, pady=5)

        # 现在创建了 log_text 组件，可以进行设备检测了
        self.provider, self.device_name = self.get_device()
        
        # 创建设备标签
        device_label = ctk.CTkLabel(self, text=f"运行设备：{self.device_name}", text_color="#87CEFA")
        device_label.pack(pady=3)

        self.log("===== 程序启动成功 =====")
        self.scan_models()

    def get_device(self):
        providers = ort.get_available_providers()
        self.log(f"可用设备：{providers}")
        
        # 优先尝试 CUDA
        if "CUDAExecutionProvider" in providers:
            try:
                # 测试 CUDA 是否真正可用
                test_session = ort.InferenceSession(
                    os.path.join(os.getcwd(), "models", os.listdir(os.path.join(os.getcwd(), "models"))[0])
                    if os.path.exists(os.path.join(os.getcwd(), "models")) and os.listdir(os.path.join(os.getcwd(), "models"))
                    else None,
                    providers=["CUDAExecutionProvider"]
                )
                return ["CUDAExecutionProvider"], "NVIDIA 独显加速 ✅"
            except Exception as e:
                self.log(f"CUDA 测试失败：{str(e)}")
        
        # 尝试 DirectML（不需要 CUDA）
        if "DmlExecutionProvider" in providers:
            try:
                # 测试 DirectML 是否真正可用
                test_session = ort.InferenceSession(
                    os.path.join(os.getcwd(), "models", os.listdir(os.path.join(os.getcwd(), "models"))[0])
                    if os.path.exists(os.path.join(os.getcwd(), "models")) and os.listdir(os.path.join(os.getcwd(), "models"))
                    else None,
                    providers=["DmlExecutionProvider"]
                )
                return ["DmlExecutionProvider"], "DirectML GPU 加速 ✅"
            except Exception as e:
                self.log(f"DirectML 测试失败：{str(e)}")
        
        # 最后使用 CPU
        return ["CPUExecutionProvider"], "CPU 低速模式 ⚠️"

    def scan_models(self):
        model_dir = os.path.join(os.getcwd(), "models")
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
            self.log("[提示] 自动创建 models 文件夹，请放入 .onnx 模型")
            self.style_box.configure(values=[])
            return
        file_list = [f for f in os.listdir(model_dir) if f.lower().endswith(".onnx")]
        self.model_dict.clear()
        style_list = []
        for fname in file_list:
            for key, show_name in STYLE_MAP.items():
                if key in fname:
                    self.model_dict[show_name] = os.path.join(model_dir, fname)
                    style_list.append(show_name)
                    break
        self.style_box.configure(values=style_list)
        if style_list:
            self.style_box.set(style_list[0])
            self.log(f"[成功] 自动加载 {len(style_list)} 种动漫风格")
        else:
            self.log("[错误] models 未找到有效模型")

    def log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{t}] {msg}\n")
        self.log_text.see("end")
        self.update()

    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("视频","*.mp4 *.avi *.mov *.mkv")])
        if path:
            self.video_path.set(path)
            self.log(f"已选视频：{os.path.basename(path)}")
            dir_p, name_ex = os.path.split(path)
            name, _ = os.path.splitext(name_ex)
            self.save_path.set(os.path.join(dir_p, f"{name}_动漫成品.mp4"))

    def select_save_path(self):
        path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4视频","*.mp4")])
        if path:
            self.save_path.set(path)
            self.log(f"自定义保存路径：{path}")

    def start_task(self):
        if self.is_running:
            return
        if not os.path.exists(self.video_path.get()):
            self.log("[错误] 请先选择视频")
            return
        if not self.save_path.get():
            self.log("[错误] 请设置保存路径")
            return
        if self.style_box.get() not in self.model_dict:
            self.log("[错误] 请选择风格/刷新模型")
            return

        self.is_running = True
        self.run_btn.configure(state="disabled", text="⏳ 转换中...")
        self.progress_bar.set(0)
        self.progress_text.configure(text="进度：0%")
        threading.Thread(target=self.work, daemon=True).start()

    def work(self):
        try:
            vid_path = self.video_path.get()
            mod_path = self.model_dict[self.style_box.get()]
            out_path = self.save_path.get()
            max_edge = int(self.res_box.get().replace(" (默认)",""))

            self.log(f"使用模型：{os.path.basename(mod_path)}")
            self.log(f"输出分辨率上限：{max_edge}px")
            self.log(f"成品保存至：{out_path}")

            sess = ort.InferenceSession(mod_path, providers=self.provider)
            in_name = sess.get_inputs()[0].name

            cap = cv2.VideoCapture(vid_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            w, h = int(cap.get(3)), int(cap.get(4))

            scale = max_edge / max(w, h)
            nw, nh = int(w * scale), int(h * scale)

            # 🔥 强制尺寸为 32 的倍数（所有模型通用）
            nw = (nw + 31) // 32 * 32
            nh = (nh + 31) // 32 * 32

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(out_path, fourcc, fps, (nw, nh))

            self.log(f"原始 {w}×{h} → 输出 {nw}×{nh}，总帧数：{total}")

            for idx in range(total):
                ret, frame = cap.read()
                if not ret:
                    break

                # ==========================
                # 🔥 100% 正确的预处理
                # ==========================
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (nw, nh))
                img = img.astype(np.float32) / 127.5 - 1.0

                # ✅ 模型需要：NHWC [1,H,W,3]
                img = np.expand_dims(img, axis=0)   # 添加批次维度 NHWC [1,H,W,3]

                out_img = sess.run(None, {in_name: img})[0][0]

                # ✅ 转回图片格式（NHWC 格式不需要转置）
                out_img = np.clip((out_img + 1) * 127.5, 0, 255).astype(np.uint8)
                out_img = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)

                writer.write(out_img)

                progress = (idx + 1) / total
                percent = round(progress * 100, 1)
                self.progress_bar.set(progress)
                self.progress_text.configure(text=f"进度：{percent}%")

                if idx % 30 == 0:
                    self.log(f"处理中：{idx+1}/{total} | {percent}%")

            cap.release()
            writer.release()
            
            # ==========================
            # 🔥 添加原始音频
            # ==========================
            try:
                self.log("\n🎵 正在提取原始音频...")
                
                # 检查 ffmpeg 是否存在
                ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")
                if not os.path.exists(ffmpeg_path):
                    self.log("⚠️ ffmpeg.exe 未找到，跳过音频添加")
                else:
                    # 临时音频文件路径
                    audio_path = out_path.replace(".mp4", "_audio.aac")
                    # 临时输出文件路径
                    temp_path = out_path.replace(".mp4", "_temp.mp4")
                    
                    # 提取原始音频
                    extract_cmd = f"{ffmpeg_path} -i \"{vid_path}\" -vn -c:a aac -b:a 128k \"{audio_path}\""
                    extract_result = subprocess.run(extract_cmd, shell=True, capture_output=True, text=True)
                    
                    if extract_result.returncode == 0 and os.path.exists(audio_path):
                        # 合并音频到转换后的视频
                        merge_cmd = f"{ffmpeg_path} -i \"{out_path}\" -i \"{audio_path}\" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \"{temp_path}\""
                        merge_result = subprocess.run(merge_cmd, shell=True, capture_output=True, text=True)
                        
                        if merge_result.returncode == 0 and os.path.exists(temp_path):
                            # 替换原文件
                            os.remove(out_path)
                            os.rename(temp_path, out_path)
                            # 清理临时文件
                            if os.path.exists(audio_path):
                                os.remove(audio_path)
                            self.log("✅ 音频添加成功！")
                        else:
                            self.log("⚠️ 音频合并失败，跳过音频添加")
                            # 清理临时文件
                            if os.path.exists(audio_path):
                                os.remove(audio_path)
                    else:
                        self.log("⚠️ 原始视频无音频或音频提取失败，跳过音频添加")
            except Exception as e:
                self.log(f"⚠️ 音频处理失败：{str(e)}")
            
            self.progress_bar.set(1)
            self.progress_text.configure(text="✅ 100% 完成！")
            self.log("\n🎉 转换成功！视频已保存！")

        except Exception as e:
            self.log(f"\n❌ 错误：{str(e)}")
        finally:
            self.is_running = False
            self.run_btn.configure(state="normal", text="🚀 开始一键转换")

if __name__ == "__main__":
    app = BeautyAnimeUI()
    app.mainloop()