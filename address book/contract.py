from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
import csv,re
from tkinter import ttk
# import database,datetime


# 数据库开关
dbopen = False

class Table:
    def __init__(self,root):
        col = ('学生编号', '学生姓名', '学生性别', '学生年龄', '出生日期',
               '手机号码', '电子邮箱', '家庭住址', '专　　业')
        self.scrollbar = Scrollbar(root)
        self.tree = Treeview(root, height=18, yscrollcommand=self.scrollbar.set)
        self.tree["columns"] = col
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        # 设置每列宽度和对齐方式
        for co in col:
            self.tree.column(co, width=120, anchor='center')
        self.tree.column('#0', width=0)
        # self.tree.pack(side='top')
        # 设置每列表头标题文本
        for c in col:
            self.tree.heading(c, text=c)

    def pack(self):
        self.tree.pack(anchor=N, side=LEFT)
        self.scrollbar.pack(anchor=N, side=LEFT,fill=Y,expand=YES)

    def unpack(self):
        self.tree.forget()
        self.scrollbar.forget()

    def getselect(self):
        return self.tree.selection()

    def isempty(self):
        if self.tree.get_children():
            return False
        else:
            return True

    def insert(self,row):
        self.tree.insert("",1,values=row)

    def delete(self):
        deltmp = self.tree.item(self.getselect())['values'][0]
        with open('userdata/data.csv', 'r') as rfile, open('userdata/del.csv', 'w', newline="") as tmpfile:
            reader = csv.reader(rfile)
            writer = csv.writer(tmpfile)
            for row in reader:
                # 数据库开关
                if dbopen:
                    try:
                        if row[0] != '学生编号' and int(row[0]) == deltmp:
                            database.delete(row[0])
                    except:
                        pass
                if  row[0] != '学生编号' and int(row[0]) == deltmp:
                    continue
                else:
                    writer.writerow(row)
        with open('userdata/data.csv', 'w') as rfile, open('userdata/del.csv', 'r') as tmpfile:
            rfile.write(tmpfile.read())
        self.tree.delete(self.getselect())

