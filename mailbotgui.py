import tkinter as tk
import datetime 
from tkinter import scrolledtext
import imaplib, smtplib, email, getpass
from email.parser import HeaderParser

"""Note that this will only work on gmail servers but working on adding 'imap.live.com' functionality for hotmail as well 
   Still Going to be working on optimizing the check_mail and delete_mail possibly using the threading module to make a worker pool
   to shorten the time it takes. because right now it loops through the emails 1 at a time. it also interupts the tkinter mainloop
   causing it to hang until the emails are fetched still need to figure out how to make it fetch emails faster. There has to be a 
   better way to loop through and do the deleting. 
   The sort functionality hasn't been added yet still not sure if i will be finishing that one or just deleting it.
   I am self taught and still a begginer so any input on this is much appreciated if anyone with some experience happens to see this."""


addresses = []

deleteList = []

user = ''
password = ''


def get_mail(user, pswd, lst, uilist):

    """Need to figure out if there is a way to make this work faster and maybe set it up to fetch all the addresses
        as soon as the person has logged into their email."""

    print(datetime.datetime.now())  

    mailServer = imaplib.IMAP4_SSL('imap.gmail.com')
    
    mailServer.login(user, pswd)

    mailServer.select('INBOX')

    typ, data = mailServer.search(None, 'All')

    for num in data[0].split():
        
        #append our header data to a list. 
                           
        #headers.append(get_header(mailServer, num))
        

        #Fetch the raw data from our emails 
        result, data = mailServer.fetch(num, '(BODY[HEADER])')
        
        rawBytes = email.message_from_bytes(data[0][1])

        #bodies.append(get_body(rawBytes))
        email_from = str(email.header.make_header(email.header.decode_header(rawBytes['From'])))
        
        address = seperate_address(email_from)

        if address not in lst:

            lst.append(address)

        else:

            continue
    #check_for_address(get_header(mailServer, num), mailServer, num, adrs)     

    mailServer.close()

    mailServer.logout()

    print(datetime.datetime.now()) 

    #this bit adds the email addresses into the ListBox Widget 
    for address in lst:

        uilist.insert(tk.END, address)


def seperate_address(string):

    if '<' in string:

        firstSplit = string.split('<')

        secondSplit = firstSplit[1].split('>')

        address = secondSplit[0]

    else:

        address = string

    return address


def  to_delete_list(adrList, dAdrList, dList):
                                                                                                                                                                                                                                                                                                       
    """we need to make sure that if an item is in the sort list it should not be able to be in the delete list and vice versa.
        Might  seperate the curselection() and get() methods into two seperate lines to make things  more readable.
        adrList.curselection() gives the index of a selected item in the listBox adrList.get() gets a value from the list at
        a given index might have to add  sList to the arguments then use `and  selection not in sList.get(0, tk.END)`"""

    selection = adrList.get(adrList.curselection())

    if selection not in  dList.get(0, tk.END):
        
        dList.insert (tk.END, selection)
        dAdrList.append(selection)

        print(dAdrList)
   
def remove_delete(dList, dAdressList):

    """This function is simply for  removing an item from the delete list."""
    
    index = dList.curselection()
    selection = dList.get(index)

    dList.delete(index)
    dAdressList.remove(selection)

    print(dAdressList)
    

def to_sort_list(adrList, sList):
    selection = adrList.get(adrList.curselection())

    if selection not in  sList.get(0, tk.END):
    
        sList.insert (tk.END, selection)
    

def remove_sort(sList):

    index = sList.curselection()

    sList.delete(index)

def delete_mail(server, num, adrs, dList):

    if adrs in str(dList):

        server.store(num, '+FLAGS', '\\DELETED')
        
        print("Message Deleted ftom " + adrs)

        
def sort_emails(sList):
    pass

def login(usr, pswd):

    global user, password

    user = usr.get()

    password = pswd.get()

    usr.delete(0, tk.END)
    pswd.delete(0, tk.END)
    
def check_mail(user, pswd, dList):

    """Need to figure out if there is a way to make this work faster and maybe set it up to fetch all the addresses
        as soon as the person has logged into their email."""

    print(datetime.datetime.now())  

    mailServer = imaplib.IMAP4_SSL('imap.gmail.com')
    
    mailServer.login(user, pswd)

    mailServer.select('INBOX')

    typ, data = mailServer.search(None, 'All')

    for num in data[0].split():
        
        #append our header data to a list. 
                           
        #headers.append(get_header(mailServer, num))
        

        #Fetch the raw data from our emails 
        result, data = mailServer.fetch(num, '(BODY[HEADER])')
        
        rawBytes = email.message_from_bytes(data[0][1])

        #bodies.append(get_body(rawBytes))
        email_from = str(email.header.make_header(email.header.decode_header(rawBytes['From'])))
        
        address = seperate_address(email_from)

            
        if address in dList:
            delete_mail(mailServer,  num, address, dList)

    mailServer.close()

    mailServer.logout()

    print(datetime.datetime.now())   
    
