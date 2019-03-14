#
# Description: This is a small program I wrote in order to make email spoofing and hence testing of SPF, DMARC and DKIM records a bit easier.
# Motivation: I was annoyed, that my SMTP server quit on me everytime I accidentally forgot one step in our communication. 
# Benefit: Send slightly altered spoofing mails without going through all of the SMTP chain again and again :)
# Questions: Frederic Mohr [at] LastBreach com
#
# Dependencies: python3, python3-tk
# Version: v1.190314

from tkinter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter.scrolledtext import ScrolledText

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()
    
    #Creation of init_window
    def init_window(self):
        self.master.title("SpoofiPy")

        Label(root, text="Sender Output",font='Helvetica 12 bold').grid(row=16,pady=20,columnspan=8)
        f_output.grid(row = 17, column = 1, sticky=W+E+S, columnspan=4,pady=20)

        
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds an exit button to the menu option
        file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        
        Label(root, text="SMTP Settings",font='Helvetica 12 bold').grid(row=0,pady=20,columnspan=8)
        
        # Dictionary with options
        choices = { 'Plain','SSL/TLS','StartTLS'}
        f_smtptls.set('StartTLS') # set the default option
        f_plaintls = OptionMenu(root, f_smtptls, *choices)

        choices2 = { 'AUTH LOGIN'}
        f_defauth.set('AUTH LOGIN') # set the default option
        f_authtyp = OptionMenu(root, f_defauth, *choices2)

        choices3 = { 'plain','html'}
        f_deftext.set('plain') # set the default option
        f_texthtml = OptionMenu(root, f_deftext, *choices3)

        Label(root, text="SMTP Host").grid(row=1, column=0)
        f_smtphost.grid(row=1,column=1, sticky=W+E, columnspan=4)
        Label(root, text="SMTP Port").grid(row=2, column=0)
        f_smtpport.grid(row=2,column=1, sticky=W+E, columnspan=4)
        Label(root, text="SMTP User").grid(row=3, column=0)
        f_smtpuser.grid(row=3,column=1, sticky=W+E, columnspan=4)
        Label(root, text="SMTP Pass").grid(row=4, column=0)
        f_smtppass.grid(row=4,column=1, sticky=W+E, columnspan=4)
        Label(root, text="Encryption").grid(row=5, column=0)
        f_plaintls.grid(row = 5, column = 1, sticky=W+E, columnspan=4)
        #Label(root, text="Authentication").grid(row=6, column=0)
        #f_authtyp.grid(row = 6, column = 1, sticky=W+E, columnspan=4)

        # SPOOFING OPTIONS
        Label(root, text="Spoofing Options",font='Helvetica 12 bold').grid(row=7,pady=20,columnspan=8)
        
        Label(root, text="MAIL FROM:").grid(row=8, column=0)
        f_mailfrom.grid(row=8,column=1, sticky=W+E, columnspan=4)
        Label(root, text="RCPT TO:").grid(row=9, column=0)
        f_rcptto.grid(row=9,column=1, sticky=W+E, columnspan=4)
        Label(root, text="From:").grid(row=10, column=0)
        f_envfrom.grid(row=10,column=1, sticky=W+E, columnspan=4)
        Label(root, text="To:").grid(row=11, column=0)
        f_envto.grid(row=11,column=1, sticky=W+E, columnspan=4)
        
        #Label(root, text="Msg Typ:").grid(row=12, column=0)
        #f_texthtml.grid(row = 12, column = 1, sticky=W+E, columnspan=4)
        
        Label(root, text="Subject:").grid(row=13, column=0)
        f_subject.grid(row = 13, column = 1, sticky=W+E, columnspan=4)
        Label(root, text="Message:").grid(row=14, column=0)
        f_message.grid(row = 14, column = 1, sticky=W+E, columnspan=4)
        

        Button(root, text='Send', command=self.send_mail).grid(row=15, column=1,columnspan=6, sticky=W+E,pady=10)


    def client_exit(self):
        exit()
        
    def send_mail(self):
        
        debug = "###########################################################################\n### DEBUGGING INFO ###\n"
        
        try:        
            if(f_smtptls.get() == "SSL/TLS"):
                #print("SSL/TLS is set")
                server = smtplib.SMTP(f_smtphost.get(), f_smtpport.get())
                server.ehlo()

            
            elif(f_smtptls.get()=="StartTLS"):
                #print("StartTLS is set")
                server = smtplib.SMTP(f_smtphost.get(), f_smtpport.get())
                server.ehlo()
                server.starttls()
            else:        
                server = smtplib.SMTP(f_smtphost.get(), f_smtpport.get())
                server.ehlo()
        except:
            debug = debug+"[!] Could not connect to server!\n"
        
        try:
            server.login(f_smtpuser.get(),f_smtppass.get())
        except:
            debug = debug+"[!] Could not finish login procedure!\n"
            
        msgtxt = f_message.get(1.0,END)
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f_envfrom.get()
        msg['To'] = f_envto.get()
        msg['Subject'] = f_subject.get()
        
        text=MIMEText(msgtxt, 'text')
        html=MIMEText(msgtxt, 'html')
        
        msg.attach(text)
        msg.attach(html)
        
        try:
            server.sendmail(f_mailfrom.get(),f_rcptto.get(),msg.as_string())
            debug = debug+"[*] Looking good! :)\n"
        except:
            debug = debug+"[!] Could not send email!\n"
            
        debug = debug+"\n\n### Email Summary ###\n"+msg.as_string()
        f_output.insert(1.0,debug)




root = Tk()

#vars - smtp settings
f_smtphost = Entry(root,bg="white")
f_smtpport = Entry(root,bg="white")
f_smtpuser = Entry(root,bg="white")
f_smtppass = Entry(root,show="*",bg="white")
f_smtptls = StringVar(root)

# vars - spoofing options
f_defauth = StringVar(root)
f_deftext = StringVar(root)
f_mailfrom = Entry(root,bg="white")
f_rcptto   = Entry(root,bg="white")
f_envfrom  = Entry(root,bg="white")
f_envto    = Entry(root,bg="white")
f_texthtml = Entry(root,bg="white")
f_subject  = Entry(root,bg="white")
f_message  = ScrolledText(root,height = 10,bg="white",wrap   = 'word')
f_output   = ScrolledText(root,height = 10,bg="white",wrap   = 'word')

e1 = Entry(root)
e2 = Entry(root)
blank = Entry(root)


#position of the window
root.geometry("+300+25")

app = Window(root)
root.mainloop()
