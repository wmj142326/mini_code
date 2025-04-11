import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk
import webbrowser  # 导入 webbrowser 模块


def convert_npy_to_txt(file_path, output_path):
    try:
        # 尝试加载np.npy文件，并捕获可能的格式错误
        try:
            data = np.load(file_path, allow_pickle=True)  # 允许加载pickle格式的数据
        except Exception as e:
            raise ValueError(f"无法加载 NPY 文件 {file_path}。可能是格式不一致或损坏：{e}")

        file_dir, file_name = os.path.split(output_path)
        file_base, file_ext = os.path.splitext(file_name)

        # 如果数据是标量（0D），将其转换为1D数组
        if data.ndim == 0:
            data = np.array([data])
        # 检查数据类型，如果是字符串类型，则使用 %s 格式化
        if np.issubdtype(data.dtype, np.str_):
            new_file_name = f"{file_base}_{data.shape}{file_ext}"
            new_output_path = os.path.join(file_dir, new_file_name)
            np.savetxt(new_output_path, data, fmt='%s')
        else:
            new_file_name = f"{file_base}_{data.shape}{file_ext}"
            new_output_path = os.path.join(file_dir, new_file_name)
            np.savetxt(new_output_path, data)
        print(f"成功将 {file_path} 转换为 {new_output_path}")

    except Exception as e:
        messagebox.showerror("错误", f"转换 NPY 文件失败：{file_path}\n{e}")


def convert_npz_to_txt(file_path, output_dir):
    try:
        data = np.load(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_folder = os.path.join(output_dir, base_name)
        os.makedirs(output_folder, exist_ok=True)

        # 将每个项转换为单独的txt文件
        for name, array in data.items():
            print(name)

            # 如果数组是 0D（标量），将其转换为 1D 数组
            if array.ndim == 0:
                array = np.array([array])

            # 检查数组的类型，并保存
            if np.issubdtype(array.dtype, np.str_):
                np.savetxt(os.path.join(output_folder, f"{name}_{array.shape}.txt"), array, fmt='%s')
            else:
                np.savetxt(os.path.join(output_folder, f"{name}_{array.shape}.txt"), array)
            print(f"成功将 {name} 保存为 {os.path.join(output_folder, f'{name}_{array.shape}.txt')}")

    except Exception as e:
        messagebox.showerror("错误", f"转换 NPZ 文件失败：{file_path}\n{e}")


def browse_files_or_folder():
    choice = file_mode.get()
    selected_files = []
    file_extension = ".npy" if file_type.get() == "npy" else ".npz"  # 根据选择的文件类型，确定后缀

    if choice == "file":
        selected_files = filedialog.askopenfilenames(
            title="选择文件",
            filetypes=[("所有文件", "*.*"), (f"{file_extension} 文件", f"*{file_extension}")],
        )
    elif choice == "folder":
        folder_path = filedialog.askdirectory(title="选择文件夹")
        if folder_path:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(file_extension):  # 只选择指定后缀的文件
                        selected_files.append(os.path.join(root, file))

    file_listbox.delete(0, tk.END)
    for f in selected_files:
        file_listbox.insert(tk.END, f)
    return selected_files


def browse_output_path():
    output = filedialog.askdirectory(title="选择输出路径")
    output_path_var.set(output)


def run_conversion():
    selected_files = file_listbox.get(0, tk.END)
    output_dir = output_path_var.get()
    file_type_choice = file_type.get()

    if not selected_files:
        messagebox.showwarning("提示", "请选择文件或文件夹")
        return

    if not output_dir:
        messagebox.showwarning("提示", "请选择输出路径")
        return

    for file_path in selected_files:
        ext = os.path.splitext(file_path)[-1].lower()
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if ext == ".npy" and file_type_choice in ["npy", "all"]:
            output_path = os.path.join(output_dir, base_name + ".txt")
            convert_npy_to_txt(file_path, output_path)
        elif ext == ".npz" and file_type_choice in ["npz", "all"]:
            convert_npz_to_txt(file_path, output_dir)

    messagebox.showinfo("完成", "转换完成！")


# =========================
# ===== GUI 开始 =====
# =========================
root = tk.Tk()
root.title("NPY/NPZ 转换为 TXT 工具")
root.geometry("800x600")

# 主框架，左右布局
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True)

