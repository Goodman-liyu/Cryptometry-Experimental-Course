from main import  *
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import time
import os
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("RSA文件加解密System")
        self.master.geometry("500x350")
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TFrame", background="#f0f0f0")
        # 使用PIL打开图片并转换为PhotoImage
        image = Image.open(r"p1.png")  # 替换为你的图片路径
        self.background_image = ImageTk.PhotoImage(image)

        # 创建Label并设置背景图片
        background_label = Label(master, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)


        self.key_size_label = ttk.Label(master, text="", style="TLabel")
        self.key_size_label.grid(row=0, column=1, padx=250, pady=50, sticky=tk.W)
        '''
        # 生成密钥按钮
        self.open_next_window_button = tk.Button(master, text="生成密钥", width = 10, height = 2,command=self.open_next_window,
                    fg ="#{:02x}{:02x}{:02x}".format(42, 87, 228), font = ("Helvetica", 12,"bold"))
        self.open_next_window_button.grid(row=1, column=2,ipadx=5,ipady=5,padx=0,pady=0)
        '''
        # RSA加密按钮

        self.open_next_window_button1 = tk.Button(master, text="RSA加密", width = 10, height = 1,command=self.open_next_window1,
                    bg="gray", fg ="black", font = ("Helvetica", 12,"bold"),bd=1,highlightthickness=1)
        self.open_next_window_button1.grid(row=1, column=1,padx=0,pady=8, ipadx=5,ipady=5)

        # RSA解密按钮
        self.open_next_window_button2 = tk.Button(master, text="RSA解密", width = 10, height = 1,command=self.open_next_window2,
                    bg="gray", fg ="black", font = ("Helvetica", 12,"bold"))
        self.open_next_window_button2.grid(row=2, column=1,padx=0,pady=8, ipadx=5,ipady=5)

        # 退出按钮
        self.exit_button = tk.Button(master, text="退出", width = 10, height = 1,command=self.on_exit,
                    bg="gray", fg ="black", font = ("Helvetica", 12,"bold"))
        self.exit_button.grid(row=3, column=1, padx=0,pady=8,ipadx=5,ipady=5)


    def on_exit(self):
        root.destroy()

    '''
    def open_next_window(self):
        self.master.iconify()  # 隐藏主窗口
        next_window = tk.Toplevel(self.master)  # 创建下一个窗口
        Next_generate(next_window,"密钥生成")
    '''

    def open_next_window1(self):
        self.master.iconify()  # 隐藏主窗口
        next_window = tk.Toplevel(self.master)  # 创建下一个窗口
        Next_encryption(next_window,"RSA加密")

    def open_next_window2(self):
        self.master.iconify()  # 隐藏主窗口
        next_window = tk.Toplevel(self.master)  # 创建下一个窗口
        Next_decryption(next_window, "RSA解密")
