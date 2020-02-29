from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from DDns import DDns
import Utils
from urllib import request
import json
import re
import os


class Application(Frame):
    def del_tree(self):
        x=self.table.get_children()
        for item in x:
            self.table.delete(item)

    def getArea(self,event):
        for item in self.table.selection():
            item_text = self.table.item(item,"values")
        self.flashArea()
        self.changeRREntry.insert(0,item_text[1])
        self.changetypeEntry.insert(0,item_text[2])
        self.changetargetentry.insert(0,item_text[3])
        self.recordid = item_text[0]
    
    def flashArea(self):
        self.changeRREntry.delete(0,'end')
        self.changetypeEntry.delete(0,'end')
        self.changetargetentry.delete(0,'end')

    def adddns(self):
        res = DDns.add_record(self.accessKeyIdEntry.get(),self.accessSecretEntry.get(),self.domainEntry.get(),self.changeRREntry.get(),self.changetypeEntry.get(),self.changetargetentry.get())
        if res == "victory":
            tkinter.messagebox.showinfo("提示","添加成功")
        elif res == "already":
            tkinter.messagebox.showinfo("提示","记录已存在")
        else:
            tkinter.messagebox.showinfo("提示","操作失败")
        self.showRecords()

    def deletedns(self):
        res = DDns.delete_record(self.accessKeyIdEntry.get(),self.accessSecretEntry.get(),self.recordid)
        if res == "victory":
            tkinter.messagebox.showinfo("提示","删除成功")
        elif res == 'fail':
            tkinter.messagebox.showinfo("提示","该记录不存在")
        else:
            tkinter.messagebox.showinfo("提示","操作失败")
        self.showRecords()

    def updatedns(self):
        res = DDns.update_record(self.accessKeyIdEntry.get(),self.accessSecretEntry.get(),self.changeRREntry.get(),self.changetypeEntry.get(),self.changetargetentry.get())
        if res == "victory":
            tkinter.messagebox.showinfo("提示","修改成功")
        elif res == "already":
            tkinter.messagebox.showinfo("提示","记录已存在")
        elif res == "fail":
            tkinter.messagebox.showinfo("提示","该记录不存在，请添加")
        else:
            tkinter.messagebox.showinfo("提示","操作失败")
        self.showRecords()

    def showRecords(self):
        self.del_tree()
        if self.checkDomain() ==0 or self.checkId() == 0:
            return
        self.wanipEntry.delete(0,'end')
        wanip = json.load(request.urlopen('https://api.ipify.org/?format=json'))['ip']
        self.wanipEntry.insert(0,wanip)
        domain = self.domainEntry.get()
        DDns.save_records(self.accessKeyId,self.accessSecret,domain)
        with open('records.json','r') as recordsfile:
            jsonfile = json.load(recordsfile)
            records = jsonfile["DomainRecords"]["Record"]
            i = 0
            for record in records:
                self.table.insert('',i,values=(record["RecordId"],record["RR"],record["Type"],record["Value"]))
                i += 1

    def checkDomain(self):
        domain = self.domainEntry.get()
        regex = re.compile("([a-z|A-Z|0-9]+.)+([a-z|A-Z|0-9]+)")
        result = re.search(regex,domain)
        if result:
            return 1
        else :
            tkinter.messagebox.showerror("警告","域名输入错误")
            return 0

    def checkId(self):
        userid = self.accessKeyIdEntry.get()
        usersecert = self.accessSecretEntry.get()
        if userid  and usersecert :
            jsonfile = {"accessKeyId":self.accessKeyIdEntry.get(),"accessSecret":self.accessSecretEntry.get()}
            with open('account.json','w') as accountfile:
                json.dump(jsonfile, accountfile, sort_keys=True, indent=4, separators=(',', ': '))
            return 1
        else :
            tkinter.messagebox.showerror("警告","Id或Secret不合法")
            return 0

    def createWidgets(self):
        Label(self).grid(row=0,column=0)
        self.accessKeyId = ""
        self.accessSecret = ""
        isexist = os.path.exists('account.json')
        print(isexist)
        if isexist :
            with open('account.json','r') as accountfile:
                jsonfile = json.load(accountfile)
                accessKeyId = jsonfile["accessKeyId"]
                accessSecret = jsonfile["accessSecret"]
                if accessKeyId != None and accessSecret != None:
                    self.accessKeyId = accessKeyId
                    self.accessSecret = accessSecret
        self.accessKeyIdLabel = Label(self)
        self.accessKeyIdLabel["text"] = "accessKeyId："
        self.accessKeyIdLabel.grid(row = 1,column = 0)

        self.accessKeyIdEntry = Entry(self)
        self.accessKeyIdEntry.grid(row = 1,column = 1)
        self.accessKeyIdEntry.insert(0,self.accessKeyId)

        self.accessSecretLabel = Label(self)
        self.accessSecretLabel["text"] = "accessSecret："
        self.accessSecretLabel.grid(row = 1,column = 2)
        
        self.accessSecretEntry = Entry(self)
        self.accessSecretEntry.grid(row = 1,column = 3)
        self.accessSecretEntry.insert(0,self.accessSecret)

        self.domainlabel = Label(self)
        self.domainlabel["text"] = "域名："
        self.domainlabel.grid(row = 1,column = 4)

        self.domainEntry = Entry(self)
        self.domainEntry.grid(row = 1,column = 5)

        self.inputbutton = Button(self)
        self.inputbutton["text"] = "确定"
        self.inputbutton["command"] = self.showRecords
        self.inputbutton.grid(row = 1,column = 6)
        
        self.wanipLabel = Label(self,text="WanIP").grid(row=2,column=0)
        self.wanipEntry = Entry(self)
        self.wanipEntry.grid(row=2,column=1)

        self.table = ttk.Treeview(self,columns=['record_id','record_RR','record_type','record_target'],show='headings')
        self.sbar = Scrollbar(self)
        self.sbar.grid(row=3, column=6,sticky="ns")
        self.table.configure(yscrollcommand=self.sbar.set)
        self.sbar.configure(command=self.table.yview)
        self.table.grid(row = 3,column = 0,columnspan=7)
        self.table.column('record_id',width=200,anchor='center')
        self.table.column('record_RR',width=150,anchor='center')
        self.table.column('record_type',width=50,anchor='center')
        self.table.column('record_target',width=400,anchor='center')
        self.table.heading('record_id',text='记录ID')
        self.table.heading('record_RR',text='主机记录')
        self.table.heading('record_type',text='记录类型')
        self.table.heading('record_target',text='记录值')
        self.table.bind("<ButtonRelease-1>", self.getArea)

        # self.getButton = Button(self,text="获取",command=self.getArea).grid(row=4,column=2)
        self.flashButton = Button(self,text="清除",command=self.flashArea).grid(row=4,column=4)

        self.RRLabel = Label(self,text = '主机记录：').grid(row=5,column=0)
        self.changeRREntry = Entry(self)
        self.changeRREntry.grid(row=5,column=1)

        self.typeLabel = Label(self,text = '记录类型：').grid(row=5,column=2)
        self.changetypeEntry = Entry(self)
        self.changetypeEntry.grid(row=5,column=3)

        self.targetLabel = Label(self,text = '记录值：').grid(row=5,column=4)
        self.changetargetentry = Entry(self)
        self.changetargetentry.grid(row=5,column=5)

        self.adddnsButton = Button(self,text="添加",command=self.adddns).grid(row=6,column=3)
        self.deleteButton = Button(self,text="删除",command=self.deletedns).grid(row=6,column=4)
        self.updateButton = Button(self,text="修改",command=self.updatedns).grid(row=6,column=5)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()




root = Tk(className="ALi-Dns")
root.geometry("1000x430+110+50")
app = Application(master=root)
app.mainloop()