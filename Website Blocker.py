from time import sleep
import os
from datetime import *
from tkinter import *
import threading

#Basic Initialisations
#os.chdir(r"C:\Windows\System32\drivers\etc")
tmp_sites=[]
BlockPeriod=None
sizes={"LoginPage":"400x420","IntroPage":"516x335","PermPage":"502x630","TempPage":"960x588"}

#Main Functions
def temp_w_remover(site):
    with open("hosts.txt",'r') as f:
            global tmp_sites
            w=f.read()    
            site=site.strip()
            if not site:
                msg="Enter  a  Website"
            elif (site in w):
                msg="Blocked Permanently"    
            elif site in tmp_sites:
                del(tmp_sites[tmp_sites.index(site)])
                print(tmp_sites)
                msg="Removed!"
            else:
                msg="NOT  in  the  Blocking  List"    
    return msg

def temp_w_adder(site):
    with open("hosts.txt",'r') as f:
            global tmp_sites
            w=f.readlines()    
            site=site.strip()
            if not site:
                msg="Enter  a  Website"
            elif (site in w):
                msg="Permanently  Blocked "    
            elif site in tmp_sites:
                msg="Already  Added"
            else:

                tmp_sites.append(site)
                msg=" Added  For  Blocking"
                print(tmp_sites)
    return msg
    
def show_sites(i):
    show=[]
    if i=="p":
        with open("hosts.txt","r") as f:
            x=f.readlines()
            x.reverse()
            for w in x:
                if (w[0]!="#") and (w[0]!='\n') :
                    if("#"+i in w):
                        show.append(w.split()[1])
                    else:
                        pass

                elif (w[0]=="#"):
                    break
    elif i =="t":
        show=tmp_sites    
    return show

def Blocker(site=None,block_type=None):
    alt_site = "127.0.0.1"
    with open("hosts.txt","r+") as f:
        x=f.read()
        site=site.strip()
        if not site:
            msg="Enter a Website"
        elif(site in x):
            msg="Website  is  already  Blocked"    
        else:
            f.write("\n"+alt_site+" "+site+" #"+ block_type)
            msg="Blocked!"
    return msg

def Unblocker(site):
    site=site.strip()
    with open("hosts.txt","r")as f:
        for i,j in enumerate(f.readlines()):
            if not site:
                msg="Enter  a  Website"
                break
            
            elif site in j:
                msg=Modify(i)
                break
            
            else:
                msg="Website  was  not  Blocked"    
    return msg

def Modify(line_no):
    with open("hosts.txt","r") as f:
        y=f.readlines()
        del(y[line_no])
    with open("hosts.txt","w") as f:
        f.writelines(y)
        msg="Unblocked  Successfully"    
    return msg

def temp_btime():
    x=input("Time ex. 12:12:12 -->> ")
    x=x.split(":")
    return time(int(x[0]),int(x[1]),int(x[2]))

def time_period(s):
    s=s.strip()
    #t=time(23,59,59)
    y=datetime.today() # same as datteiime.now()
    #x=datetime.strptime(s,"%H:%M:%S")
    #x=x-timedelta(hours=1,minutes=1,seconds=1)
    
    if not s:
        msg="Period  Not  Added"
        return msg    
    
    else:
        try:
            x=s.split(":")
            q=timedelta(days=int(x[0]),hours=int(x[1]),minutes=int(x[2]),seconds=int(x[3]))

            global BlockPeriod
            BlockPeriod = y + q
            msg="Blocking till --> "+str(BlockPeriod.time())
            print(BlockPeriod)
        
        except Exception:
            msg="Error in Time Period"
        
        return msg

def temp_block(BlockPeriod):
    flag=True
    while flag:
        with open("hosts.txt","r+") as f:
            content=f.read()
            
            if (datetime.now() < BlockPeriod):
                
                for website in tmp_sites:
                    if website not in content:
                        Blocker(website,"t")
                        print("Blocked --> ",website)
                    else:
                        pass
        
            else:
                for website in tmp_sites:
                    print("Unblocked --> ",website)
                    Unblocker(website)
                tmp_sites.clear()
                BlockPeriod=None
                flag=False
                msg="*Time Completed*" 
            
            sleep(5) 
    return msg       

#########################################################################################
                             #-#-#-#--***TKINTER Portion***--#-#-#
#########################################################################################
class MainWindow(Tk):
    def __init__(self,*args,**kwargs):
        Tk. __init__(self,*args,**kwargs)
        self['bg']="#292929"
        self.title("Website  Blocker")

        main=Frame(self)
        main.grid(row=0,column=0,sticky="nsew")
        self.all_frames={}

        for i in ("LoginPage","IntroPage","PermPage","TempPage"):
            self.all_frames[i]=eval(i)(main,self)
            self.all_frames[i].grid(row=0,column=0,sticky="nsew")
            self.all_frames[i].grid_remove()
        
        self.all_frames["LoginPage"].grid()

    def show_frame(self,caller,called):
        self.all_frames[caller].grid_remove()
        self.all_frames[called].grid()
        root.geometry(sizes[called])
        

