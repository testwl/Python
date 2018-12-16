from tkinter import *
filename=r"test.txt"
def savetxt(filename):
    f=open(filename,'w')
    txt=en.get()
    f.write(txt)
    f.close()
root=Tk()
en=Entry(root)
en.pack()
bu=Button(root,text="save txt",command=lambda:savetxt(filename))
bu.pack()
root.mainloop()