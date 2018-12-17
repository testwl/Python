import os
import cv2
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from tkinter import StringVar
from tkinter import ttk
from PIL import Image, ImageTk
from base_method import Method
from tkinter import *

class Application(object):

    def __init__(self):
        self.root = tk.Tk()
        self.func =Method()
    

    def Run(self):
        self.root.mainloop()

    # 设置tab
    def setupUI(self):
        self.root.title('Android测试辅助工具')
        # self.root.geometry("600x700")
        tab_control = ttk.Notebook(self.root)
        
        frame_bar_qr = ttk.Frame(tab_control)
        tab_control.add(frame_bar_qr, text='条码和二维码')
        
        frame_mobinfo = ttk.Frame(tab_control)
        tab_control.add(frame_mobinfo, text='手机信息')

        frame_capture = ttk.Frame(tab_control)
        tab_control.add(frame_capture, text='屏幕截图')

        frame_record = ttk.Frame(tab_control)
        tab_control.add(frame_record, text='屏幕录制')

        frame_apk = ttk.Frame(tab_control)
        tab_control.add(frame_apk, text='apk安装包')

        frame_logcat = ttk.Frame(tab_control)
        tab_control.add(frame_logcat, text='logcat日志抓取与分析')

        tab_control.pack(expand=1, fill=tk.BOTH)
        return frame_bar_qr, frame_mobinfo, frame_capture, frame_record, frame_apk, frame_logcat

    # 条码和二维码tab
    def get_code(self, frame_bar_qr):
        # label
        label1 = ttk.Label(frame_bar_qr, text='条码：')
        label1.grid(row=0, column=0, ipady=2, sticky = 'E')
        # 条码输入框entry
        entry = ttk.Entry(frame_bar_qr, width=35)
        entry.grid(row=0, column=1)
        entry.focus()
        # 图片显示label
        label_bar_qr = ttk.Label(frame_bar_qr)
        label_bar_qr.grid(row=3, columnspan=4)
        # code =  entry.get()为什么不能放在这里？？？
        def barcode_exe():
            code = entry.get()
            if len(code)>0:
                self.func.barcode(code)
                self.func.show_image(label_bar_qr, 'barcode.png')
            else:
                label_bar_qr.config(image = '')
                tkinter.messagebox.showinfo('提示', '请输入条码')
        # 生成条形码button
        button1 = ttk.Button(frame_bar_qr, text='生成条形码', command=barcode_exe)
        button1.grid(row=1, column=0, sticky = 'W') 
        def qcode_exe():
            code = entry.get()
            if len(code)>0:
                self.func.qcode(code)
                self.func.show_image(label_bar_qr, 'qrcode.png')
            else:
                label_bar_qr.config(image = '')
                tkinter.messagebox.showinfo('提示', '请输入条码')
        # 生成二维码button
        button2 = ttk.Button(frame_bar_qr, text='生成二维码', command=qcode_exe)
        button2.grid(row=1, column=1, sticky = 'W')
        # 清空button
        button3 = ttk.Button(frame_bar_qr, text='清空', command=lambda:entry.delete(0, tk.END))
        button3.grid(row=0, column=3, sticky = 'W')

    # 截屏tab
    def get_capture(self, frame_capture):
        # 显示图片的label
        label_capture = ttk.Label(frame_capture)
        def capture_exe():
            self.func.capture()
            if os.path.exists('./screen.png'):
                self.func.show_image(label_capture, 'screen.png', x=4)
            else:
                label_capture.config(image='')
                tkinter.messagebox.showinfo('提示', '截屏失败')
        # 截屏button
        button4 = ttk.Button(frame_capture, text='截屏', command=capture_exe)
        button4.pack()
        label_capture.pack()

    # 录屏tab
    def get_video(self, frame_record):
        def video_exe():
            self.func.record()
            if os.path.exists('./record.mp4'):
                self.func.show_video()
            else:
                tkinter.messagebox.showinfo('提示', '录屏失败')
        # 录屏button
        button5 = ttk.Button(frame_record, text='录屏', command=video_exe)
        button5.pack()
        
    # 手机信息tab
    def get_mobinfo(self, frame_mobinfo):
        label_info = ttk.Label(frame_mobinfo)
        button6 = ttk.Button(frame_mobinfo, text='Android版本', command=lambda:self.func.info(label_info, 'adb shell getprop ro.build.version.release'))
        button6.grid(row=0, column=0)
        button7 = ttk.Button(frame_mobinfo, text='屏幕分辨率', command=lambda:self.func.info(label_info, 'adb shell wm size'))
        button7.grid(row=0, column=1)
        button8 = ttk.Button(frame_mobinfo, text='设备号', command=lambda:self.func.info(label_info, 'adb devices'))
        button8.grid(row=0,column=2)
        button9 = ttk.Button(frame_mobinfo, text='设备型号', command=lambda:self.func.info(label_info, 'adb shell getprop ro.product.model'))
        button9.grid(row=0,column=3)
        button10 = ttk.Button(frame_mobinfo, text='用户安装app', command=lambda:self.func.info(label_info, 'adb shell pm list packages -3'))
        button10.grid(row=0,column=4)
        label_info.grid(row=1,columnspan=6)

    def get_apk(self, frame_apk):

        def selectPath():
            file = filedialog.askopenfilename(filetypes=[("apk格式", ".apk")])
            path.set(file)

        label1=ttk.Label(frame_apk, text='安装包路径：')
        label1.grid(row=0, column=0, sticky='W')
        path = StringVar()
        apkfile = ttk.Entry(frame_apk, textvariable = path, width=35)
        apkfile.grid(row=0,column=1, sticky='W')
        button13 = ttk.Button(frame_apk, text = '选择文件', command = selectPath)
        button13.grid(row=0, column=2, sticky='W')
        label_apkinfo = ttk.Label(frame_apk)
        button11 = ttk.Button(frame_apk, text='apk反编译', command=lambda:self.func.apk_apktool(label_apkinfo, apkfile.get()))
        button11.grid(row=1, column=0)
        button12 = ttk.Button(frame_apk, text='安装apk', command=lambda:self.func.inapk(label_apkinfo, apkfile.get()))
        button12.grid(row=1, column=1)
        button14 = ttk.Button(frame_apk, text='aapt获取包信息', command=lambda:self.func.apk_aapt(label_apkinfo, apkfile.get()))
        button14.grid(row=1, column=2)
        label_apkinfo.grid(row=2, columnspan=6)

    def logcat(self, frame_logcat):
        def get_logcat():
            content = self.func.get_log()
            # if content.poll:
            
                # with open('.//log.log', encoding = 'utf8') as f:
                    # for each_line in f:
                        # text.delete('1.0', 'end')
                
        
        def show_logcat():
            content = self.func.close_log()
            if content.poll:
            # for each_line in iter(content.stdout.readline, 'utf8'):
                for each_line in content.stdout.readlines():
                    each_line = each_line.decode('utf8')
                    text.insert(INSERT,each_line)
            # with open('.//log.log', encoding = 'utf8') as f:
            #     for each_line in f:
            #         # text.delete('1.0', 'end')
            #         text.insert(INSERT,each_line)
        def search_packg():
            packg = entry.get()
            pids = self.func.get_pid('.//log.log', packg)
            print(pids)
            results = self.func.log_pid('.//log.log', pids)
            for line in results:
                # text.delete('1.0', 'end')
                text.insert(INSERT,line)

        scroll = tkinter.Scrollbar(frame_logcat)
        text = tkinter.Text(frame_logcat, borderwidth=0)
       
        button1 = ttk.Button(frame_logcat, text = '抓取日志', command =get_logcat)
        button2 = ttk.Button(frame_logcat, text='结束抓取', command = show_logcat)
        entry = ttk.Entry(frame_logcat)
        button3 =ttk.Button(frame_logcat, text = '搜索指定包名日志', command = search_packg)
        
        
        button1.pack()
        button2.pack()
        entry.pack()
        button3.pack()
        scroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)
        text.pack(side = tkinter.LEFT, fill = tkinter.Y)
        scroll.config(command = text.yview)
        text.config(yscrollcommand = scroll.set)


app = Application()
frame_bar_qr ,frame_mobinfo, frame_capture, frame_record ,frame_apk ,frame_logcat = app.setupUI()
app.get_code(frame_bar_qr)
app.get_capture(frame_capture)
app.get_video(frame_record)
app.get_mobinfo(frame_mobinfo)
app.get_apk(frame_apk)
app.logcat(frame_logcat)
app.Run()