class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("MailBot")

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky='nsew')        

        #This dictionary will contain all of our frame objects that represent
        #different pages of the GUI 
        self.frames = {}

        #for loop iterates through all of the frames below and stores the
        #objects value in self.frame 
        for F in (HomePage, PageTwo, PageThree):

            self.frame = F(self.container, self)

            #we add into our dictionary so that the frames container can be
            #accessed from the show_frame() method
            self.frames[F] = self.frame

            self.frame.grid(row=0, column=0, sticky='nsew')

        #We call our show_frame() method and give it the page we want to start
        #with as an argument
        self.show_frame(HomePage)

    def show_frame(self, cont):
        """the show_frame method can be with the page you want to display as
           the argument."""

        frame = self.frames[cont]

        frame.tkraise()

class HomePage(tk.Frame):

    """Our HomePage will be the where our application starts out there will be a menu to navigate our application.
        I want to add a sign in menu to our home page so our user can sign in when the app is launched.`"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.userLabel = tk.Label(self, text='Email:')
        self.userLabel.grid(row=0, column=0)

        self.userEntry = tk.Entry(self)
        self.userEntry.grid(row=0, column=1)

        self.passwordLabel = tk.Label(self, text='Password:')
        self.passwordLabel.grid(row=1, column=0,)

        self.passwordEntry = tk.Entry(self, show='*')
        self.passwordEntry.grid(row=1, column=1)

        self.loginBtn = tk.Button(self, text='Login',  command=lambda:  login(self.userEntry, self.passwordEntry))
        self.loginBtn.grid(row=0, column=2, rowspan=2, padx=2, pady=2)

        self.pageTwo = tk.Button(self, text='Manage Emails', command=lambda: controller.show_frame(PageTwo))
        self.pageTwo.grid(row=2, column=0, padx=2, pady=2, columnspan=2)

       # self.pageThree = tk.Button(self, text='Page 3', width=10, command=lambda: controller.show_frame(PageThree))
       #self.pageThree.grid(row=0, column=1, padx=2, pady=2)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.getAdrressBtn = tk.Button(self,text='Get Addresses', command=lambda: get_mail(user, password, addresses, self.addressBox))
        self.getAdrressBtn.grid(row=0, column=0, padx=2, pady=2)

        self.addressScroll = tk.Scrollbar(self)
        self.addressScroll.grid(row=1, column=1, sticky='nsw')
        
        self.addressBox = tk.Listbox(self, yscrollcommand=self.addressScroll.set, width=50)
        self.addressBox.grid(row=1, column=0, padx=2, pady=2)

        self.addressScroll.config(command = self.addressBox.yview)

        self.addToDeleteBtn = tk.Button(self, text='To Delete', command=lambda: to_delete_list(self.addressBox, deleteList, self.deleteBox))
        self.addToDeleteBtn.grid(row=3, column=2, padx=2, pady=2)

        self.removeFromDeleteBtn = tk.Button(self, text='Remove', command=lambda: remove_delete(self.deleteBox,deleteList))
        self.removeFromDeleteBtn.grid(row=3, column=3,  padx=2, pady=2)

        self.deleteButton = tk.Button(self, text='Delete Selected', command=lambda: check_mail(user, password, deleteList))
        self.deleteButton.grid(row=4, column=2, columnspan=2)

        self.delLbl = tk.Label(self, text='Delete by Address')
        self.delLbl.grid(row=2,  column=0)

        self.delScroll = tk.Scrollbar(self)
        self.delScroll.grid(row=3, column=1, sticky='nsw')
        
        self.deleteBox = tk.Listbox(self, yscrollcommand=self.delScroll.set, width=50)
        self.deleteBox.grid(row=3, column=0, padx=2, pady=2)

        self.delScroll.config(command = self.deleteBox.yview)

        self.sortScroll = tk.Scrollbar(self)
        self.sortScroll.grid(row=5, column=1, sticky='nsw')

        self.sortLbl = tk.Label(self, text='Sort by Address')
        self.sortLbl.grid(row=4,  column=0)

        self.addToSortBtn = tk.Button(self, text='To Sort', command=lambda: to_sort_list(self.addressBox, self.sortBox))
        self.addToSortBtn.grid(row=5, column=2,  padx=2, pady=2)

        self.removeFromSortBtn = tk.Button(self, text='Remove',  command=lambda: remove_sort(self.sortBox))
        self.removeFromSortBtn.grid(row=5, column=3,  padx=2, pady=2)

        self.sortBox = tk.Listbox(self, yscrollcommand=self.sortScroll.set, width=50)
        self.sortBox.grid(row=5, column=0, padx=2, pady=2)

        self.sortScroll.config(command = self.sortBox.yview)

        self.homeButton = tk.Button(self,text='Home', command=lambda: controller.show_frame(HomePage))
        self.homeButton.grid(row=6, column=0, padx=2, pady=2)
            
           
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.homeButton = tk.Button(self,text='Home', command=lambda: controller.show_frame(HomePage))
        self.homeButton.grid(row=0, column=0, padx=2, pady=2)
               
app = MyApp()
app.mainloop()