class IntroPage(Frame):
    def __init__(self,parent,root):
        super().__init__()
        self['bg']="#292929"
        print(self,"*****************",root)
#Labels
        self.h=Label(self,text=" START BLOCKING! ",bg="#149662",fg="white",font='impact 40 bold underline',anchor="center")
        self.h.grid(row=0,column=0,columnspan=7,sticky="nsew")
        self.p=Label(self,text="Permanent",bg="#FF652F",fg="white",font='impact 30 italic ',padx=60,pady=20)
        self.p.grid(row=1,column=2,columnspan=3,padx=10,pady=20,sticky="nsew")
        self.t=Label(self,text="Temporarily",bg="#FF652F",fg="white",font='impact 30 italic',padx=50,pady=20)
        self.t.grid(row=2,column=2,columnspan=3,padx=10,pady=20,sticky="nsew")

#Buttons
        #self.buttonimg=PhotoImage(file="Buttonpng.png")
        self.pb=Button(self,text="*GO-->>*",font='impact 25 italic',bg="#FFE400",fg="white",width=10,command=lambda:root.show_frame("IntroPage","PermPage"))
        self.pb.grid(row=1,column=6,sticky="nsew",pady="0.3c",padx="0.3c")
        self.tb=Button(self,text="*GO-->>*",font='impact 25 italic',bg="#FFE400",fg="white",width=10,command=lambda:root.show_frame("IntroPage","TempPage"))
        self.tb.grid(row=2,column=6,sticky="nsew",pady="0.3c",padx="0.3c")

class PermPage(Frame):
    def __init__(self,parent,root):
        Frame.__init__(self,parent)
        self['bg']="#292929"
        self.e=StringVar(value="Enter A WebSite")

#Labels
        self.h=Label(self,text=" PERMANENT BLOCKING ",bg="#149662",fg="white",font='impact 40 bold underline',anchor="center",height=1)
        self.h.grid(row=0,column=0,columnspan=7,sticky="nsew")

#Entry  
        self.web_adder=Entry(self,font="Impact 20 italic", textvariable=self.e,justify="center")
        self.web_adder.grid(row=1,column=1,columnspan=5,sticky="nsew",pady="0.3c") 

#Buttons
        #self.backimg=PhotoImage(file='icon.png')
        self.backB=Button(self, text="< Back <",font='impact 20 italic ',fg="white",bg="#FFE400",anchor="center",command=lambda:root.show_frame("PermPage","IntroPage"))
        self.backB.grid(row=2,column=3)
        self.blockB=Button(self,font='impact 30 italic ',text="Block",fg="white",bg="#FF652F",anchor="center",padx='0.5c',command=self.block_button)
        self.blockB.grid(row=2,column=1)
        self.unblockB=Button(self,font='impact 30 italic ',text="Unblock",fg="white",bg="#FF652F",anchor="center",padx='0.5c',command=self.unblock_button)
        self.unblockB.grid(row=2,column=5)

#Info Displayer

        self.info=Text(self,font="impact 20 italic",height=10,width=30)
        self.info.grid(row=3,column=0,columnspan=7,sticky="nsew",pady="1c")
        self.info_display("p")

#FUNCTIONS ASSCOCIATED WITH BUTTONS
    def info_display(self,q):
        x=show_sites(q)

        if not x:
            self.info.config(state="normal")
            self.info.delete(1.0,END)
            self.info.insert(1.0,"  "+"*Permanently Blocked*\n"+"  ")
            self.info.insert(2.0,"NONE")
            self.info.config(state="disabled")
            return

        elif q=="p":
            self.info.config(state="normal")
            self.info.insert(1.0,"  "+"*Permanently Blocked*\n"+"  ")
            self.info.delete(2.0,END) 
            
            for i,w in enumerate(x):            
                self.info.insert(float(i+2),"\n-->"+w)  
            
            self.info.config(state="disabled")
        
        elif q=="t":
            self.info2.config(state="normal")           
            self.info2.insert(1.0,"  "+"*Temporarily Blocked*\n"+"  ")            
            
            if not tmp_sites:
                self.info2.delete(2.0,END)
                self.info2.insert(2.0,"\nNONE")
                return
            else:
                self.info2.delete(2.0,END)
                for i,w in enumerate(x):
                    self.info2.insert(float(i+2),'\n-->'+w)        
                self.info2.config(state="disabled")
        return

    def block_button(self):
        x=self.e.get()
        y=Blocker(x,'p')
        self.e.set(y)
        self.info_display("p")        
        return

    def unblock_button(self):
        x=self.e.get()
        y=Unblocker(x)
        self.e.set(y)
        self.info_display("p")   
        #self.info_display()  
        return 