'''
class Next_generate:
    def __init__(self, master,name):
        self.master = master
        self.master.title(name)
        self.master.geometry("900x470")

        self.frame = ttk.Frame(self.master, style="TFrame")
        self.frame.grid(row=0, column=0, padx=5, pady=20)

        self.key_size_label = ttk.Label(self.frame, text="选择密钥位数:", style="TLabel")
        self.key_size_label.grid(row=1, column=1)

        self.key_size_combobox = ttk.Combobox(self.frame, values=[64, 128, 256, 512, 1024], state="readonly", font=("Helvetica", 12))
        self.key_size_combobox.set(256)  # 默认选择256位
        self.key_size_combobox.grid(row=1, column=2)
        ############
        self.b1 = ttk.Button(self.frame, text="生成质数", command=self.generate_PQ, style="TButton")
        self.b1.grid(row=2, column=0)

        self.b2 = ttk.Button(self.frame, text="计算n与Euler", command=self.n_and_Euler, style="TButton")
        self.b2.grid(row=2, column=1)

        self.b3 = ttk.Button(self.frame, text="产生密钥", command=self.eandd, style="TButton")
        self.b3.grid(row=2, column=2)

        self.back_to_main_button = ttk.Button(master, text="返回主窗口", command=self.back_to_main, style="TButton")
        self.back_to_main_button.grid(row=10, column=0, padx=0, pady=0)

        self.save = ttk.Button(master, text="保存密钥", command=self.savetofile, style="TButton")
        self.save.grid(row=9, column=0, padx=0, pady=0)

        ###############
        self.t1 = tk.Text(self.frame, height=9, width=120, state='normal', font = ("Helvetica", 10))
        self.t1.grid(row=3, column=0, columnspan=3, pady=10)
        self.t1.config(state='normal')
        self.t1.insert(tk.END, "RSA相关信息：")
        self.t1.config(state='disabled')


        # RSA相关信息窗口
        self.RSA_text = tk.Text(self.frame, height=6, width=120, state='normal',font = ("Helvetica", 10))
        self.RSA_text.grid(row=4, column=0, columnspan=3, pady=10)
        self.RSA_text.config(state='normal')
        self.RSA_text.insert(tk.END, "公私钥对：")
        self.RSA_text.config(state='disabled')

    def back_to_main(self):
        self.master.destroy()  # 关闭当前窗口
        root.deiconify()  # 显示主窗口

    def generate_PQ(self):
        size = int(self.key_size_combobox.get())
        self.P,self.Q=generate_PQ(size)

        self.t1.config(state='normal')  # 启用文本框
        self.t1.insert(tk.END, f"\nP={self.P}\nQ={self.Q}")
        self.t1.config(state='disabled')  # 禁用文本框

    def n_and_Euler(self):
        self.n = caculate_n(self.P, self.Q)
        self.Euler= Euler(self.P, self.Q)

        self.t1.config(state='normal')  # 启用文本框
        self.t1.insert(tk.END, f"\n{split}\nn={self.n} \nEuler(n)={self.Euler}")
        self.t1.config(state='disabled')  # 禁用文本框

    def eandd(self):
        self.e=find_e(self.Euler)
        self.d=get_d(self.e,self.Euler)
        self.RSA_text.config(state='normal')  # 启用文本框
        self.RSA_text.insert(tk.END, f"\n 公钥e= {self.e} \n 私钥d= {self.d}")
        self.RSA_text.config(state='disabled')  # 禁用文本框

    def savetofile(self):
        user_input = simpledialog.askstring("保存密钥", "请输入保存地址:")
        if user_input is None:
            messagebox.showinfo("错误", "请输入正确的保存地址")
            raise ValueError("地址错误")
        else:
            with open(user_input, 'w',encoding='utf-8') as file:
                file.write(f"公钥e={self.e} \n私钥d={self.d}\nn={self.n}")
                messagebox.showinfo("保存密钥", "保存成功")
'''
class Next_encryption:
    def __init__(self, master,name):
        self.master = master
        self.master.title(name)
        self.master.geometry("750x520")

        self.frame = ttk.Frame(self.master, style="TFrame")
        self.frame.grid(row=0, column=0, padx=20, pady=20)
    # 文件路径输入框+文字
        self.browse_button = ttk.Button(self.frame, text="待加密文件", command=self.BrowseShow_file, style="TButton")
        self.browse_button.grid(row=0, column=0)#, padx=10, pady=10)

        self.file_path_entry = ttk.Entry(self.frame, width=50, state='disabled', font=("Helvetica", 12))
        self.file_path_entry.grid(row=0, column=1)
    # 密钥长度选择
        self.key_size_label = ttk.Label(self.frame, text=" "*85+"选择密钥位数:",style="TLabel")
        self.key_size_label.grid(row=1, column=1)

        self.key_size_combobox = ttk.Combobox(self.frame, width=10,values=[64, 128, 256, 512, 1024], state="readonly", font=("Helvetica", 12))
        self.key_size_combobox.set(64)  # 默认选择256位
        self.key_size_combobox.grid(row=1, column=2)
    # 浏览文件按钮
        #self.b4 = ttk.Button(self.frame, text="显示原始文本", command=self.show, style="TButton")
        #self.b4.grid(row=2, column=0)

        self.b5 = ttk.Button(self.frame, text="加密", command=self.encrypt, style="TButton")
        self.b5.grid(row=1, column=0)

        self.back_to_main_button = ttk.Button(self.frame, text="返回主窗口", command=self.back_to_main,style="TButton")
        self.back_to_main_button.grid(row=8, column=2)

        self.b6 = ttk.Button(self.frame, text="保存密文", command=self.save_c, style="TButton")
        self.b6.grid(row=8, column=0)
    #############
        # 原文本信息
        self.t1 = tk.Text(self.frame, height=12, width=100, state='disabled')
        self.t1.grid(row=5, column=0, columnspan=3, pady=10)
        self.t1.config(state='normal')
        self.t1.insert(tk.END, "文本信息:\n")
        self.t1.config(state='disabled')
        #密文信息
        self.t2 = tk.Text(self.frame, height=12, width=100, state='disabled')
        self.t2.grid(row=6, column=0, columnspan=3, pady=10)
        self.t2.config(state='normal')
        self.t2.insert(tk.END, "密文信息:\n")
        self.t2.config(state='disabled')



    def back_to_main(self):
        self.master.destroy()  # 关闭当前窗口
        root.deiconify()  # 显示主窗口

    def BrowseShow_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_path_entry.config(state='normal')  # 启用输入框
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, self.file_path)
            self.file_path_entry.config(state='disabled')  # 禁用输入框
            self.file_size = os.path.getsize(self.file_path)
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content_str = file.read()
            self.t1.config(state='normal')  # 启用文本框
            self.t1.insert(tk.END, content_str)
            self.t1.config(state='disabled')  # 禁用文本框

    def encrypt(self):
        time1 = time.time()
        self.size = int(self.key_size_combobox.get())
        #print(self.size)
        self.P,self.Q = generate_PQ(self.size)
        self.n = caculate_n(self.P,self.Q)
        self.m = Euler(self.P,self.Q)
        self.e = find_e(self.m)
        self.d = get_d(self.e,self.m)
        time2 = time.time()
        self.Tgenerate = time2 - time1
        self.Tgenerate_label = ttk.Label(self.frame, text="密钥生成时间:{:.5f}".format(self.Tgenerate), style="TLabel")
        self.Tgenerate_label.grid(row=1, column=1)
        #print("P:{0},Q:{1},n:{2},m:{3},e:{4},d:{5}".format(P,Q,n,m,e,d))

        #e = simpledialog.askinteger("输入", "公钥e:", parent=self.master)
        #n = simpledialog.askinteger("输入", "模n:", parent=self.master)
        self.save_key()
        if self.e is not None and self.n is not None:
            time1 = time.time()
            self.encode_str = encode(self.file_path, self.e, self.n)
            self.Tencode = time.time() - time1
            self.Tencode_label = ttk.Label(self.frame, text="加密时间:{:.5f}  加密速度:{:.5f}byte/s".format(self.Tencode,(self.file_size/self.Tencode)), style="TLabel")
            self.Tencode_label.grid(row=8, column=1)
            messagebox.showinfo("RSA", "加密成功")
            self.t2.config(state='normal')  # 启用文本框
            self.t2.insert(tk.END, self.encode_str)
            self.t2.config(state='disabled')  # 禁用文本框
        else:
            # 用户点击取消按钮或未输入有效的值
            raise ValueError("无效的输入")

    def save_c(self):
        user_input = simpledialog.askstring("保存密文", "请输入保存地址:")
        if user_input is None:
            messagebox.showinfo("错误", "请输入正确的保存地址")
            raise ValueError("地址错误")
        else:
            with open(user_input, 'w', encoding='utf-8') as file:
                file.write(self.encode_str)
                messagebox.showinfo("保存密文", "保存成功")

    def save_key(self):
        user_input = simpledialog.askstring("hh", "请输入密钥保存地址:")
        if user_input is None:
            messagebox.showinfo("错误", "请输入正确的保存地址")
            raise ValueError("地址错误")
        else:
            with open(user_input, 'w',encoding='utf-8') as file:
                file.write(f"Public_e={self.e}\nPrivate_d={self.d}\nn={self.n}")
                messagebox.showinfo("保存密钥", "保存成功")

