import socket
import threading
import tkinter as tk 
from tkinter import END, Listbox, Toplevel, Toplevel, Entry, Button, Label, ACTIVE, ANCHOR
import  time
import tkinter.ttk as ttk
udpSockets = list() # a list of udp sockets to send new online users
peersList = dict() # a dictionary that hold a peerName as key and its ip address as port
peersChatList = dict() # a dictionary that hold chat with a peer, peerName as key and chatList as value
key = ""


class Application:
    def __init__(self, master,name):

        master.geometry("600x450+405+183")
        self.TPanedwindow1 = ttk.Panedwindow(master, orient="horizontal")
        self.TPanedwindow1.place(relx=0.0, rely=0.0, relheight=0.98
                , relwidth=1.01)
        self.TPanedwindow1_p1 = ttk.Labelframe(width=405)
        self.TPanedwindow1.add(self.TPanedwindow1_p1)
        self.TPanedwindow1_p2 = ttk.Labelframe()
        self.TPanedwindow1.add(self.TPanedwindow1_p2)

        self.txtMsgs = tk.Text(self.TPanedwindow1_p1,state='disabled')
        self.txtMsgs.place(relx=0.0, rely=0.0, relheight=0.93, relwidth=1.0, y=-12
                , h=12)
        self.txtMsgs.configure(background="white")
        self.txtMsgs.configure(font="TkTextFont")
        self.txtMsgs.configure(foreground="black")
        self.txtMsgs.configure(highlightbackground="#d9d9d9")
        self.txtMsgs.configure(highlightcolor="black")
        self.txtMsgs.configure(insertbackground="black")
        self.txtMsgs.configure(selectbackground="#c4c4c4")
        self.txtMsgs.configure(selectforeground="black")
        self.txtMsgs.configure(width=405)

        self.txtMsg = tk.Entry(self.TPanedwindow1_p1)
        self.txtMsg.place(relx=0.0, rely=0.95,height=20, relwidth=0.73)
        self.txtMsg.configure(background="white")
        self.txtMsg.configure(disabledforeground="#a3a3a3")
        self.txtMsg.configure(font="TkFixedFont")
        self.txtMsg.configure(foreground="#000000")
        self.txtMsg.configure(highlightbackground="#d9d9d9")
        self.txtMsg.configure(highlightcolor="black")
        self.txtMsg.configure(insertbackground="black")
        self.txtMsg.configure(selectbackground="#c4c4c4")
        self.txtMsg.configure(selectforeground="black")

        self.btnSend = Button(self.TPanedwindow1_p1)
        self.btnSend.place(relx=0.74, rely=0.94, height=24, width=107, y=3)
        self.btnSend.configure(activebackground="#d9d9d9")
        self.btnSend.configure(activeforeground="#000000")
        self.btnSend.configure(background="#d9d9d9")
        self.btnSend.configure(disabledforeground="#a3a3a3")
        self.btnSend.configure(foreground="#000000")
        self.btnSend.configure(highlightbackground="#d9d9d9")
        self.btnSend.configure(highlightcolor="black")
        self.btnSend.configure(pady="0")
        self.btnSend.configure(text='Send')

        self.list = Listbox(self.TPanedwindow1_p2)
        self.list.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0
                , y=-12, h=12)
        self.list.configure(background="white")
        self.list.configure(disabledforeground="#a3a3a3")
        self.list.configure(font="TkFixedFont")
        self.list.configure(foreground="#000000")
        self.list.configure(highlightbackground="#d9d9d9")
        self.list.configure(highlightcolor="black")
        self.list.configure(selectbackground="#c4c4c4")
        self.list.configure(selectforeground="black")
        self.list.configure(width=134)


# this class is used to display simple window to input name
class MyDialog:

    def __init__(self, parent):
        name = self.name = ""
        top = self.top = Toplevel(parent)

        Label(top, text="Name").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)
        
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        name = self.name = self.e.get()
        self.top.destroy()



if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    d= MyDialog(root)  # ask for name
    root.wait_window(d.top)
    name = d.name.lower()
    app = Application(root,name) 
    root.title("One Time Pad - Encrypted Message Client ("+name+")")
    root.resizable(False,False)
    root.iconbitmap(r'logo.ico')
    root.deiconify()
    root.mainloop() #start the main window