class TempPage(Frame):
    def __init__(self,parent,root):
        Frame.__init__(self,parent)
        self['bg']="#292929"
        self['height']=10
        root.geometry("960x588")
        self.ew=StringVar(value="Enter A WebSite")
        self.et=StringVar(value="For How Long -> Days:H:M:S")

#Labels
        self.h=Label(self,text=" Temporary Blocking ",bg="#149662",fg="white",font='impact 40 bold underline',anchor="center",height=1)
        self.h.grid(row=0,column=0,columnspan=7,sticky="nsew")
        self.t2=Label(self,text=" Wait for the above given period of time. ",bg="#FF652F",fg="white",font='impact 20 bold underline',anchor="center",height=1)
#Entry
        self.web_adder=Entry(self,font="Impact 20 italic", textvariable=self.ew,justify="center")
        self.web_adder.grid(row=1,column=1,columnspan=5,sticky="nsew",pady="0.3c")        
        self.time_adder=Entry(self,font="Impact 20 italic", bg="cyan",textvariable=self.et,width=30,justify="center")  

#Buttons
        self.addB=Button(self,font="impact 20 italic underline",text="Add+",fg="white",bg="#FF652F",command=self.add_button)
        self.addB.grid(row=2,column=1)
        
        self.removeB=Button(self,font="impact 20 italic underline",text="Remove",fg="white",bg="#FF652F",command=self.remove_button)
        self.removeB.grid(row=2,column=3)   
        
        self.settimeB=Button(self,font="impact 20 italic underline",text="Set Time",fg="white",bg="#FF652F",command=self.settime_button)
        self.settimeB.grid(row=2,column=5)
        

        self.timeB=Button(self,font="impact 20 italic underline",text="Fix Time",fg="white",bg="#FF652F",command=self.time_button)
        self.backB=Button(self,  text="< Back <",font='impact 20 italic ',fg="white",bg="#FFE400",anchor="center",command=lambda:root.show_frame("TempPage","IntroPage"))
        self.backB.grid(row=3,column=3)

        self.blockB=Button(self,font="impact 20 italic underline",text="Block",fg="white",bg="#FF652F",command=self.block_button)
        #self.forceB=Button(self,font="impact 20 italic underline",text="Forced EXIT",fg="white",bg="#FF652F",command=self.force_button)

        #self.backimg=PhotoImage(file='icon.png')
        self.backB2=Button(self, text="< Back <",font='impact 20 italic ',fg="white",bg="#FF652F",anchor="center",command=self.back_button)

#Displaying Info for blocked Websites
        self.info=Text(self,font="impact 20 italic",height=10,width=30)
        self.info.grid(row=3,column=0,columnspan=3,sticky="nsew",pady="1c")
        self.info_display("p")
        self.info2=Text(self,font="impact 20 italic",height=10,width=30)
        self.info2.grid(row=3,column=4,columnspan=3,sticky="nsew",pady="1c")
        self.info_display("t")

