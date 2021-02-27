import tkinter as tk
from tkinter import messagebox
import os
import sys
import pandas as pd
from PIL import Image, ImageTk



class basedesk():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('选择页面')
        global w, h
        w, h = 1000, 800
        self.root.geometry('{}x{}'.format(w, h))
        initface(self.root)


class initface():
    def __init__(self, master):
        self.master = master
        self.master.config()
        # 基准界面initface
        global w, h, stunum, stuname, stugrade, tmpgrade, filepath, \
                itStu, itPic
        filepath = os.getcwd()
        itStu = iter(os.listdir(filepath + '/Data'))
        try:
            global nowstu, nowpic
            nowstu = next(itStu)

        except StopIteration:
            btn = tk.Button(root, command=messagebox.showinfo('警告', 'Data中没有作业内容'))
            btn.pack()
            sys.exit()
        try:
            itPic = iter(os.listdir(filepath + '/Data' + '/' + nowstu))
            nowpic = next(itPic)
        except StopIteration:
            btn = tk.Button(root, command=messagebox.showinfo('警告', nowstu + '没有作业内容'))
            btn.pack()
            sys.exit()
        stunum = []
        stuname = []
        stugrade = []
        tmpgrade = []
        num, name = nowstu.split('-')
        stunum.append(num)
        stuname.append(name)
        self.initface = tk.Frame(self.master, height=h, width=w)
        self.initface.pack_propagate(0)
        self.initface.pack()
        frm1 = tk.Frame(self.initface, height=h, width=w/2)
        frm1.pack_propagate(0)
        frm1.pack(side=tk.LEFT)
        frm2 = tk.Frame(self.initface, height=h, width=w/2)
        frm2.pack_propagate(0)
        frm2.pack(side=tk.RIGHT)
        quote = '  说明：每位学生建立一个文件夹放在Data文件夹中，命名方式为\"学号-姓名\",不包括引号,尽量保证学号位数一致。学生文件夹中包含' \
                '作业的图片，按1,2,3......的顺序命名，如\'1.jpg\',最后成绩会取每一张图片的平均值。程序退出后就数据就会存成Data.xlsx。' \
                '注：程序不能中途退出或返回，否则需要重新开始。'
        lab1 = tk.Label(frm1, text=quote, font=('宋体', 17, 'bold'), wraplength=300, justify=tk.LEFT)
        lab1.pack(pady=h/5)
        lab2 = tk.Label(frm2, text='评分方式', font=('Times', 15, 'bold'))
        lab2.pack(pady=h/5)
        self.v = tk.IntVar()
        self.v.set(1)
        r1 = tk.Radiobutton(frm2, text='A,B,C,D', font=('', 10, ''), variable=self.v, value=1)
        r1.pack()
        r2 = tk.Radiobutton(frm2, text='0-100分', font=('', 10, ''), variable=self.v, value=2)
        r2.pack()
        btn = tk.Button(frm2, text='确定', command=self.nextStep)
        btn.pack(pady=h/10)

    def nextStep(self, ):
        self.initface.destroy()
        mainscreen(self.master, self.v.get())


class mainscreen():
    def __init__(self, master, choice):
        self.master = master
        self.master.title('主页面')
        global w, h, filepath, it, nowstu, nowpic
        self.mainscreen = tk.Frame(self.master, height=h, width=w)
        self.mainscreen.pack_propagate(0)
        self.mainscreen.pack()
        DealPic(self.mainscreen, choice)
        btn_back = tk.Button(self.mainscreen, text='返回', command=self.back)
        btn_back.pack(side=tk.BOTTOM)

    def back(self):
        self.mainscreen.destroy()
        initface(self.master)

class DealPic():
    def __init__(self, master, choice):
        global w, h, nowpic, nowstu, tmpgrade, filepath
        self.master = master
        self.ch = choice
        num, name = nowstu.split('-')
        self.frm = tk.Frame(self.master, height=h / 3 * 2, width=w / 3)
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.RIGHT, pady=(0, h / 3))
        lab = tk.Label(self.frm, text='为' + name + '打分:')
        lab.pack(pady=(h / 5, h / 100))
        self.cv = tk.Canvas(self.master, height=h/1.2, width=w/3*2)
        self.cv.pack(anchor=tk.NW)
        # fil = Image.open(filepath+'/Data/'+nowstu+'/'+nowpic)
        # print(fil)
        global img, im, im_resized
        im = Image.open(filepath+'/Data/'+nowstu+'/'+nowpic)
        imw, imh = im.size
        im_resized = im.resize((int(w/3*2), int(h/1.2)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im_resized)
        self.cv.create_image(20, 20, anchor=tk.NW, image=img)
        if choice == 1:
            self.v = tk.IntVar()
            self.v.set(1)
            r1 = tk.Radiobutton(self.frm, text='A', font=('', 10, ''), variable=self.v, value=1)
            r1.pack()
            r2 = tk.Radiobutton(self.frm, text='B', font=('', 10, ''), variable=self.v, value=2)
            r2.pack()
            r3 = tk.Radiobutton(self.frm, text='C', font=('', 10, ''), variable=self.v, value=3)
            r3.pack()
            r4 = tk.Radiobutton(self.frm, text='D', font=('', 10, ''), variable=self.v, value=4)
            r4.pack()
        else:
            self.text = tk.Entry(self.frm, width=10)
            self.text.pack(pady=(0, 10))
        btn = tk.Button(self.frm, text='确认', command=self.confirm)
        btn.pack()

    def confirm(self):
        global nowstu, nowpic, itPic, itStu, filepath, stunum, stuname, stugrade, root
        if self.ch == 1:
            tmpgrade.append(self.v.get())
        else:
            print(int(self.text.get()))
            tmpgrade.append(int(self.text.get()))
        self.frm.destroy()
        self.cv.destroy()
        try:
            nowpic = next(itPic)
            DealPic(self.master, self.ch)
        except StopIteration:
            try:
                if self.ch == 1:
                    stugrade.append(chr(sum(tmpgrade)//len(tmpgrade)+ord('A')-1))
                else:
                    stugrade.append(sum(tmpgrade)//len(tmpgrade))
                tmpgrade.clear()
                nowstu = next(itStu)
                num, name = nowstu.split('-')
                stunum.append(num)
                stuname.append(name)
            except StopIteration:
                self.save()
                self.back_main()
            try:
                itPic = iter(os.listdir(filepath + '/Data/' + nowstu))
                nowpic = next(itPic)
                DealPic(self.master, self.ch)
            except StopIteration:
                btn = tk.Button(root, command=messagebox.showinfo('警告', nowstu+'没有作业内容'))
                btn.pack()
                sys.exit()


    def save(self):
        global stunum, stuname, stugrade
        print(stunum)
        print(stuname)
        print(stugrade)
        df = pd.DataFrame(data={'学号': stunum,
                                '姓名': stuname,
                                '成绩': stugrade})
        df.to_excel('Data.xls', index=False)
        messagebox.showinfo('提示', '报告已经成功生成！')

    def back_main(self):
        self.master.destroy()
        global root
        initface(root)

if __name__ == '__main__':
    root = tk.Tk()
    w, h = root.maxsize()
    img = None
    im = None
    im_resized = None
    stunum = None
    stugrade = None
    stuname = None
    nowstu = None
    nowpic = None
    itStu = None
    itPic = None
    filepath = None
    tmpgrade = None
    basedesk(root)
    root.mainloop()