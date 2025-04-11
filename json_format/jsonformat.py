import os
import json
import pickle
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
import webbrowser
from datetime import datetime, date, time
from pathlib import Path
import types


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


def safe_json(obj, path="root", log_list=None):
    if log_list is None:
        log_list = []

    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj

    elif isinstance(obj, (np.integer, np.floating)):
        log_list.append(f"{path} 是 {type(obj).__name__}，已转换为基本类型")
        return obj.item()

    elif isinstance(obj, np.ndarray):
        log_list.append(f"{path} 是 numpy.ndarray，已转换为 list")
        return obj.tolist()

    elif isinstance(obj, (set, frozenset)):
        log_list.append(f"{path} 是 set，已转换为 list")
        return list(obj)

    elif isinstance(obj, (bytes, bytearray)):
        log_list.append(f"{path} 是 bytes，已转换为 utf-8 字符串")
        return obj.decode("utf-8", errors="replace")

    elif isinstance(obj, complex):
        log_list.append(f"{path} 是 complex，已转换为字符串")
        return f"{obj.real}+{obj.imag}j"

    elif isinstance(obj, (datetime, date, time)):
        log_list.append(f"{path} 是 datetime 类型，已转换为 ISO 格式字符串")
        return obj.isoformat()

    elif isinstance(obj, Path):
        log_list.append(f"{path} 是 pathlib.Path，已转换为字符串")
        return str(obj)

    elif isinstance(obj, (types.FunctionType, types.BuiltinFunctionType, types.ModuleType)):
        log_list.append(f"{path} 是 {type(obj).__name__}，不支持序列化，已转换为描述字符串")
        return f"<<non-serializable: {type(obj).__name__}>>"

    elif isinstance(obj, dict):
        return {str(k): safe_json(v, f"{path}.{k}", log_list) for k, v in obj.items()}

    elif isinstance(obj, (list, tuple)):
        return [safe_json(item, f"{path}[{i}]", log_list) for i, item in enumerate(obj)]

    else:
        log_list.append(f"{path} 是 {type(obj).__name__}，未支持，使用 str() 转换")
        return str(obj)


def format_json_file(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_data)
    except Exception as e:
        messagebox.showerror("错误", f"格式化 JSON 文件失败：{file_path}\n{e}")


def convert_pkl_to_json(file_path, output_path):
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        safe_data = safe_json(data)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(safe_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("错误", f"转换 PKL 文件失败：{file_path}\n{e}")


def convert_json_to_pkl(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(output_path, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        messagebox.showerror("错误", f"转换 JSON 文件失败：{file_path}\n{e}")


def process_files(file_paths, output_dir, file_type, conversion_type):
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[-1].lower()
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, base_name + (".json" if conversion_type != "json_to_pkl" else ".pkl"))

        if ext == ".pkl" and file_type in ["pkl", "all"]:
            if conversion_type == "json_to_pkl":
                convert_json_to_pkl(file_path, output_path)
            else:
                convert_pkl_to_json(file_path, output_path)

        elif ext == ".json" and file_type in ["json", "all"]:
            if conversion_type == "json_to_pkl":
                convert_json_to_pkl(file_path, output_path)
            else:
                format_json_file(file_path, output_path)


def browse_files_or_folder():
    choice = file_mode.get()
    selected_files = []
    file_extension = ".json" if file_type.get() == "json" else ".pkl"  # 根据选择的文件类型，确定后缀

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
    conversion_choice = conversion_type.get()

    if not selected_files:
        messagebox.showwarning("提示", "请选择文件或文件夹")
        return

    if not output_dir:
        messagebox.showwarning("提示", "请选择输出路径")
        return

    process_files(selected_files, output_dir, file_type_choice, conversion_choice)
    messagebox.showinfo("完成", "转换完成！")


# =========================
# ===== GUI 开始 =====
# =========================
root = tk.Tk()
root.title("PKL/JSON 格式化转换工具")
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
try:
    img = Image.open("logo.png")
    img = img.resize((150, 150))
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(right_frame, image=photo)
    img_label.image = photo
    img_label.pack(pady=5)
except Exception as e:
    print("未找到 logo.png 或无法加载：", e)

# 使用 Text 控件代替 Label，实现多个超链接

welcome_text = tk.Text(right_frame, width=28, height=8, font=("Arial", 10), wrap="word", borderwidth=0)

welcome_text.insert(tk.END, "欢迎使用 JSON 格式化工具！\n")

welcome_text.insert(tk.END, "\n 项目地址：\n")
welcome_text.insert(tk.END, "github/minicode/\n", "project")

welcome_text.insert(tk.END, "\n欢迎访问我的个人主页：\n")
welcome_text.insert(tk.END, "https://wmj142326.github.io/\n", "homepage")

# 设置 tag 样式
welcome_text.tag_config("homepage", foreground="blue", underline=True)
welcome_text.tag_config("project", foreground="blue", underline=True)

# 禁止编辑
welcome_text.config(state="disabled", cursor="hand2")
welcome_text.pack(pady=5)


# 点击事件
def open_link(event):
    idx = welcome_text.index("@%s,%s" % (event.x, event.y))
    tags = welcome_text.tag_names(idx)
    if "homepage" in tags:
        webbrowser.open_new("https://wmj142326.github.io/")
    elif "project" in tags:
        webbrowser.open_new("https://github.com/wmj142326/mini_code/")


welcome_text.bind("<Button-1>", open_link)

# ==== 左侧内容 ====
file_mode = tk.StringVar(value="file")
file_type = tk.StringVar(value="json")
conversion_type = tk.StringVar(value="json_format")
output_path_var = tk.StringVar()

# 功能选择
mode_frame = ttk.LabelFrame(left_frame, text="功能选择")
mode_frame.pack(fill='x', pady=5)
ttk.Radiobutton(mode_frame, text="JSON转PKL", variable=conversion_type, value="json_to_pkl").pack(anchor='w')
ttk.Radiobutton(mode_frame, text="JSON格式化", variable=conversion_type, value="json_format").pack(anchor='w')

# 方式选择
mode_frame = ttk.LabelFrame(left_frame, text="方式选择")
mode_frame.pack(fill='x', pady=5)
ttk.Radiobutton(mode_frame, text="文件", variable=file_mode, value="file").pack(anchor='w')
ttk.Radiobutton(mode_frame, text="文件夹", variable=file_mode, value="folder").pack(anchor='w')

# 处理文件类型
type_frame = ttk.LabelFrame(left_frame, text="处理文件类型")
type_frame.pack(fill='x', pady=5)
ttk.Radiobutton(type_frame, text="仅 JSON", variable=file_type, value="json").pack(anchor='w')
ttk.Radiobutton(type_frame, text="仅 PKL", variable=file_type, value="pkl").pack(anchor='w')
ttk.Radiobutton(type_frame, text="PKL 和 JSON", variable=file_type, value="all").pack(anchor='w')

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
pyinstaller --onefile --windowed --icon=json.ico --add-data "logo.png;." jsonformat.py
"""