# 左边控件区
left_frame = ttk.Frame(main_frame)
left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

# 右边 logo 和欢迎语
right_frame = ttk.Frame(main_frame)
right_frame.pack(side='right', fill='y', padx=10, pady=10)

# ==== 右侧内容 ====
# 尝试加载logo图片
try:
    img = Image.open("logo.png")
    img = img.resize((150, 150))  # 调整大小
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(right_frame, image=photo)
    img_label.image = photo  # 保持对图片的引用
    img_label.pack(pady=5)
except Exception as e:
    print("未找到 logo.png 或无法加载：", e)

# 使用 Text 控件代替 Label，实现多个超链接
welcome_text = tk.Text(right_frame, width=28, height=8, font=("Arial", 10), wrap="word", borderwidth=0)
welcome_text.insert(tk.END, "欢迎使用 NPY/NPZ 转 TXT 工具！\n")

# 设置两个超链接
welcome_text.insert(tk.END, "\n项目地址：\n")
welcome_text.insert(tk.END, "https://github.com/minicode/\n", "project")

welcome_text.insert(tk.END, "\n欢迎访问我的个人主页：\n")
welcome_text.insert(tk.END, "https://wmj142326.github.io/\n", "documentation")

# 设置 tag 样式
welcome_text.tag_config("project", foreground="blue", underline=True)
welcome_text.tag_config("documentation", foreground="blue", underline=True)

# 绑定点击事件
welcome_text.tag_bind("project", "<Button-1>", lambda e: webbrowser.open("https://github.com/wmj142326/mini_code/"))
welcome_text.tag_bind("documentation", "<Button-1>", lambda e: webbrowser.open("https://wmj142326.github.io/"))

# 禁止编辑
welcome_text.config(state="disabled", cursor="hand2")
welcome_text.pack(pady=5)

# ==== 左侧内容 ====
file_mode = tk.StringVar(value="file")
file_type = tk.StringVar(value="npy")
output_path_var = tk.StringVar()

# 功能选择
mode_frame = ttk.LabelFrame(left_frame, text="功能选择")
mode_frame.pack(fill='x', pady=5)
ttk.Radiobutton(mode_frame, text="仅 NPY", variable=file_type, value="npy").pack(anchor='w')
ttk.Radiobutton(mode_frame, text="仅 NPZ", variable=file_type, value="npz").pack(anchor='w')
ttk.Radiobutton(mode_frame, text="NPY 和 NPZ", variable=file_type, value="all").pack(anchor='w')

# 方式选择
mode_frame = ttk.LabelFrame(left_frame, text="方式选择")
mode_frame.pack(fill='x', pady=5)
ttk.Radiobutton(mode_frame, text="文件", variable=file_mode, value="file").pack(anchor='w')
ttk.Radiobutton(mode_frame, text="文件夹", variable=file_mode, value="folder").pack(anchor='w')

# 按钮和文件列表
ttk.Button(left_frame, text="选择文件或文件夹", command=browse_files_or_folder).pack(fill='x', pady=5)
file_listbox = tk.Listbox(left_frame, height=10)
file_listbox.pack(fill='both', pady=5, expand=True)

# 输出路径
output_frame = ttk.Frame(left_frame)
output_frame.pack(fill='x', pady=5)
ttk.Label(output_frame, text="输出路径：").pack(side='left')
ttk.Entry(output_frame, textvariable=output_path_var, width=40).pack(side='left', padx=5)
ttk.Button(output_frame, text="浏览", command=browse_output_path).pack(side='left')

# 开始转换按钮
ttk.Button(left_frame, text="开始转换", command=run_conversion).pack(fill='x', pady=10)

root.mainloop()

"""
pyinstaller --onefile --windowed --icon=npz.ico --add-data "logo.png;." npy_npz2txt.py
"""
