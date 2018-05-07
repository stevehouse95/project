import socket
import threading
import tkinter as tk 
from tkinter import END, Listbox, Toplevel, Toplevel, Entry, Button, Label, ACTIVE, ANCHOR
from genKey import genKey
from encrypt import encrypt
import  time
import tkinter.ttk as ttk
from datetime import datetime
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

        self.btnSend = Button(self.TPanedwindow1_p1, command = self.btnSendClicked)
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


        #self.btnSend.bind("<Button-1>", self.btnSendClicked)
        self.list.bind('<<ListboxSelect>>', self.listBoxSelectionChanged)
        self.name = name
        self.startBroadCasting() # start broadcasting that i am online
        self.p2pPort = 49789 # p2p port

    # Send button click event
    def btnSendClicked(self):
        peerName = str(self.list.get(self.list.curselection())) # get peer name whom to send the message
        peerName =peerName.lower()
        if peerName in peersList.keys():
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
            self.sock.connect((peersList[peerName],self.p2pPort))  
            msg = self.name + ": "+self.txtMsg.get() 
            if peerName in peersChatList.keys():
                peersChatList[peerName] = peersChatList[peerName] + "\n" + msg + "\n" + datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
            else:
                peersChatList[peerName] = msg + "\n" + datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
            
            msg =self.do_padding(msg)
            msg = encrypt(msg,key)     # encrypt the message  
            self.sock.send(msg.encode()) # send the message
            self.sock.close()
            self.txtMsgs.configure(state='normal')
            self.txtMsgs.delete("1.0",END)
            self.txtMsgs.insert(END,peersChatList[peerName]+"\n") # update the chat
            self.txtMsgs.configure(state='disabled')
            self.txtMsg.delete(0,END)

    def do_padding(self,msg):
       return msg.rjust(500, '~')

    # list box selection chnaged event to update the chat
    def listBoxSelectionChanged(self,event):
        try:
            try:
                self.txtMsgs.delete("1.0",END) # clear the chat area
            except Exception as e  :
                pass
            peerName = str(self.list.get(ANCHOR)) # get current selected peer name
            peerName = peerName.lower()
            if(peerName in  peersChatList.keys()): 
                self.txtMsgs.insert(END,peersChatList[peerName]) # update chat
            else:
                self.txtMsgs.insert(END,"")
        except Exception as e:
            pass


    # one of the peers that is started first will become UDP server that listens broadcast request and handles whos online
    class UDPServerThread(threading.Thread):
        def __init__(self, threadID, name,listBoxClients):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.listBoxClients = listBoxClients
        def run(self):
            print("Starting " + self.name)
            self.serverSide()

        # to handle udp connections
        def serverSide(self):
            name = self.name
            address = ('', 54545)
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            server_socket.bind(address)
            while True: # keep listening
                print("Listening")
                try:
                    recv_data, addr = server_socket.recvfrom(2048) # get data from socket
                    sender_ip = addr[0] # get sender ip
                    data_received = recv_data.decode() # get data
                    print(sender_ip,':',data_received)
                    if data_received.lower() in peersList.keys() or data_received.lower() == name.lower(): # check if name already exists ask sender to change name
                        server_socket.sendto("Invalid Name".encode(), addr)
                        continue
                    server_socket.sendto(name.encode(), addr) # send my name to connecting client
                    time.sleep(1)
                    server_socket.sendto(key.encode(),addr) # send key for encrypting/decrypting
                    for peer in peersList.keys(): # tell each available peer that a new client has arrived so that they can update their list
                        server_socket.sendto(str((peer.lower(),peersList[peer])).encode(),addr)
                    for sck in udpSockets: # send other available client details to new client
                        try:
                            sck[0].sendto(str((data_received,sender_ip)).encode(),sck[1])
                        except  :
                            pass
                    udpSockets.append((server_socket,addr))
                    peersList[data_received.lower()] = sender_ip 
                    self.listBoxClients.insert(END,data_received)  # add client in list
                except  Exception as e:
                    pass
    
    # this class handles UDP thread functionality, i.e when a new client arrives UDP server will broadcast a message and this class handles it and updates its list. 
    class UDPClientThread(threading.Thread):
        def __init__(self, threadID, name,listBoxClients,client_socket):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.listBoxClients = listBoxClients
            self.name = name
            self.client_socket = client_socket
        def run(self):
            print("Starting " + self.name)
            self.clientSide()    
       


        # this method handles the udp connections
        def clientSide(self):
            while True:
                try:
                    self.client_socket.settimeout(1000)
                    peer_data,sender_address = self.client_socket.recvfrom(2048) # get data sent by udp server
                    peer = str(peer_data.decode()) # decode the data
                    peer_name = str(peer.split(', ')[0].replace('(','')).replace("'","") # get peerName
                    peer_addr = str(peer.split(', ')[1].replace(')','')).replace("'","") # get perrAddress
                    peersList[peer_name.lower()] = peer_addr 
                    self.listBoxClients.insert(END,peer_name.lower())  # add client in list
                except Exception as e:
                    pass
        


    # this function starts broadcasting and if a UDP server is available connect to it otherwise start a server
    def startBroadCasting(self): 
        address = ('<broadcast>', 54545) 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        global key
        name = self.name
        client_socket.sendto(name.encode(), address) # send the name to server
        try: # try to connect to a broadcast server if available 
            client_socket.settimeout(5) 
            recv_data, addr = client_socket.recvfrom(2048) # get the message from server 
            while str(recv_data.decode()) == "Invalid Name": # if server says its invaild name then ask to re input the name
                name = input("Name already taken, Enter Naw name = ")
                client_socket.sendto(name.encode(), address) 
                recv_data, addr = client_socket.recvfrom(2048)
            peersList[recv_data.decode().lower()] = addr[0] # add the server in peer list
            self.list.insert(END,recv_data.decode().lower()) # update the listBox
            recv_data, addr = client_socket.recvfrom(2048) # get key from server
            
            key = recv_data.decode()
            self.UDPClientThread(1, name,self.list, client_socket).start() #starts udp client
        except Exception as e: # if server is not available start udp server
            key = genKey(500) # generate key
            self.UDPServerThread(2, name,self.list).start()


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
