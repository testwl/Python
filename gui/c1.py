from tkinter import *

root=Tk()
root.title('天气预报数据处理窗口')#窗口名字
root.geometry('800x450')#设置主窗口大小

def openfile():
    filename = str(e1.get())
    try:
        with open(filename) as f:
            for each_line in f:
                text.insert(INSERT,each_line)                
    except OSError as reason:
        print('文件不存在！\n请重新输入文件名'+str(reason))
        
topFrame = Frame(root,bd=1, relief=SUNKEN)
topFrame.pack(fill=BOTH)

bottomFrame = Frame(root,bd=1, relief=SUNKEN)
bottomFrame.pack(fill=BOTH)

label=Label(topFrame,text="文件名：")
label.grid(row=0,column=0, sticky=W)

v1=StringVar()
e1=Entry(topFrame,textvariable=v1)
e1.grid(row=0,column=1,sticky=W)

b1=Button(topFrame,text="确认",command=openfile)
b1.grid(row=0,column=2,padx=5,sticky=W)

text = Text(bottomFrame, height=600)
text.pack(fill=BOTH)


mainloop()