class Next_decryption:
    def __init__(self, master, name):
        self.master = master
        self.master.title(name)
        self.master.geometry("750x520")

        self.frame = ttk.Frame(self.master, style="TFrame")
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        # 文件路径输入框
        self.file_path_entry = ttk.Entry(self.frame, width=50, state='disabled', font=("Helvetica", 12))
        self.file_path_entry.grid(row=0, column=1)#, padx=10, pady=10, ipady=3)
        # 浏览文件按钮
        self.browse_button = ttk.Button(self.frame, text="待解密文件", command=self.BrowseShow_file,style="TButton")
        self.browse_button.grid(row=0, column=0)#, padx=10, pady=10)

        #self.b4 = ttk.Button(self.frame, text="显示原始密文", command=self.show, style="TButton")
        #self.b4.grid(row=2, column=0)
        self.b5 = ttk.Button(self.frame, text="解密", command=self.decrypt, style="TButton")
        self.b5.grid(row=2, column=2)

        self.b5 = ttk.Button(self.frame, text="解密密钥", command=self.read_keys_from_file, style="TButton")
        self.b5.grid(row=2, column=0)
        #解密文件路径输入
        self.key_file_entry = ttk.Entry(self.frame, width=50, state='disabled', font=("Helvetica", 12))
        self.key_file_entry.grid(row=2, column=1)

        self.back_to_main_button = ttk.Button(self.frame, text="返回主窗口", command=self.back_to_main,style="TButton")
        self.back_to_main_button.grid(row=8, column=2, padx=0, pady=0)

        self.b6 = ttk.Button(self.frame, text="保存明文", command=self.save_m, style="TButton")
        self.b6.grid(row=8, column=0, padx=0, pady=0)
        #############密文显示框
        self.t1 = tk.Text(self.frame, height=12, width=100, state='disabled')
        self.t1.grid(row=5, column=0, columnspan=3, pady=10)
        self.t1.config(state='normal')
        self.t1.insert(tk.END, "密文信息:\n")
        self.t1.config(state='disabled')
        #明文显示框
        self.t2 = tk.Text(self.frame, height=12, width=100, state='disabled')
        self.t2.grid(row=6, column=0, columnspan=3, pady=10)
        self.t2.config(state='normal')
        self.t2.insert(tk.END,"明文信息:\n")
        self.t2.config(state='disabled')

    def back_to_main(self):
        self.master.destroy()  # 关闭当前窗口
        root.deiconify()  # 显示主窗口

    def BrowseShow_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_path_entry.config(state='normal')  # 启用输入框
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, self.file_path)
            self.file_path_entry.config(state='disabled')  # 禁用输入框
            self.efile_size = os.path.getsize(self.file_path)
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content_str = file.read()
            self.t1.config(state='normal')  # 启用文本框
            self.t1.insert(tk.END, content_str)
            self.t1.config(state='disabled')  # 禁用文本框

    def decrypt(self):
        if self.d is not None and self.n is not None:
            time1 = time.time()
            self.decode_str = decode(self.file_path, self.d, self.n)
            self.Tdecode = time.time() - time1
            self.Tdecode_label = ttk.Label(self.frame, text="解密时间:{:.5f}  解密速度:{:.5f}byte/s".format(self.Tdecode,(self.efile_size/self.Tdecode)), style="TLabel")
            self.Tdecode_label.grid(row=8, column=1)
            messagebox.showinfo("RSA", "解密成功")
            self.t2.config(state='normal')  # 启用文本框
            self.t2.insert(tk.END, self.decode_str)
            self.t2.config(state='disabled')  # 禁用文本框
        else:
            raise ValueError("无效的输入")

    def save_m(self):
        user_input = simpledialog.askstring("保存明文", "请输入保存地址:")
        if user_input is None:
            messagebox.showinfo("错误", "请输入正确的保存地址")
            raise ValueError("地址错误")
        else:
            with open(user_input, 'w', encoding='utf-8') as file:
                file.write(self.decode_str)
                messagebox.showinfo("保存明文", "保存成功")

    def read_keys_from_file(self):
        self.key_file = filedialog.askopenfilename()
        if self.key_file:
            self.key_file_entry.config(state='normal')  # 启用输入框
            self.key_file_entry.delete(0, tk.END)
            self.key_file_entry.insert(0, self.key_file)
            self.key_file_entry.config(state='disabled')  # 禁用输入框
        with open(self.key_file, 'r') as file:
            for line in file:
                if line.startswith('Public_e='):
                    self.e = int(line.split('=')[1])
                elif line.startswith('Private_d='):
                    self.d = int(line.split('=')[1])
                elif line.startswith('n='):
                    self.n = int(line.split('=')[1])

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()