class Listtree:
    def __init__(self):
        self.tree = Treeview(root)
        self.treeroot = self.tree.insert("", 0, text='全部')
        self.tree.item(self.treeroot, tags='全部')
        self.tree.tag_bind("全部", "<Double-Button-1>", self.callback)
        self.subtitle = []   # 记录以存在目录
        self.cur = Table(root)
        self.tree.pack(side=LEFT,anchor=N)
        self.cur.pack()
        self.tree.selection_set(self.treeroot)

        # 判断数据库
        if dbopen:
            result = database.filltable('全部')
            # print(result)
            for row in result:
                self.insert(row[8])
                self.cur.insert(row)
        else:
            with open('userdata/data.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.insert(row[8])
                    if row[0] != '学生编号':
                        self.cur.insert(row)

    # 获取鼠标焦点
    def getselect(self):
        return self.tree.item(self.tree.selection())['text']

    def callback(self,event):
        index = self.tree.item(self.tree.focus())['text']
        self.cur.unpack()
        self.cur = Table(root)

        # 数据库对应函数
        if dbopen:
            result = database.filltable(index)
            for row in result:
                self.cur.insert(row)
        else:
            with open('userdata/data.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] != '学生编号' and row[8] == index:
                        self.cur.insert(row)
                    if index == '全部' and row[0] != '学生编号':
                        self.cur.insert(row)
        self.cur.pack()

    def insert(self,obj):
        if obj not in self.subtitle and obj != '专业':
            self.subtitle.append(obj)
            rot = self.tree.insert(self.treeroot, 0, text=obj)
            self.tree.item(rot, tags=obj)
            self.tree.tag_bind(obj, "<Double-Button-1>", self.callback)

    def delete(self):
        self.subtitle.remove(self.getselect())
        self.tree.delete(self.tree.selection())



class Inputwindow:
    def __init__(self,mode):
        self.top = Toplevel()
        self.top.title(mode)
        self.top.geometry("500x500+300+100")
        self.postdata = []   # 提交如文件夹的数组
        self.mode =mode
        f = ('楷体', 14, "normal")
        Label(self.top, text="学生信息", font=f \
              ).grid(row=0, column=0)
        Button(self.top, text='提交', font=f, width=6, bg='#ccccff' \
               , command=lambda: self.Adddata(self.top)).grid(row=4, column=7, sticky=E, padx=65)
        Button(self.top, text='关闭', font=f, width=6, bg='#ccccff', command \
            =self.top.destroy).grid(row=7, column=7, sticky=E, padx=65)
        index = ['学生编号','学生姓名','学生性别','学生年龄','出生日期', \
                     '手机号码','电子邮箱','家庭住址','专　　业']
        row = 3
        for ind in index:
            Label(self.top,text=ind, font=f1).grid(pady=15,padx=30, \
                                                 row=row,column=0,sticky=W)
            row += 1
        global inpbox
        inpbox = []
        self.v = IntVar()   # 存储性别
        self.v.set(0)
        num = 0
        for i in range(3,12):
            if i == 5:
                Radiobutton(self.top, text='男', variable=self.v, value=0 \
                            , font=f1).grid(row=i, column=1, columnspan=3)
                Radiobutton(self.top, text='女', variable=self.v, value=1 \
                            , font=f1).grid(row=i, column=4, columnspan=3)
            elif i == 7:
                self.age = []       # 存储日期信息
                for j, item in [(1, '年'), (3, '月'), (5, '日')]:
                    self.age.append(StringVar())
                    a = ttk.Combobox(self.top, width=4, textvariable=self.age[num], state='readonly')
                    a.grid(row=i, column=j)
                    if j == 1:
                        a['values'] = [y for y in range(1920, 2017)]
                    elif j == 3:
                        a['values'] = [m for m in range(1, 13)]
                    else:
                        a['values'] = [m for m in range(1, 32)]
                    a.current(1)
                    Label(self.top, text=item).grid(row=i, column=j + 1)
                    num += 1

            else:
                e = Entry(self.top, font=f1)
                e.grid(row=i, column=1, columnspan=6)
                inpbox.append(e)
        self.info = []  # 存储其余七个文本数据
        for i in range(7):
            self.info.append(StringVar())
            inpbox[i].config(textvariable=self.info[i])

    # 添加数据
    def Adddata(self,master):
    #try:
        postdata = self.getpostdata()
        if self.mode == 'Add':
            if postdata:
                postdata[0] = str(int(postdata[0]))
                # print(postdata)
                if dbopen:
                    try:
                        database.insert(postdata)
                    except:
                        pass
                flag = 1
                with open('userdata/data.csv', 'r+', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    # print(next(reader))
                    for row in reader:
                        if row[0] == '学生编号':
                            continue
                        if int(row[0]) == int(postdata[0]):
                            flag = 0
                            break
                    if flag:
                        leftlist.insert(postdata[8])
                        if leftlist.getselect() == postdata[8] or leftlist.getselect() == '全部':
                            leftlist.cur.insert(postdata)
                        w = csv.writer(csvfile)
                        w.writerow(postdata)
                        for i in range(7):
                            self.info[i].set('')
                        messagebox.showinfo('Reslut', '添加成功', parent=self.top)
                    else:
                        messagebox.showinfo('Error!', '编号重复啦！', parent=self.top)
            else:
                messagebox.showinfo('Error!', '输入不合法，请重试', parent=self.top)

        else:
            if postdata:
                if dbopen:
                    try:
                        database.edit(postdata)
                    except:
                        pass
                tmp = leftlist.cur.getselect()
                tmp = leftlist.cur.tree.item(tmp)['values'][0]
                if int(postdata[0]) == tmp:
                    leftlist.cur.tree.delete(leftlist.cur.getselect())
                    if leftlist.getselect() == postdata[8] or leftlist.getselect() == '全部':
                        leftlist.cur.insert(postdata)
                    leftlist.insert(postdata[8])
                    if leftlist.cur.isempty():
                        leftlist.delete()
                    # 跟新信息
                    with open('userdata/data.csv', 'r') as rfile, open('userdata/del.csv', 'w', newline="") as tmpfile:
                        reader = csv.reader(rfile)
                        writer = csv.writer(tmpfile)
                        for row in reader:
                            if row[0] != "学生编号" and int(postdata[0]) == int(row[0]):
                                writer.writerow(postdata)
                            else:
                                writer.writerow(row)
                    with open('userdata/data.csv', 'w') as rfile, open('userdata/del.csv', 'r') as tmpfile:
                        rfile.write(tmpfile.read())
                    messagebox.showinfo('Result', '修改成功！',parent=self.top)
                    self.top.destroy()
                else:
                    messagebox.showinfo('Error!', '不得修改编号哦！', parent=self.top)
            else:
                messagebox.showinfo('Error!', '输入不合法', parent=self.top)
    # except:
    #     print('错误啦')

    # 输入验证函数
    def checkinput(self):
        f = 1
        for i in range(7):
            if self.info[i].get() == "":
                f = 0
                break

        def isch(i):
            x, y = ['\u4e00', '\u9fa5']
            for wd in self.info[i].get():
                if not x <= wd <= y:
                    inpbox[i].config(fg='red')
                    return 0
            inpbox[i].config(fg='black')
            return 1

        def is_vavid_date(y,m,d):
            try:
                ye = int(y)
                mo = int(m)
                da = int(d)
                datetime.date(ye,mo,da)
                return 1
            except:
                return 0

        if f:
            info = self.info
            age = self.age
            if not is_vavid_date(age[0].get(),age[1].get(),age[2].get()):

                f = 0
            if not re.match(r'1[0-9]{10}', info[3].get()) or len(info[3].get()) != 11:
                f = 0
                inpbox[3].config(fg='red')
                # print(len(info[4].get()),info[4].get()[0])
            else:
                inpbox[3].config(fg='black')
            if re.search(r'[^0-9]{1,}', info[0].get()):
                f = 0
                inpbox[0].config(fg='red')
            else:
                inpbox[0].config(fg='black')
            if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn.net.edu]{1,3}$', info[4].get()):
                f = 0
                inpbox[4].config(fg='red')
            else:
                inpbox[4].config(fg='black')
            if re.search(r'[^0-9]{1,}', info[2].get()) or 2019 - int(age[0].get()) != int(info[2].get()):
                f = 0
                inpbox[2].config(fg='red')
            else:
                inpbox[2].config(fg='black')
            if isch(1) == 0:
                f = isch(1)
            if isch(5) == 0:
                f = isch(5)
            if isch(6) == 0:
                f = isch(6)
            return f
        else:
            return f

    def getpostdata(self):
        if self.checkinput():
            v= self.v
            tmp = []
            for i in range(7):
                if i == 2:
                    if v.get() == 0:
                        tmp.append('男')
                    else:
                        tmp.append('女')
                if i == 3:
                    tmp.append(self.age[0].get() + '/' + self.age[1].get() + '/' + self.age[2].get())
                tmp.append(self.info[i].get())
            return tmp
        else:
            return []

    def loaddata(self,data):
        for i in range(9):
            if i == 2:
                if data[i] == '男':
                    self.v.set(0)
                else:
                    self.v.set(1)
                continue
            if i == 4:
                tmp = data[4].split('-',2)
                self.age[0].set(tmp[0])
                self.age[1].set(tmp[1])
                self.age[2].set(tmp[2])
                continue
            if i == 3:
                self.info[2].set(data[i])
                continue
            if i < 2:
                self.info[i].set(data[i])
            self.info[i-2].set(data[i])

def Adduser():
    Inputwindow('Add')




def Edit():
    tmp =  leftlist.cur.tree.item(leftlist.cur.getselect())['values']
    x = tmp
    # print(x)
    if x == "":
        messagebox.showinfo('Error!', '请选择修改项')
    else:
        window = Inputwindow("Edit")
        window.loaddata(x)
def Deluser():
    v = messagebox.askyesno('Warning', '确定删除该学生信息?')
    if v:
        try:
            leftlist.cur.delete()
            if leftlist.cur.isempty():
                leftlist.delete()
            messagebox.showinfo('Reslut', '删除成功')
        except:
            messagebox.showinfo('Error!', '删除失败')

def Search():
    top = Toplevel()
    top.title("Search")
    # top.geometry("500x300+450+250")
    top.geometry("400x300+450+250")
    Label(top, text="查找", font=f \
          ).grid(row=0, column=0, padx=10, pady=5)
    # Label(top, text='查询方式', font=f1).grid(row=1, column=2)
    # li = ['编号', '姓名', '号码']
    # v = IntVar() # 查询方式
    # i = 0
    # for inx in li:
    #     Radiobutton(top, text=inx, variable=v, value=i, font=f1) \
    #         .grid(row=2, column=i + 1, pady=15, padx=25)
    #     i += 1
    # v.set(0)
    box = StringVar()
    Entry(top, font=f1, textvariable=box). \
        grid(pady=15, row=3, column=1, columnspan=3)

    def find():
        top = Toplevel()
        top.title('Result')
        top.geometry("1100x300+200+250")
        keyword = box.get()    # 查询关键字
        restable = Table(top)
        parenttree = leftlist.cur.tree
        children = parenttree.get_children()

        if dbopen:
            res = database.search(None,box.get(),leftlist.getselect())
            for ind in res:
                restable.insert(ind)
        else:
            try:
                for child in children:
                    if v.get() == 0:
                        item = parenttree.item(child)['values']
                        if keyword == "" or item[0] == int(keyword):
                            restable.insert(item)
                    elif v.get() == 1:
                        item = parenttree.item(child)['values']
                        if item[1] == keyword or keyword == "":
                            restable.insert(item)
                    else:
                        item = parenttree.item(child)['values']
                        if str(item[5]) == keyword or keyword == "":
                            restable.insert(item)
            except:
                pass
        restable.pack()

    # 清空命令
    def Clean():
        box.set('')

    Button(top, text='查找', font=f, bg='#ccccff', width=6, command=find). \
        grid(row=4, column=1, pady=15)
    Button(top, text='清空', font=f, bg='#ccccff', width=6, command=Clean). \
        grid(row=4, column=2, pady=10)
    Button(top, text='关闭', font=f, bg='#ccccff', width=6, command=top.destroy). \
        grid(row=4, column=3, pady=10)

def Backup():
    try:
        with open('userdata/data.csv','r') as r,open('userdata/backup.csv','w') as t:
            t.write(r.read())
        messagebox.showinfo('Reslut','备份成功！')
    except:
        messagebox.showinfo('Reslut','备份失败！')

def Restore():
    v = messagebox.askyesno('!','确定要恢复备份?')
    if v:
        if dbopen:
            database.restore('userdata/backup.csv')
        with open('userdata/data.csv','w') as r,open('userdata/backup.csv','r') as t:
            r.write(t.read())
        messagebox.showinfo('Reslut','导入成功,请重启！')




root = Tk()
root.title("MyContract")
#root.geometry('1015x500+230+180')

#打开图片
ima1 = PhotoImage(file='images/add.png')
ima2 = PhotoImage(file='images/edit.png')
ima3 = PhotoImage(file='images/delete.png')
ima4 = PhotoImage(file='images/search.png')
ima5 = PhotoImage(file='images/backup.png')
ima6 = PhotoImage(file='images/restore.png')

f=('楷体',14,"normal")
f1 = ('楷体',11,'normal')

#创建按钮
def CreateLab(root,ima,tex):
    g = LabelFrame(root,bg='#dfd')
    g.pack(side=LEFT,anchor=N,pady=5)
    ba = Button(g,text=tex,font=f,image=ima,compound=TOP)
    ba.pack(side=TOP,anchor=N)
    return ba

# 主界面菜单按钮
fra = Frame(root,bg='#dfd')
fra.pack(side=TOP,fill=X)
lab = [CreateLab(fra,im,ind) for ind,im in [('添加',ima1),('编辑',ima2), \
                                          ('删除',ima3),('查找',ima4),('备份',ima5),('恢复',ima6)]]
lab[0].config(command=Adduser)
lab[1].config(command=Edit)
lab[2].config(command=Deluser)
lab[3].config(command=Search)
lab[4].config(command=Backup)
lab[5].config(command=Restore)

leftlist = Listtree()




if __name__ == '__main__':
    mainloop()
