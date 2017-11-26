# Testing Documentation
# https://www.bluepay.com/developers/testing/

# Complete API Documentation
# https://www.bluepay.com/sites/default/files/documentation/BluePay_bp10emu/BluePay%201-0%20Emulator.txt

"""
Our main program that processes credit card transactions
"""

#from tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from BluePay import *
from DB import *

# creating a database to store all Transaction details.
db = Database("transaction_information.db")

# Class that constructs an interface to process credit cards and 
class Processor(tk.Frame):
    #data = []
    #newData = []
    #inFile = ""
    # Class constructor for the application interface
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    #  Function to construct the main application interface 
    def initUI(self):
        self.menubar = tk.Menu(self.parent)    # create a toplevel menu
        self.parent.config(menu= self.menubar)  # display the menu
        self.parent.geometry('700x500')
        self.parent.title("Credit Card Processor")
        self.imagePath = tk.PhotoImage(file="creditcards.gif")

        self.w = tk.Label(self.parent, image=self.imagePath).pack()

        self.tx = tk.Label(self.parent, text="Credit card Processing Module", font=('Cabria', 30, 'bold'), bg="black", fg="white" ).pack(expand = True, fill=tk.BOTH)
        self.tx1 = tk.Label(self.parent, text=" Please select an appropriate function by clicking on the button", font=('Cabria', 18)).pack(expand = True, fill=tk.BOTH)
  
        self.button1 = tk.Button(self.parent, width = 16, text="Charge Credit Card", font=('Cabria', 18, 'bold'), command=self.charge_UI).pack(padx=5, pady=5)
        self.button2 = tk.Button(self.parent, width = 16, text="Refund", font=('Cabria', 18, 'bold'),activeforeground='blue', command=self.refund_UI).pack(padx=5, pady=5)
        self.button3 = tk.Button(self.parent, width = 16, text="Void", font=('Cabria', 18, 'bold'), command=self.void_UI).pack(padx=5, pady=5)
        self.button5 = tk.Button(self.parent, width = 16, text="Manage Transactions", font=('Cabria', 18, 'bold'), command=self.transaction_manager).pack(padx=5, pady=5)
        self.button4 = tk.Button(self.parent, width = 16, text="QUIT", font=('Cabria', 18, 'bold'), command=self.parent.quit).pack(padx=10, pady=10)
        # create a pulldown menu, and add it to the menu bar
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)

        self.fileMenu.add_command(label="Charge/Process", command=self.charge_UI)
        self.fileMenu.add_command(label="Refund", command=self.refund_UI)
        self.fileMenu.add_command(label="Void", command=self.void_UI)
        self.fileMenu.add_command(label="Manage Transactions", command=self.transaction_manager)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="Credit Card Transactions", menu=self.fileMenu)

        # create more pulldown menus
        self.helpMenu = tk.Menu(self.menubar, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.About)
        self.menubar.add_cascade(label="Help", menu=self.helpMenu) 

        self.txt = tk.Label(self.parent)
        self.txt.pack(fill=tk.BOTH, expand=True)

    # Function to show Appliation details in a popup
    def About(self):
        messagebox.showinfo("About", "   Credit Card Processor \n Developed by: Bharath Ogety and Vipul Rana\n Version: 1.0 ")

    # Function to build and interface to interact with the SQLlite database which stores all transactions
    def transaction_manager(self):
        # creating a new window
        self.custWindow = tk.Toplevel(self.parent)
        self.custWindow.geometry('850x350')
        self.custWindow.title("Manage Transactions")
        
        #creating labels for the entry fields
        self.l1 = tk.Label(self.custWindow, text="Full Name", font=('Cabria', 16))
        self.l1.grid(row=1, column=0)

        self.l2 = tk.Label(self.custWindow, text="Transaction Type", font=('Cabria', 16))
        self.l2.grid(row=1, column=2)

        self.l3 = tk.Label(self.custWindow, text="Amount", font=('Cabria', 16))
        self.l3.grid(row=2, column=0)

        self.l4 = tk.Label(self.custWindow, text="Status", font=('Cabria', 16))
        self.l4.grid(row=2, column=2)

        self.l5 = tk.Label(self.custWindow, text="Transaction ID", font=('Cabria', 16))
        self.l5.grid(row=3, column=0)

        # creating entry fields
        self.full_name_text = tk.StringVar()
        self.e1 = tk.Entry(self.custWindow, textvariable=self.full_name_text)
        self.e1.grid(row=1, column=1)

        self.trans_type_text = tk.StringVar()
        self.e2 = tk.Entry(self.custWindow, textvariable=self.trans_type_text)
        self.e2.grid(row=1, column=3)

        self.amount_text = tk.StringVar()
        self.e3 = tk.Entry(self.custWindow, textvariable=self.amount_text)
        self.e3.grid(row=2, column=1)

        self.status_text = tk.StringVar()
        self.e4 = tk.Entry(self.custWindow, textvariable=self.status_text)
        self.e4.grid(row=2, column=3)

        self.trans_id_text = tk.StringVar()
        self.e5 = tk.Entry(self.custWindow, textvariable=self.trans_id_text)
        self.e5.grid(row=3, column=1)

        # creating a listbox to display the data retrieved fromt the database in a interactable manner
        # inspired from https://stackoverflow.com/questions/8647735/tkinter-listbox
        self.list1 = tk.Listbox(self.custWindow, height=10, width=55)
        self.list1.grid(row=4, column=0, rowspan=8, columnspan=4)
        self.list1.bind("<<ListboxSelect>>", self.get_selected_row)

        # creating a scrollbar for the list box
        self.sc = tk.Scrollbar(self.custWindow)
        self.sc.grid(row=4, column=3, rowspan=8)
        self.list1.configure(yscrollcommand=self.sc.set)
        self.sc.configure(command=self.list1.yview)

        # creating buttons to perform database operations like Add, remove, update
        self.b1 = tk.Button(self.custWindow, text="View all", width=12, font=('Cabria', 16), command=self.view_command)
        self.b1.grid(row=4, column=4)

        self.b2 = tk.Button(self.custWindow, text="Search entry", width=12, font=('Cabria', 16), command=self.search_command)
        self.b2.grid(row=5, column=4)

        self.b3 = tk.Button(self.custWindow, text="Add entry", width=12, font=('Cabria', 16), command=self.add_command)
        self.b3.grid(row=6, column=4)

        self.b4 = tk.Button(self.custWindow, text="Update selected", width=12, font=('Cabria', 16), command=self.update_command)
        self.b4.grid(row=7, column=4)

        self.b5 = tk.Button(self.custWindow, text="Delete selected", width=12, font=('Cabria', 16), command=self.delete_command)
        self.b5.grid(row=8, column=4)

        self.b6 = tk.Button(self.custWindow, text="Clear", width=12, font=('Cabria', 16), command=self.clearValue_trans)
        self.b6.grid(row=9, column=4)

        self.b8 = tk.Button(self.custWindow, text="Refund", width=10,font=('Cabria', 16, 'bold'), command=self.refund_UI1)
        self.b8.grid(row=14, column=1)

        self.b9 = tk.Button(self.custWindow, text="Void", width=10,font=('Cabria', 16, 'bold'), command=self.void_UI1)
        self.b9.grid(row=14, column=2)

        self.b7 = tk.Button(self.custWindow, text="Close", width=10, font=('Cabria', 16, 'bold'), command=self.custWindow.destroy)
        self.b7.grid(row=14, column=3)


    # Build a from to process a Sale transaction    
    def charge_UI(self):
        self.chargeWindow = tk.Toplevel(self.parent)
        self.chargeWindow.geometry('560x250')
        self.chargeWindow.title("Process a Credit card Charge")

        tk.Label (self.chargeWindow, text = "Full Name: ", font=('Cabria', 16)).grid (row=1, sticky=tk.E)
        tk.Label (self.chargeWindow, text = "Amount to Charge in $: ", font=('Cabria', 16)).grid (row=2, sticky=tk.E)
        tk.Label (self.chargeWindow, text = "Credit Card Number: ", font=('Cabria', 16)).grid (row=3, sticky=tk.E)
        tk.Label (self.chargeWindow, text = "Expiration Date(MM/YY): ", font=('Cabria', 16)).grid (row=4, sticky=tk.E)
        tk.Label (self.chargeWindow, text = "Security Code (CCV): ", font=('Cabria', 16)).grid (row=5, sticky=tk.E)
        self.fullName_charge = tk.Entry(self.chargeWindow)
        self.chargeAmount_charge = tk.Entry(self.chargeWindow)
        self.cardNumber_charge = tk.Entry(self.chargeWindow)
        self.expirationDate_charge = tk.Entry(self.chargeWindow)
        self.ccv_charge = tk.Entry(self.chargeWindow)
      
        self.fullName_charge.grid (row=1, column=1)
        self.chargeAmount_charge.grid (row=2, column=1)
        self.cardNumber_charge.grid (row=3, column=1)
        self.expirationDate_charge.grid (row=4, column=1)
        self.ccv_charge.grid (row=5, column=1)

        self.submit_charge = tk.Button(self.chargeWindow, width = 12, text="Charge now!", font=('Cabria', 16, 'bold'), command=self.chargeSubmit).grid(row=5, column=4)
        self.close_charge = tk.Button(self.chargeWindow, width = 12, text="Close",font=('Cabria', 16, 'bold'), command=self.chargeWindow.destroy).grid(row=6, column=4)
        
        self.demo1_charge = tk.Button(self.chargeWindow, width = 12, text="Demo- Success", font=('Cabria', 16), command=self.demoSale_Success).grid(row=2, column=4)
        self.demo2_charge = tk.Button(self.chargeWindow, width = 12, text="Demo- Decline", font=('Cabria', 16),command=self.demoSale_Failure).grid(row=3, column=4)
        self.clearButton_charge = tk.Button(self.chargeWindow, width = 12, text="Clear", font=('Cabria', 16), command=self.clearValue_charge).grid(row=4, column=4)
        
    # Demo info to test a Successful sale Transaction
    def demoSale_Success(self):
        self.fullName_charge.delete(0,tk.END)
        self.fullName_charge.insert(0,"Test Success")
        self.chargeAmount_charge.delete(0,tk.END)
        self.chargeAmount_charge.insert(0,"5.00")
        self.cardNumber_charge.delete(0,tk.END)
        self.cardNumber_charge.insert(0,"4111111111111111")
        self.expirationDate_charge.delete(0,tk.END)
        self.expirationDate_charge.insert(0,"1219")
        self.ccv_charge.delete(0,tk.END)
        self.ccv_charge.insert(0,"123")

    # Demo info to test a Failed sale Transaction
    def demoSale_Failure(self):
        self.fullName_charge.delete(0,tk.END)
        self.fullName_charge.insert(0,"Test Failure")
        self.chargeAmount_charge.delete(0,tk.END)
        self.chargeAmount_charge.insert(0,"4.00")
        self.cardNumber_charge.delete(0,tk.END)
        self.cardNumber_charge.insert(0,"4111111111111111")
        self.expirationDate_charge.delete(0,tk.END)
        self.expirationDate_charge.insert(0,"1219")
        self.ccv_charge.delete(0,tk.END)
        self.ccv_charge.insert(0,"123")

    # Demo info to test a Successful Refund Transaction
    def demoRefund_Success(self):
        self.fullName_refund.delete(0,tk.END)
        self.fullName_refund.insert(0,"Test Success")
        self.chargeAmount_refund.delete(0,tk.END)
        self.chargeAmount_refund.insert(0,"5.00")
        self.transactonID_refund.delete(0,tk.END)
        self.transactonID_refund.insert(0,"")
    
    # Demo info to test a Failed Refund Transaction
    def demoRefund_Failure(self):
        self.fullName_refund.delete(0,tk.END)
        self.fullName_refund.insert(0,"Test Failure")
        self.chargeAmount_refund.delete(0,tk.END)
        self.chargeAmount_refund.insert(0,"4.00")
        self.transactonID_refund.delete(0,tk.END)
        self.transactonID_refund.insert(0,"")
 
    # clear all fields in the charge form
    def clearValue_charge(self):
        self.fullName_charge.delete(0,tk.END)
        self.cardNumber_charge.delete(0,tk.END)
        self.chargeAmount_charge.delete(0,tk.END)
        self.expirationDate_charge.delete(0,tk.END)
        self.ccv_charge.delete(0,tk.END)
        #self.chargeWindow.destroy()

    # clear all fields in the refund form
    def clearValue_refund(self):
        self.fullName_refund.delete(0,tk.END)
        self.transactonID_refund.delete(0,tk.END)
        self.chargeAmount_refund.delete(0,tk.END)
    
    # clear all fields in the void form
    def clearValue_void(self):
        self.fullName_void.delete(0,tk.END)
        self.transactonID_void.delete(0,tk.END)
        self.chargeAmount_void.delete(0, tk.END)
    
    # clear all fields in the transaction manager form
    def clearValue_trans(self):
        self.list1.select_clear(0,tk.END)
        self.list1.delete(0, tk.END)
        self.full_name_text.set("")
        self.trans_type_text.set("")
        self.amount_text.set("")
        self.status_text.set("")
        self.trans_id_text.set("")
        
    # Reads info entered in the UI and talks to Payment Gateway API to get an approval
    def chargeSubmit(self):
        #print(self.entry)
        account_id = '100426906084'
        secret_key = 'FM1LU6NJ2XCLTCEUNWPCK7TJLUZLXTKQ' 
        mode = 'Test'

        # checking Authorization API using the credentials
        payment = BluePay(
            account_id = account_id, 
            secret_key = secret_key, 
            mode = mode
        ) 

        # making an object to pass to information to the API
        payment.set_customer_information(
            name1 = self.fullName_charge.get(),
            name2 = "",
            addr1 = "",
            addr2 = "",
            city = "",
            state = "",
            zipcode = "",
            country = ""
        )

        payment.set_cc_information(
            card_number = self.cardNumber_charge.get(), # setting credit card #
            card_expire = self.expirationDate_charge.get(), # setting expiration date
            cvv2 = self.ccv_charge.get() # setting security code
        )
        payment.sale(amount = self.chargeAmount_charge.get()) # setting charge amount
        # Makes the API Request
        payment.process()

        # Read response from BluePay
        if payment.is_successful_response():
            global db
            db.insert(self.fullName_charge.get(), "CHARGE", self.chargeAmount_charge.get(), payment.status_response, payment.trans_id_response)
            self.chargeWindow.destroy()
            messagebox.showinfo("Transaction Status",
                'Transaction Status: ' + payment.status_response+ '\n'+
                'Transaction Message: ' + payment.message_response+ '\n'+
                'Transaction ID: ' + payment.trans_id_response + '\n'+
                'AVS Result: ' + payment.avs_code_response + '\n'+
                'CVV2 Result: ' + payment.cvv2_code_response + '\n'+
                'Masked Payment Account: ' + payment.masked_account_response+ '\n'+
                'Card Type: ' + payment.card_type_response + '\n'+
                'Auth Code: ' + payment.auth_code_response
            )
        else:
            messagebox.showinfo("Transaction Status","Failed: "+ payment.message_response)

    # Builds a form to process a refund transaction
    def refund_UI(self):
        self.refundWindow = tk.Toplevel(self.parent)
        self.refundWindow.geometry('560x230')
        self.refundWindow.title("Process a refund")

        tk.Label (self.refundWindow, text = "Full Name: ", font=('Cabria', 16)).grid (row=1, sticky=tk.E)
        tk.Label (self.refundWindow, text = "Amount to Refund in $: ", font=('Cabria', 16)).grid (row=2, sticky=tk.E)
        tk.Label (self.refundWindow, text = "Transaction ID: ", font=('Cabria', 16)).grid (row=3, sticky=tk.E)
   
        self.fullName_refund = tk.Entry(self.refundWindow)
        self.chargeAmount_refund = tk.Entry(self.refundWindow)
        self.transactonID_refund = tk.Entry(self.refundWindow)

        self.fullName_refund.grid (row=1, column=1)
        self.chargeAmount_refund.grid (row=2, column=1)
        self.transactonID_refund.grid (row=3, column=1)
        
        self.demo1_refund = tk.Button(self.refundWindow, width = 12, text="Demo- Success", font=('Cabria', 16), command=self.demoRefund_Success).grid(row=1, column=4)
        self.demo2_refund = tk.Button(self.refundWindow, width = 12, text="Demo- Decline", font=('Cabria', 16),command=self.demoRefund_Failure).grid(row=2, column=4)
        self.clearButton_refund = tk.Button(self.refundWindow, width = 12, text="Clear", font=('Cabria', 16), command=self.clearValue_refund).grid(row=3, column=4)

        self.submit_refund = tk.Button(self.refundWindow, width = 12, text="Refund now!", font=('Cabria', 16, 'bold'), command=self.refundSubmit).grid(row=4, column=4)
        self.close_refund = tk.Button(self.refundWindow, width = 12, text="Close", font=('Cabria', 16, 'bold'), command=self.refundWindow.destroy).grid(row=5, column=4)

    # Builds a form to process a refund transaction
    def refund_UI1(self):
        self.refundWindow = tk.Toplevel(self.parent)
        self.refundWindow.geometry('560x230')
        self.refundWindow.title("Process a refund")

        tk.Label (self.refundWindow, text = "Full Name: ", font=('Cabria', 16)).grid (row=1, sticky=tk.E)
        tk.Label (self.refundWindow, text = "Amount to Refund in $: ", font=('Cabria', 16)).grid (row=2, sticky=tk.E)
        tk.Label (self.refundWindow, text = "Transaction ID: ", font=('Cabria', 16)).grid (row=3, sticky=tk.E)
   
        self.fullName_refund = tk.Entry(self.refundWindow)
        self.chargeAmount_refund = tk.Entry(self.refundWindow)
        self.transactonID_refund = tk.Entry(self.refundWindow)

        self.fullName_refund.grid (row=1, column=1)
        self.chargeAmount_refund.grid (row=2, column=1)
        self.transactonID_refund.grid (row=3, column=1)
        
        self.demo1_refund = tk.Button(self.refundWindow, width = 12, text="Demo- Success", font=('Cabria', 16), command=self.demoRefund_Success).grid(row=1, column=4)
        self.demo2_refund = tk.Button(self.refundWindow, width = 12, text="Demo- Decline", font=('Cabria', 16),command=self.demoRefund_Failure).grid(row=2, column=4)
        self.clearButton_refund = tk.Button(self.refundWindow, width = 12, text="Clear", font=('Cabria', 16), command=self.clearValue_refund).grid(row=3, column=4)

        self.submit_refund = tk.Button(self.refundWindow, width = 12, text="Refund now!", font=('Cabria', 16, 'bold'), command=self.refundSubmit).grid(row=4, column=4)
        self.close_refund = tk.Button(self.refundWindow, width = 12, text="Close", font=('Cabria', 16, 'bold'), command=self.refundWindow.destroy).grid(row=5, column=4)

        self.fullName_refund.insert(0, self.full_name_text.get())
        self.chargeAmount_refund.insert(0, self.amount_text.get())
        self.transactonID_refund.insert(0, self.trans_id_text.get())
    

    # Reads info entered in the UI and talks to Payment Gateway API to get an approval
    def refundSubmit(self):
        account_id = '100426906084'
        secret_key = 'FM1LU6NJ2XCLTCEUNWPCK7TJLUZLXTKQ'
        mode = 'Test'

        payment_return = BluePay(
            account_id = account_id, # Merchant's Account ID
            secret_key = secret_key, # Merchant's Secret Key
            mode = mode # Transaction Mode: TEST (can also be LIVE)
        )

        # Creates a refund transaction against previous sale
        payment_return.refund(
            #transaction_id = payment.trans_id_response, # id of the transaction to refund
            transaction_id = self.transactonID_refund.get(),
            amount = self.chargeAmount_refund.get() # partial refund of $1.75
        )

        # Makes the API Request for processing the return transaction
        payment_return.process()

        # Read response from BluePay
        if payment_return.is_successful_response():
            global db
            db.insert(self.fullName_refund.get(), "REFUND", self.chargeAmount_refund.get(), payment_return.status_response, payment_return.trans_id_response)
            self.refundWindow.destroy()
            messagebox.showinfo("Transaction Status",
                'Transaction Status: ' + payment_return.status_response+ '\n'+
                'Transaction Message: ' + payment_return.message_response+ '\n'+
                'Transaction ID: ' + payment_return.trans_id_response + '\n'+
                'AVS Result: ' + payment_return.avs_code_response + '\n'+
                'CVV2 Result: ' + payment_return.cvv2_code_response + '\n'+
                'Masked Payment Account: ' + payment_return.masked_account_response+ '\n'+
                'Card Type: ' + payment_return.card_type_response + '\n'+
                'Auth Code: ' + payment_return.auth_code_response
            )
        else:
            messagebox.showinfo("Transaction Status","Failure Notice: "+ payment_return.message_response)


    # Builds a form to void a transaction
    def void_UI1(self):
        # if self.voidWindow.state() == 'normal':
        #    print("Again")
        #    self.voidWindow.focus_set()
        #else:    
        self.voidWindow = tk.Toplevel(self.parent)
        self.voidWindow.geometry('560x230')
        self.voidWindow.title("Void a transaction")

        tk.Label (self.voidWindow, text = "Full Name: ", font=('Cabria', 16)).grid (row=1, sticky=tk.E)
        tk.Label (self.voidWindow, text = "Transaction ID: ", font=('Cabria', 16)).grid (row=2, sticky=tk.E)
        tk.Label (self.voidWindow, text = "Amount in $: ", font=('Cabria', 16)).grid (row=3, sticky=tk.E)

        self.fullName_void = tk.Entry(self.voidWindow)
        self.transactonID_void = tk.Entry(self.voidWindow)
        self.chargeAmount_void = tk.Entry(self.voidWindow)

        self.fullName_void.grid (row=1, column=1)
        self.transactonID_void.grid (row=2, column=1)
        self.chargeAmount_void.grid (row=3, column=1)
        
        #self.demo1_void = tk.Button(self.voidWindow, width = 12, text="Demo- Success", font=('Cabria', 16), command=self.voidWindow.destroy).grid(row=1, column=4)
        #self.demo2_void = tk.Button(self.voidWindow, width = 12, text="Demo- Decline", font=('Cabria', 16), command=self.voidWindow.destroy).grid(row=2, column=4)
        self.clearButton_void = tk.Button(self.voidWindow, width = 12, text="Clear", font=('Cabria', 16), command=self.clearValue_void).grid(row=3, column=4)
        
        self.submit_void = tk.Button(self.voidWindow, width = 12, text="Void now!", font=('Cabria', 16, 'bold'), command=self.voidSubmit).grid(row=4, column=4)
        self.close_void = tk.Button(self.voidWindow, width = 12, text="Close", font=('Cabria', 16, 'bold'), command=self.voidWindow.destroy).grid(row=5, column=4)

        self.transactonID_void.insert(0, self.trans_id_text.get())
        self.fullName_void.insert(0, self.full_name_text.get())
        self.chargeAmount_void.insert(0, self.amount_text.get())

    # Builds a form to void a transaction
    def void_UI(self):
        # if self.voidWindow.state() == 'normal':
        #    print("Again")
        #    self.voidWindow.focus_set()
        #else:    
        self.voidWindow = tk.Toplevel(self.parent)
        self.voidWindow.geometry('500x300')
        self.voidWindow.title("Void a transaction")

        tk.Label (self.voidWindow, text = "Full Name: ", font=('Cabria', 16)).grid (row=1, sticky=tk.E)
        tk.Label (self.voidWindow, text = "Transaction ID: ", font=('Cabria', 16)).grid (row=2, sticky=tk.E)
        tk.Label (self.voidWindow, text = "Amount in $: ", font=('Cabria', 16)).grid (row=3, sticky=tk.E)

        self.fullName_void = tk.Entry(self.voidWindow)
        self.transactonID_void = tk.Entry(self.voidWindow)
        self.chargeAmount_void = tk.Entry(self.voidWindow)

        self.fullName_void.grid (row=1, column=1)
        self.transactonID_void.grid (row=2, column=1)
        self.chargeAmount_void.grid (row=3, column=1)
        
        #self.demo1_void = tk.Button(self.voidWindow, width = 12, text="Demo- Success", font=('Cabria', 16), command=self.voidWindow.destroy).grid(row=1, column=4)
        #self.demo2_void = tk.Button(self.voidWindow, width = 12, text="Demo- Decline", font=('Cabria', 16), command=self.voidWindow.destroy).grid(row=2, column=4)
        self.clearButton_void = tk.Button(self.voidWindow, width = 12, text="Clear", font=('Cabria', 16), command=self.clearValue_void).grid(row=3, column=4)
        
        self.submit_void = tk.Button(self.voidWindow, width = 12, text="Void now!", font=('Cabria', 16, 'bold'), command=self.voidSubmit).grid(row=4, column=4)
        self.close_void = tk.Button(self.voidWindow, width = 12, text="Close", font=('Cabria', 16, 'bold'), command=self.voidWindow.destroy).grid(row=5, column=4)

    # Reads info entered in the UI and talks to Payment Gateway API to void a transaction
    def voidSubmit(self):
        account_id = "100426906084"
        secret_key = "FM1LU6NJ2XCLTCEUNWPCK7TJLUZLXTKQ"
        mode = "TEST"

        payment = BluePay(
            account_id = account_id,
            secret_key = secret_key,
            mode = mode
        )

        payment_cancel = BluePay(
            account_id=account_id,  # Merchant's Account ID
            secret_key=secret_key,  # Merchant's Secret Key
            mode=mode  # Transaction Mode: TEST (can also be LIVE)
        )

        # Finds the previous payment by ID and attempts to void it
        #payment_cancel.void(payment.trans_id_response)
        #test = self.transactonID_void
        payment_cancel.void(self.transactonID_void.get())


        # Makes the API Request to void the payment
        payment_cancel.process()

        # If transaction was approved..
        if payment_cancel.is_successful_response():
            global db
            db.insert(self.fullName_void.get(), "VOID", self.chargeAmount_void.get(), payment_cancel.status_response, payment_cancel.trans_id_response)
            self.voidWindow.destroy()
            messagebox.showinfo("Transaction Status",
                'Transaction Status: ' + payment_cancel.status_response+ '\n'+
                'Transaction Message: ' + payment_cancel.message_response+ '\n'+
                'Transaction ID: ' + payment_cancel.trans_id_response + '\n'+
                'AVS Result: ' + payment_cancel.avs_code_response + '\n'+
                'CVV2 Result: ' + payment_cancel.cvv2_code_response + '\n'+
                'Masked Payment Account: ' + payment_cancel.masked_account_response+ '\n'+
                'Card Type: ' + payment_cancel.card_type_response + '\n'+
                'Auth Code: ' + payment_cancel.auth_code_response
            )
        else:
            messagebox.showinfo("Transaction Status","Failure Notice: "+ payment_cancel.message_response)

    # populate all the data from the database into the list box
    def view_command(self):
        global db
        self.list1.delete(0, tk.END)
        for row in db.view():
            self.list1.insert(tk.END, row)

    # Function to query the Transactions database and retireves the information found into the listbox
    def search_command(self):
        global db
        self.list1.delete(0, tk.END)
        for row in db.search(self.full_name_text.get(), self.trans_type_text.get(), self.amount_text.get(), self.status_text.get(), self.trans_id_text.get()):
            self.list1.insert(tk.END, row)

    # Function to create a new transaction record
    def add_command(self):
        global db
        db.insert(self.full_name_text.get(), self.trans_type_text.get(), self.amount_text.get(), self.status_text.get(), self.trans_id_text.get())
        self.view_command()

    # Function to remove a transaction from the database
    def delete_command(self):
        global db
        db.delete(self.get_selected_row()[0])
        self.view_command()

    # Function to update any transaction related details
    def update_command(self):
        global db
        db.update(cur_id, self.full_name_text.get(), self.trans_type_text.get(), self.amount_text.get(), self.status_text.get(), self.trans_id_text.get())
        self.view_command()

    # Function to return the selcted record data from the listbox
    def get_selected_row(self,vent=None):
        global cur_id
        self.index = self.list1.curselection()[0]
        self.selected_tuple = self.list1.get(self.index)
        cur_id = self.selected_tuple[0]

        self.e1.delete(0, tk.END)
        self.e1.insert(tk.END, self.selected_tuple[1])

        self.e2.delete(0, tk.END)
        self.e2.insert(tk.END, self.selected_tuple[2])

        self.e3.delete(0, tk.END)
        self.e3.insert(tk.END, self.selected_tuple[3])

        self.e4.delete(0, tk.END)
        self.e4.insert(tk.END, self.selected_tuple[4])

        self.e5.delete(0, tk.END)
        self.e5.insert(tk.END, self.selected_tuple[5])

        return self.selected_tuple
            

# main function to create a class instance
def main():
    root = tk.Tk()
    ex = Processor(root)
    root.mainloop()  

# if the file is called directly then only run the main 
if __name__ == '__main__':
    main()