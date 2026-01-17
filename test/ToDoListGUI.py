# -*- coding: utf-8 -*-
# Python 图形界面版 记事本/日记程序 (tkinter实现)
# 核心功能：新建笔记、打开笔记、编辑笔记、保存笔记、自动按日期命名、文件持久化
# 核心模块：tkinter(图形界面)、os(文件操作)、datetime(日期命名)、tkinter弹窗组件
import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from datetime import datetime

# ===================== 图形记事本主程序 =====================
class GuiNotebook:
    def __init__(self, root):
        # 初始化主窗口
        self.root = root
        self.root.title("✨ Python 图形记事本 - 日记专用 ✨")  # 窗口标题
        self.root.geometry("800x600")  # 窗口默认大小：宽800 高600
        
        # 定义变量：记录当前打开的文件路径，初始为空
        self.file_path = None
        
        # 创建【带滚动条的多行编辑区】核心组件（记事本的编辑区域）
        self.text_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("宋体", 12), bg="#f8f9fa", fg="#212529"
        )
        # 让编辑区占满整个窗口
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        # 创建【菜单栏】：新建/打开/保存/另存为/退出 (标准记事本样式)
        self.create_menu()

    def create_menu(self):
        """创建顶部菜单栏"""
        # 创建主菜单
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # 创建【文件】子菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        
        # 文件菜单的功能选项，绑定对应的功能函数
        file_menu.add_command(label="新建笔记", command=self.new_note, accelerator="Ctrl+N")
        file_menu.add_command(label="打开笔记", command=self.open_note, accelerator="Ctrl+O")
        file_menu.add_separator()  # 分隔线
        file_menu.add_command(label="保存笔记", command=self.save_note, accelerator="Ctrl+S")
        file_menu.add_command(label="另存为", command=self.save_as_note)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 绑定快捷键（和Windows记事本一致）
        self.root.bind("<Control-n>", lambda e: self.new_note())
        self.root.bind("<Control-o>", lambda e: self.open_note())
        self.root.bind("<Control-s>", lambda e: self.save_note())

    def new_note(self):
        """新建笔记：清空编辑区，重置文件路径"""
        if self.text_area.get(1.0, tk.END).strip():  # 判断是否有未保存内容
            if messagebox.askyesno("提示", "当前笔记有未保存内容，是否新建空白笔记？"):
                self.text_area.delete(1.0, tk.END)
                self.file_path = None
                self.root.title("✨ Python 图形记事本 - 日记专用 ✨")
        else:
            self.text_area.delete(1.0, tk.END)
            self.file_path = None

    def open_note(self):
        """打开笔记：弹出文件选择框，选择txt文件并读取内容"""
        # 弹出文件选择窗口，只允许选择txt文本文件
        file_path = filedialog.askopenfilename(
            title="打开笔记",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialdir="./"  # 默认打开当前程序所在文件夹
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # 清空编辑区，写入读取的内容
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.file_path = file_path
                # 窗口标题显示当前打开的文件名
                self.root.title(f"✨ {os.path.basename(file_path)} - Python图形记事本 ✨")
                messagebox.showinfo("成功", f"已打开笔记：{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"打开笔记失败：{str(e)}")

    def auto_save_by_date(self):
        """核心功能：自动按【年月日】生成文件名保存，和你原版本逻辑完全一致"""
        # 获取当前日期，格式化：2026-01-18
        current_date = datetime.now().strftime("%Y-%m-%d")
        # 自动生成文件名：2026-01-18_我的日记.txt
        file_name = f"{current_date}_我的日记.txt"
        # 解决同一天多篇日记重名问题：自动加序号 2026-01-18_我的日记_1.txt
        num = 1
        while os.path.exists(file_name):
            file_name = f"{current_date}_我的日记_{num}.txt"
            num += 1
        # 保存文件到当前程序所在文件夹
        full_path = os.path.join("./", file_name)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                # 获取编辑区所有内容
                content = self.text_area.get(1.0, tk.END)
                f.write(content)
            self.file_path = full_path
            self.root.title(f"✨ {file_name} - Python图形记事本 ✨")
            messagebox.showinfo("保存成功", f"笔记已自动保存为：\n{file_name}\n保存在当前程序文件夹")
        except Exception as e:
            messagebox.showerror("保存失败", f"自动保存失败：{str(e)}")

    def save_note(self):
        """保存笔记：优先自动按日期命名保存，已保存过的文件直接覆盖"""
        if self.file_path:  # 如果文件已经保存过，直接覆盖
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    content = self.text_area.get(1.0, tk.END)
                    f.write(content)
                messagebox.showinfo("保存成功", "笔记已更新保存！")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存失败：{str(e)}")
        else:  # 新笔记，调用自动按日期命名保存
            self.auto_save_by_date()

    def save_as_note(self):
        """另存为：自定义文件名和保存路径"""
        file_path = filedialog.asksaveasfilename(
            title="另存为",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialdir="./"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    content = self.text_area.get(1.0, tk.END)
                    f.write(content)
                self.file_path = file_path
                self.root.title(f"✨ {os.path.basename(file_path)} - Python图形记事本 ✨")
                messagebox.showinfo("保存成功", f"笔记已另存为：\n{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("保存失败", f"另存为失败：{str(e)}")

# ===================== 程序启动入口 =====================
if __name__ == "__main__":
    # 创建tkinter主窗口
    root = tk.Tk()
    # 实例化记事本程序
    app = GuiNotebook(root)
    # 运行主循环，显示窗口
    root.mainloop()