#FUNCTIONS ASSCOCIATED WITH BUTTONS

    def info_display(self,q):
        x=show_sites(q)
        if q=="p":
            self.info.config(state="normal")
            self.info.insert(1.0,"  "+"*Permanently Blocked*\n"+"  ")
            self.info.delete(2.0,END) 

            for i,w in enumerate(x):            
                self.info.insert(float(i+2),"\n-->"+w)  
            self.info.config(state="disabled")
        
        elif q=="t":
            self.info2.config(state="normal")           
            self.info2.insert(1.0,"  "+"*Temporarily Blocked*\n"+"  ")            
            
            if not tmp_sites:
                self.info2.delete(2.0,END)
                self.info2.insert(2.0,"\nNONE")
                return
            
            else:
                self.info2.delete(2.0,END)
                for i,w in enumerate(x):
                    self.info2.insert(float(i+2),'\n-->'+w)        
                self.info2.config(state="disabled")
        return

    def add_button(self):
        x=self.ew.get()
        y=temp_w_adder(x)         
        self.ew.set(y)
        self.info_display("t")
        return

    def remove_button(self):
        x=self.ew.get()
        y=temp_w_remover(x)         
        self.ew.set(y)
        self.info_display("t")
        return

    def settime_button(self):
        if not tmp_sites:
            self.ew.set("Add  Websites  First")
            return
        
        else:

            self.web_adder.grid_remove()
            self.addB.grid_remove()
            self.settimeB.grid_remove()
            self.removeB.grid_remove()
            self.time_adder.grid(row=1,column=1,columnspan=5,sticky="nsew",pady="0.3c") 
            self.timeB.grid(row=2,column=1)
            self.backB2.grid(row=3,column=3)
            self.blockB.grid(row=2,column=5)
            return

    def back_button(self):
        self.web_adder.grid()
        self.addB.grid()
        self.settimeB.grid()
        self.removeB.grid()
        self.backB.grid()
        self.backB2.grid_remove()
        self.blockB.grid_remove()
        self.time_adder.grid_remove()
        self.timeB.grid_remove()
        return 

    def time_button(self):
        if not tmp_sites:
            self.et.set("Add  Websites  First")
            return

        else:
            x=self.et.get()
            y=time_period(x)
            self.et.set(y)
            print(BlockPeriod)
            return

    def block_button(self):

        if (BlockPeriod==None):
            self.et.set("Set Time Period")
            print(BlockPeriod)
            return
        
        else:
            self.timeB.grid_remove()
            self.backB.grid_remove()
            self.backB2.grid_remove()
            self.blockB.grid_remove()
            self.t2.grid(row=2,column=0,columnspan=7)
            root.geometry("848x600")
            threading.Thread(target=temp_block,args=(BlockPeriod,)).start()
            threading.Thread(target=self.timer,args=(BlockPeriod,)).start()
        return    

    def timer(self,x):
        while True:
            y=x-datetime.now()
            if y.days==-1:
                self.info_display("t")
                self.et.set(" WEBSITES  UNBLOCKED ")
                sleep(3)
                root.show_frame("TempPage","IntroPage")
                self.back_button()
                self.t2.grid_remove()
                break
            self.et.set(y)
            sleep(1)
        return    


    def force_button(self):
        self.forceB.grid_remove()
        tmp_sites.clear()
        global BlockPeriod
        BlockPeriod=None
        for i in tmp_sites:
            Unblocker(i)
        root.show_frame("TempPage","IntroPage")
        return


class LoginPage(Frame):
    def __init__(self,parent,root):
        self.try_count=3
        super().__init__()
        self['bg']="#292929"
        self.username=StringVar()
        self.password=StringVar()
        self.res=StringVar()
        print(self,"*****************",root)

#Labels
        self.h=Label(self,text=" WEBSITE BLOCKER ",bg="#149662",fg="white",font='impact 40 bold underline',anchor="center")
        self.h.grid(row=0,column=0,columnspan=7,sticky="nsew")
        self.u=Label(self,text="UserName",bg="#FF652F",fg="white",font='impact 30 italic ',padx="0.29c")
        self.u.grid(row=1,column=1,columnspan=2,sticky="nsew",pady="0.3c")
        self.p=Label(self,text="Password",bg="#FF652F",fg="white",font='impact 30 italic')
        self.p.grid(row=2,column=1,columnspan=2,sticky="nsew",pady="0.3c")

#Buttons
        self.login=Button(self,text="Login",font='impact 30 italic ',fg="white",bg="#FF652F",anchor="center",padx='0.5c',command=self.loginB)
        self.login.grid(row=4,column=2,columnspan=3,sticky="nsew",pady="0.3c",padx="0.3c")

#Entries
        self.eu=Entry(self,textvariable=self.username,font="impact 30 italic",width=10)
        self.eu.grid(row=1,column=4,columnspan=2,sticky="nsew",pady="0.3c")
        self.ep=Entry(self,textvariable=self.password,show="*",font="impact 30 italic",width=10)
        self.ep.grid(row=2,column=4,columnspan=2,sticky="nsew",pady="0.3c")
        self.es=Entry(self,textvariable=self.res,font="impact 30 italic",width=10,justify="center")
        self.es.grid(row=3,column=1,columnspan=5,sticky="nsew",pady="0.3c")
        self.es.config(state="disabled")

#FUNCTIONS FOR BUTTONS
    def loginB(self):
        u=str(self.username.get()).strip().lower()
        p=str(self.password.get()).strip().lower()
        

        if  not u and not p:
            self.res.set("Enter Both Credentials.")
            self.username.set("")
            self.password.set("")


        elif  u!="user" or p!="pass":
            self.try_count-=1
            self.res.set(str(self.try_count) +" CHANCES LEFT.")
            self.username.set("")
            self.password.set("")
            print(self.try_count)

        elif u == "user" and p=="pass":
            self.res.set("Login Successful.")
            self.username.set("")
            self.password.set("")
            sleep(1)
            root.show_frame("LoginPage","IntroPage")
            return True

        if self.try_count==0 :
            root.quit()    
        return 


###***Main***###
root=MainWindow()
root.geometry("415x405")
root.mainloop()
