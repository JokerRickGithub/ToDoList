# -*- coding: utf-8 -*-
# Python 本地记事本/日记程序 - 带文件持久化
# 核心模块：os(文件操作)、datetime(日期命名)
import os
from datetime import datetime

# -------------------------- 功能函数封装 --------------------------
def show_all_notes():
    """查看当前目录下所有的笔记/日记文件"""
    print("\n===== 你的所有笔记/日记 =====")
    # 获取当前目录下所有文件
    all_files = os.listdir("./")
    # 筛选出 以 .txt 结尾的笔记文件
    note_files = [file for file in all_files if file.endswith(".txt")]
    
    if not note_files:
        print("暂无笔记/日记文件，快去新建一篇吧！")
        return []
    # 遍历展示所有笔记文件
    for index, file_name in enumerate(note_files, start=1):
        print(f"{index}. {file_name}")
    return note_files

def create_new_note():
    """新建笔记/日记 - 自动按日期命名，支持多行输入"""
    print("\n===== 新建笔记/日记 =====")
    # 1. 获取当前系统日期，自动生成文件名【核心：datetime的日期格式化】
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{current_date}_我的日记.txt"
    # 解决同一天多篇日记的命名问题：自动加序号 2026-01-17_我的日记_1.txt
    num = 1
    while os.path.exists(file_name):
        file_name = f"{current_date}_我的日记_{num}.txt"
        num += 1

    # 2. 接收多行输入，编辑笔记内容【核心：多行文本输入】
    print("请输入你的笔记内容（输入【end】并回车，结束编辑并保存）：")
    note_content = []
    while True:
        line = input()
        if line.strip() == "end":
            break
        note_content.append(line)
    # 把多行内容拼接成完整文本，换行符保留
    final_content = "\n".join(note_content)

    # 3. 保存笔记到文件【核心：文件写入 持久化存储】
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"✅ 笔记保存成功！文件名：{file_name}")
        print(f"✅ 文件保存在：{os.path.abspath(file_name)}")
    except Exception as e:
        print(f"❌ 笔记保存失败：{str(e)}")

def open_and_edit_note():
    """打开已有笔记，查看内容 + 支持二次编辑保存"""
    note_files = show_all_notes()
    if not note_files:
        return
    
    # 选择要打开的笔记序号
    try:
        choice = int(input("\n请输入要打开的笔记序号："))
        if choice < 1 or choice > len(note_files):
            print("❌ 输入的序号无效！")
            return
    except ValueError:
        print("❌ 请输入正确的数字序号！")
        return
    
    # 获取选中的文件名
    selected_file = note_files[choice-1]
    file_path = os.path.join("./", selected_file)

    # 读取笔记内容【核心：文件读取】
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"\n===== 打开笔记：{selected_file} =====")
        print(content)
        print("-" * 50)
    except Exception as e:
        print(f"❌ 读取笔记失败：{str(e)}")
        return

    # 二次编辑功能
    edit_choice = input("是否要编辑这篇笔记？(输入 y 编辑，其他键返回菜单)：").strip().lower()
    if edit_choice == "y":
        print(f"\n请编辑笔记内容（输入【end】并回车，结束编辑并覆盖保存）：")
        new_content = []
        while True:
            line = input()
            if line.strip() == "end":
                break
            new_content.append(line)
        final_new_content = "\n".join(new_content)
        
        # 覆盖保存
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_new_content)
            print(f"✅ 笔记编辑后保存成功！")
        except Exception as e:
            print(f"❌ 编辑保存失败：{str(e)}")

# -------------------------- 主程序菜单 --------------------------
def main():
    """主函数：程序入口，展示菜单"""
    print("=" * 50)
    print("🎉 Python 本地记事本/日记程序 (文件持久化版) 🎉")
    print("=" * 50)
    while True:
        print("\n【请选择操作】")
        print("1. 新建笔记/日记")
        print("2. 打开已有笔记/编辑笔记")
        print("3. 查看所有笔记/日记")
        print("4. 退出程序")
        choice = input("\n请输入你的选择（1/2/3/4）：").strip()
        
        if choice == "1":
            create_new_note()
        elif choice == "2":
            open_and_edit_note()
        elif choice == "3":
            show_all_notes()
        elif choice == "4":
            print("\n👋 感谢使用记事本程序，再见！")
            break
        else:
            print("❌ 输入错误，请选择 1/2/3/4 中的一个！")

# 程序启动
if __name__ == "__main__":
    main()
