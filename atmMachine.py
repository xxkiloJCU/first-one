# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 22:01:37 2018

@author: PC
"""

from tkinter import *
from bankAccount import bankAccount
from numPad import numberPad
import pickle
import time
import random

widget = None

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        numPad = Label(self)
        self.switchFrame(loginPage, numPad)
        
        # Used to switch between windows.
        # All switch functions must pass numPad to the loading function
        # so that the latter can destroy it. This is to avoid double pads.
    def switchFrame(self, frame_class, numPad):       
        newFrame = frame_class(self)
        self.loadNewFrame(newFrame, numPad)
        
        # Same as switchFrame, but passes an argument to the new window.
        # Used to pass the account object around, so that new window
        # can access the methods of the bankAccount class
    def switchFrameArgument(self, frame_class, arg, numPad):       
        newFrame = frame_class(self, arg)
        self.loadNewFrame(newFrame, numPad)
        
        # Same as switchFrame, but passes three arguments to new window
        # Used to pass account object, amount to withdraw/deposit and a dummy
        # value to allow ATM to distinguish withdraw/deposit after PinCheck
    def switchFrameThreeArguments(self, frame_class, arg1, arg2, arg3, numPad):
        newFrame = frame_class(self, arg1, arg2, arg3)
        self.loadNewFrame(newFrame, numPad)
    
        # Used by switchFrame functions to load he new frame into parent window.
        # It destroys the current frame and replaces it with the new one.
    def loadNewFrame(self, frame, numPad):
        if self._frame is not None:
            self._frame.destroy()
        numPad.destroy()
        self._frame = frame
        self._frame.grid(row = 1, column = 1, pady = 40)


class loginPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        # Variables for user entries
        self.entryID = StringVar()
        self.entryPIN = StringVar()
        self.master = master
        
        # Login page widgets
        welcomeLabel = Label(self, text = "Welcome to Bank of JCU ATM")
        idLabel = Label(self, text = "Account ID: ")
        pinLabel = Label(self, text = "PIN: ")
        nameEntry = Entry(self, textvariable = self.entryID)
        self.pinEntry = Entry(self, textvariable = self.entryPIN, show = "•")
        padLabel = Label(self, text = "                ")
        dateTime = Label(self, text = time.strftime('%m/%d/%Y %H:%M'))
        self.wrongInputMsg = Message(self, fg = "Red", text = None, width = 500)
        
        # Login button
        loginButton = Button(self, text = "Login", 
                command = self.accountLogin)
        
        newUserButton = Button(self, text = "New User",
               command = lambda: master.switchFrame(createAccountPage, self.numPad))
        
        # Place widgets into Frame
        dateTime.grid(row = 1, column = 1, columnspan = 3, padx = 10, sticky = E)
        welcomeLabel.grid(row = 2, column = 1, pady = 50, columnspan = 3)
        idLabel.grid(row = 3, column = 1, padx = 50, sticky = "E")
        pinLabel.grid(row = 4, column = 1,padx = 50, sticky = "E")
        nameEntry.grid(row = 3, column = 2, sticky = "W")
        self.pinEntry.grid(row = 4, column = 2, sticky = "W")
        padLabel.grid(row = 6, column =  3, pady = 10)
        loginButton.grid(row = 5, column = 2)
        newUserButton.grid(row = 7, column = 3)
        self.wrongInputMsg.grid(row = 6, column = 1, columnspan = 3)
        
        #Create number pad
        self.numPad = numberPad(self.pinEntry)
        self.numPad.grid(row = 8, column = 1, columnspan = 3)
        
    def accountLogin(self):
        try:
            account = self.getAccount()
            self.master.switchFrameArgument(actionPage, account, self.numPad)
            
        except(FileNotFoundError, SyntaxError, NameError, AttributeError):
            
            self.wrongInputMsg["text"] = "Incorrect ID/Pin. Try again"
        
    def getAccount(self):
        infile = open(self.entryID.get() + ".pickle", "rb")
        account = pickle.load(infile)
        infile.close()
        
        if eval(self.entryPIN.get()) == account.getPinCode():
            return account
    
        else:
            return "Error"
            

class createAccountPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        # Declare input variables
        self.firstName = StringVar()
        self.lastName = StringVar()
        self.sex = IntVar()
        self.master = master
        self.phoneN = StringVar()
        self.pin = StringVar()
        self.pinConfirm = StringVar()
        
        # Create widgets
        firstName = Label(self, text = "First Name: ")
        enterFirst = Entry(self, textvariable = self.firstName)
        lastName = Label(self, text = "Last Name: ")
        enterLast = Entry(self, textvariable = self.lastName)
        mfLabel = Label(self, text = "Sex: ")
        rbMale = Radiobutton(self, text = "Male",
            variable = self.sex, value = 1)
        rbFemale = Radiobutton(self, text = "Female",
            variable = self.sex, value = 2)
        birthDate = Label(self, text = "Date of birth: ")
        enterPhone = Entry(self, width = 18, textvariable = self.phoneN)
        padLabel = Label(self, text = " ")
        pinLabel = Label(self, text = "Create PIN: ")
        enterPin = Entry(self, textvariable = self.pin, show = "•", width = 7)
        confirmPin = Label(self, text = "Re-Enter PIN: ")
        phoneNumber = Label(self, text = "Phone: ")
        enterConfirm = Entry(self, textvariable = self.pinConfirm, show = "•", width = 7)
        lengthPin = Label(self, text = "4-digit code", fg = "Grey")
        self.errorMsg = Message(self, text = None, fg = "Red", width = 500)
        self.successMsg = Message(self, text = None, fg = "Green", width = 500)
        self.yourIDMsg = Message(self, text = None, fg = "Green", width = 500)
        
        
        # Create account and exit buttons
        createButton = Button(self, text = "Create account",
                             command = self.createAccount)
        exitButton = Button(self, text = "Exit",
               command = self.exitPage)

        # Create number pad
        self.numPad = numberPad(enterPin)
        self.numPad.grid(row = 8, column = 1, columnspan = 5)
        
        #Place objects in Frame
        firstName.grid(row = 1, column = 1)
        enterFirst.grid(row = 1, column = 2)
        lastName.grid(row = 2, column = 1)
        enterLast.grid(row = 2, column = 2)
        mfLabel.grid(row = 1, column = 3, padx = 5, sticky = E)
        rbMale.grid(row = 1, column = 4)
        rbFemale.grid(row = 1, column = 5)
        phoneNumber.grid(row = 2, column = 3, padx = 5, sticky = E)
        enterPhone.grid(row = 2, column = 4, columnspan = 2, sticky = W)
        padLabel.grid(row = 3, column = 1, pady = 10)
        pinLabel.grid(row = 5, column = 1)
        enterPin.grid(row = 5, column = 2, sticky = W)
        confirmPin.grid(row = 6, column = 1)
        enterConfirm.grid(row = 6, column = 2, sticky = W)
        createButton.grid(row = 7, column = 1, pady = 10, columnspan = 2)
        exitButton.grid(row = 7, column = 5, sticky = E)
        lengthPin.grid(row = 5, column = 2, sticky = E)
        self.errorMsg.grid(row = 7, column = 2, columnspan = 4)
        self.successMsg.grid(row = 5, column = 3, rowspan = 2, columnspan = 2)
        
        
    def createAccount(self):
        try:
            if self.checkBlankField() == True:
                self.errorMsg["text"] = "Please fill all fields." 
        
            elif len(self.pin.get()) == 4 and len(self.pinConfirm.get()) == 4:
                if self.pin.get() == self.pinConfirm.get():
                    newAccount = bankAccount(self.generateID(), self.firstName.get(),
                    self.lastName.get(), self.sex.get(), 0, 
                    self.phoneN.get(), eval(self.pin.get()))
        
                    outfile = open(newAccount.getUserID() + ".pickle", "wb")
                    pickle.dump(newAccount, outfile)
                    outfile.close()
                    
                    # Transaction list starts with 6 empty values to avoid problems
                    # in history view when fewer than 6 transactions have occurred.
                    transactList = [None, None, None, None, None, None]
                    outfile2 = open(newAccount.getUserID() + "-T" + ".pickle", "wb")
                    pickle.dump(transactList, outfile2)
                    
                    self.successMsg["text"] = "Account created!\n" \
                    + "Your ID is: " + newAccount.getUserID()
                    self.errorMsg["text"] = ""
            
                else:
                    letterCheck = eval(self.pin.get()) + eval(self.pinConfirm.get())
                    self.errorMsg["text"] = "Error: PINs do not match!"
                    self.successMsg["text"] = ""
                
            
            else:
                ltCheck = eval(self.pin.get()) + eval(self.pinConfirm.get())
                self.errorMsg["text"] = "Error: PIN must have 4 digits."
                
        except(NameError, SyntaxError):
            self.errorMsg["text"] = "Error: PIN must be a number."
    
    def checkBlankField(self):
        if self.firstName.get() == '':
            return True
        
        elif self.lastName.get() == '':
            return True
        
        elif self.sex.get() == 0:
            return True
        
        elif self.phoneN.get() == '':
            return True
        
        elif self.pin.get() == '':
            return True
        
        elif self.pinConfirm.get() == '':
            return True
        
        else:
            return False
    
    def exitPage(self):
        self.master.switchFrame(loginPage, self.numPad)
    
    def generateID(self):
        ID = self.firstName.get()[0] + self.lastName.get()[0]\
        + str(random.randint(100, 999))
        return ID


class actionPage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        self.master = master
        
        # Welcome label and options
        clientLabel = Label(self, text = account.getTitle() + " " + 
            account.getOwnerLastName() + ", what would you like to do today?")
        
        dateTime = Label(self, text = time.strftime('%m/%d/%Y %H:%M'))
        ghostEntry = Entry(self)
        
        balanceBt = Button(self, text = "Balance",
                command = lambda: self.gotoBalance(account, self.numPad))
        transactionBt = Button(self, text = "Transaction",
                command = lambda: self.gotoTransaction(account, self.numPad))
        settingsBt = Button(self, text = "Manage account",
                command = lambda: self.gotoManage(account, self.numPad))
        
        logoutBt = Button(self, text = "Log out",
                command = lambda: self.logOut(loginPage, self.numPad))
        
        # Place widgets in Frame
        balanceBt.grid(row = 3, column = 2, pady = 10)
        transactionBt.grid(row = 3, column = 3, pady = 10)
        settingsBt.grid(row = 3, column = 4, pady = 10)
        clientLabel.grid(row = 2, column = 1, 
                    columnspan = 4, padx = 50, pady = 20)
        dateTime.grid(row = 1, column = 4)
        logoutBt.grid(row = 4, column = 4, sticky = E, pady = 10)
        
        #Creates number pad
        self.numPad = numberPad(ghostEntry)
        self.numPad.grid(row = 5, column = 1, columnspan = 4)

    def gotoBalance(self, account, numPad):
        self.master.switchFrameArgument(balancePage, account, self.numPad)
    
    def gotoManage(self, account, numPad):
        self.master.switchFrameArgument(managePage, account, self.numPad)
        
    def gotoTransaction(self, account, numPad):
        self.master.switchFrameArgument(transactionPage, account, self.numPad)
        
    def logOut(self, page, numPad):
        self.master.switchFrame(loginPage, self.numPad)


class balancePage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        self.master = master
        amt = account.getBalance()
        
        balanceLabel = Label(self, text = "Your current balance is: ")
        ghostEntry = Entry(self)
        self.amount = Message(self, text = "$ " + str(amt), width = 500)
        backBt = Button(self, text = "Back", 
                        command = lambda: self.goBack(account, self.numPad))
        
        if amt > 0:
            self.amount["fg"] = "Green"
        
        elif amt < 0:
            self.amount["fg"] = "Red"
        
        balanceLabel.grid(row = 1, column = 1, padx = 80, pady = 10, columnspan = 2)
        self.amount.grid(row = 2, column = 1, columnspan = 2)
        backBt.grid(row = 3, column = 2, pady = 10)
        
        #Create number pad
        self.numPad = numberPad(ghostEntry)
        self.numPad.grid(row = 8, column = 1, columnspan = 5)
        
    def goBack(self, account, numPad):
        self.master.switchFrameArgument(actionPage, account, self.numPad)
        

class transactionPage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        self.master = master
        
        ghostEntry = Entry(self)
        depositBt = Button(self, text = "Deposit",
                command = lambda: self.gotoDeposit(account, self.numPad), width = 10, height = 10)
        withdrawBt = Button(self, text = "Withdraw",
                command = lambda: self.gotoWithdraw(account, self.numPad), width = 10, height = 10)
        
        depositBt.grid(row = 1, column = 1, padx = 50, pady = 50)
        withdrawBt.grid(row = 1, column = 2, padx = 50, pady = 50)
        
        self.numPad = numberPad(ghostEntry)
        self.numPad.grid(row = 8, column = 1, columnspan = 5)
    
    def gotoDeposit(self, account, numPad):
        self.master.switchFrameArgument(depositPage, account, self.numPad)
    
    def gotoWithdraw(self, account, numPad):
        self.master.switchFrameArgument(withdrawPage, account, self.numPad)
        

class depositPage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        self.amount = StringVar()
        self.master = master
        
        howMuch = Label(self, text = "How much would you\nlike to deposit?")
        dollarSign = Label(self, text = "$")
        amountEntry = Entry(self, textvariable = self.amount)
        nextBt = Button(self, text = "Next",
                    command = lambda: self.gotoPinCheck(account, self.numPad))
        
        
        howMuch.grid(row = 1, column = 1, columnspan = 2, padx = 50, pady = 20)
        dollarSign.grid(row = 2, column = 1, sticky = E)
        amountEntry.grid(row = 2, column = 2, sticky = W)
        nextBt.grid(row = 3, column = 2)
        
        # Create numpad
        self.numPad = numberPad(amountEntry)
        self.numPad.grid(row = 8, column = 1, columnspan = 5)
        
    def gotoPinCheck(self, account, numPad):
        self.master.switchFrameThreeArguments(pinCheckWindow,
                            account, eval(self.amount.get()), 1, self.numPad)
        
class withdrawPage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        self.amount = IntVar()
        self.master = master
        
        ghostEntry = Entry()
        howMuch = Label(self, text = "How much would you\nlike to withdraw?")
        tenDollars = Radiobutton(self, text = "$ 10",
                                variable = self.amount, value = 10)
        twentyDollars = Radiobutton(self, text = "$ 20", 
                                variable = self.amount, value = 20)
        fiftyDollars = Radiobutton(self, text = "$ 50", 
                                variable = self.amount, value = 50)
        onehundredDollars = Radiobutton(self, text = "$100",
                                variable = self.amount, value = 100)
        twohundredDollars = Radiobutton(self, text = "$200", 
                                variable = self.amount, value = 200)
        fivehundredDollars = Radiobutton(self, text = "$500",
                                variable = self.amount, value = 500)
        
        nextBt = Button(self, text = "Next",
                    command = lambda: self.gotoPinCheck(account, self.numPad))
        
        howMuch.grid(row = 1, column = 1, padx = 80, pady = 20, columnspan = 2)
        tenDollars.grid(row = 2, column = 1)
        twentyDollars.grid(row = 3, column = 1)
        fiftyDollars.grid(row = 4, column = 1)
        onehundredDollars.grid(row = 2, column = 2)
        twohundredDollars.grid(row = 3, column = 2)
        fivehundredDollars.grid(row = 4, column = 2)
        nextBt.grid(row = 5, column = 2)
        
        #Creates number pad
        self.numPad = numberPad(ghostEntry)
        self.numPad.grid(row = 6, column = 1, columnspan = 2)
        
        
    def gotoPinCheck(self, account, numPad):
        self.master.switchFrameThreeArguments(pinCheckWindow,
                                account, self.amount.get(), 0, self.numPad)   
        
class pinCheckWindow(Frame):
    def __init__(self, master, account, amount, mode):
        Frame.__init__(self, master)
        self.account = account
        self.amount = amount
        self.pinInput = StringVar()
        self.master = master
        self.attempts = 0
        
        insertLabel = Label(self, text = "Please insert your PIN Code")
        pinEntry = Entry(self, textvariable = self.pinInput, show = "•")
        confirmBt = Button(self, text = "Confirm", 
                    command = lambda: self.processConfirmBt(mode, self.numPad))
        
        self.errorMsg = Message(self, text = "", fg = "Red", width = 500)
        
        insertLabel.grid(row = 1, column = 1, padx = 50)
        pinEntry.grid(row = 2, column = 1, padx = 50, pady = 10)
        confirmBt.grid(row = 3, column = 1, padx = 50, pady = 10)
        self.errorMsg.grid(row = 4, column = 1, padx = 50)
        
        self.numPad = numberPad(pinEntry)
        self.numPad.grid(row = 5, column = 1)
        

    def processConfirmBt(self, mode, numPad):
        try:    
            userInput = eval(self.pinInput.get())
            if self.attempts <= 2:
                if self.account.pinCheck(userInput) == True:
                    if mode == 0:
                        if self.account.getBalance() - self.amount >= -1000:
                            self.account.withdrawMoney(self.amount)
                            transactList = self.getHistory()
                            newTransaction = time.strftime('%m/%d/%Y %H:%M') + "     " + "- $" + str(self.amount)
                            transactList.append(newTransaction)
                            self.saveAccount(transactList)
                            self.master.switchFrameThreeArguments(transactionEndWindow,
                                    self.account, self.amount, 0, self.numPad)
                        
                        else:
                            self.errorMsg["text"] = "Insufficient funds."
                            time.sleep(2)
                            self.goBack(actionPage, self.account, self.numPad)
                            
                            
                    else:
                        self.account.depositMoney(self.amount)
                        transactList = self.getHistory()
                        newTransaction = time.strftime('%m/%d/%Y %H:%M') + "     " + "+ $" + str(self.amount)
                        transactList.append(newTransaction)
                        self.saveAccount(transactList)
                        self.master.switchFrameThreeArguments(transactionEndWindow,
                                    self.account, self.amount, 1, self.numPad)

                else:
                    self.attempts += 1
                    errorMessage = "Wrong Pin." + " " + str(3 - self.attempts) + " attempts left"
                    self.errorMsg["text"] = errorMessage
        
            else:
                self.master.switchFrame(loginPage, self.numPad)
        
        except(NameError, SyntaxError):
            self.attempts += 1
            errorMessage = "Wrong Pin." + " " + str(3 - self.attempts) + " attempts left"
            self.errorMsg["text"] = errorMessage
            
    def getHistory(self):
         infile = open(self.account.getUserID() + "-T" + ".pickle", "rb")
         transactList = pickle.load(infile)
         infile.close()
         
         return transactList
     
    def goBack(self, actionPage, account, numPad):
        self.master.switchFrameArgument(actionPage, account, self.numPad)
        
    def saveAccount(self, transactList):
        outfile = open(self.account.userID + ".pickle", "wb")
        pickle.dump(self.account, outfile)
        outfile.close()
        
        outfile2 = open(self.account.getUserID() + "-T" + ".pickle", "wb")
        pickle.dump(transactList, outfile2)
        outfile.close()

                
class transactionEndWindow(Frame):
    def __init__(self, master, account, amount, mode):
        Frame.__init__(self, master)
        self.master = master
        
        if mode == 0:
            withdrawText = "You have withdrawn $" + str(amount)
            thankLabel= Label(self, text = withdrawText)
        else:
            depositText = "You have deposited $" + str(amount)
            thankLabel = Label(self, text = depositText)
         
        ghostEntry = Entry(self)
        balanceLabel = Label(self, 
                text = "Your current balance is $" + str(account.getBalance()))
        
        otherOperation = Label(self, text = "Perform another operation?")
        yesBt = Button(self, text = "Yes", 
            command = lambda: self.processYesBt(actionPage, account, self.numPad))
        noBt = Button(self, text = "No",
            command = lambda: self.processNoBt(loginPage, self.numPad))
            
        # Place widgets into Frame
        thankLabel.grid(row = 1, column = 1, padx = 80, columnspan = 2)
        balanceLabel.grid(row = 2, column = 1, columnspan = 2)
        otherOperation.grid(row = 3, column = 1, columnspan = 2, pady = 20)
        yesBt.grid(row = 4, column = 1)
        noBt.grid(row = 4, column = 2)
        
        #Creates number pad
        self.numPad = numberPad(ghostEntry)
        self.numPad.grid(row = 5, column = 1, columnspan = 2)


    def processYesBt(self, page, account, numPad):
        self.master.switchFrameArgument(actionPage, account, self.numPad)
        
    def processNoBt(self, page, numPad):
        self.master.switchFrame(loginPage, self.numPad)


class managePage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        self.master = master
        
        ghostEntry = Entry(self)
        changePinBt = Button(self, text = "Change\nPin",
                command = lambda: self.gotoPinChange(account, self.numPad), width = 10, height = 10)
        movlistBt = Button(self, text = "Transaction\nHistory",
                command = lambda: self.gotoHistory(account, self.numPad), width = 10, height = 10)
        
        changePinBt.grid(row = 1, column = 1, padx = 50, pady = 50)
        movlistBt.grid(row = 1, column = 2, padx = 50, pady = 50)
        
        #Creates number pad
        self.numPad = numberPad(ghostEntry)
        self.numPad.grid(row = 2, column = 1, columnspan = 2)
    
    def gotoPinChange(self, account, numPad):
        self.master.switchFrameArgument(changePinWindow, account, self.numPad)
    
    def gotoHistory(self, account, numPad):
        self.master.switchFrameArgument(historyPage, account, self.numPad)


class changePinWindow(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        
        #Declare input variables
        self.account = account
        self.phoneInput = StringVar()
        self.master = master
        self.newPin = StringVar()
        self.confirmNewPin = StringVar()
        
        #Create widgets
        phoneLabel = Label(self, text = "Input your phone number:")
        newPinLabel = Label(self, text = "Choose a new PIN:")
        confirmNewPin = Label(self, text = "Re-enter new PIN:")
        phoneEntry = Entry(self, textvariable = self.phoneInput)
        newPinEntry = Entry(self, textvariable = self.newPin, show = "•")
        confirmPinEntry = Entry(self, textvariable = self.confirmNewPin, show = "•" )
        changePinBt = Button(self, text = "Change PIN", 
                command = lambda: self.processChangePinBt(account))
        backBt = Button(self, text = "Back", width = 6,
                command = lambda: self.goBack(actionPage, account, self.numPad))
        self.errorMsg = Message(self, text = None, fg = "Red", width = 500)
        self.successMsg = Message(self, text = None, fg = "Green", width = 500)
        
        
        # Place widgets in window
        phoneLabel.grid(row = 1, column = 1, padx = 8)
        newPinLabel.grid(row = 2, column = 1, padx = 8)
        confirmNewPin.grid(row = 3, column = 1, padx = 8)
        phoneEntry.grid(row = 1, column = 2, padx = 8)
        newPinEntry.grid(row = 2, column = 2, padx = 8)
        confirmPinEntry.grid(row = 3, column = 2)
        changePinBt.grid(row = 6, column = 2, sticky = W)
        backBt.grid(row = 6, column = 2, sticky = E)
        self.errorMsg.grid(row = 4, column = 2)
        self.successMsg.grid(row = 5, column = 2)
        
        self.numPad = numberPad(newPinEntry)
        self.numPad.grid(row = 7, column = 1, columnspan = 2)
        
    def processChangePinBt(self, account):
        try:
            if self.checkBlankField() == True:
                self.errorMsg["text"] = "Please fill all fields." 
        
            elif len(self.newPin.get()) == 4 and len(self.confirmNewPin.get()) == 4:
                if self.phoneInput.get() == account.getPhoneNumber():
                    if self.newPin.get() == self.confirmNewPin.get():
                        account.changePinCode(eval(self.newPin.get()))
                        self.saveAccount(account)
                        self.successMsg["text"] = "PIN change successful!"
                        self.errorMsg["text"] = ""
                        
                    else:
                        letterCheck = eval(self.newPin.get()) + eval(self.confirmNewPin.get())
                        self.errorMsg["text"] = "Error: PINs don't match!"
                        self.successMsg["text"] = ""
            
                else:
                    letterCheck = eval(self.newPin.get()) + eval(self.confirmNewPin.get())
                    self.errorMsg["text"] = "Error: Incorrect Phone"
                    self.successMsg["text"] = ""
                
            
            else:
                ltCheck = eval(self.newPin.get()) + eval(self.confirmNewPin.get())
                self.errorMsg["text"] = "Error: PIN must have 4 digits."
                
        except(NameError, SyntaxError):
            self.errorMsg["text"] = "Error: PIN must be a number."
    
    def checkBlankField(self):
        if  self.phoneInput.get() == '':
            return True
        
        elif self.newPin.get() == '':
            return True
        
        elif self.confirmNewPin.get() == '':
            return True
        
        else:
            return False
        
    def goBack(self, actionPage, account, numPad):
        self.master.switchFrameArgument(actionPage, account, self.numPad)
        
    def saveAccount(self, account):
        outfile = open(account.getUserID() + ".pickle", "wb")
        pickle.dump(account, outfile)
        outfile.close()  
    
    
class historyPage(Frame):
    def __init__(self, master, account):
        Frame.__init__(self, master)
        
        # Variables are declared
        self.master = master
        self.account = account
        self.transactList = self.getHistory()
        
        ghostLabel = Label(self)
        backBt = Button(self, text = "Back",
            command = lambda: self.goBack(actionPage, account, self.numPad))
        backBt.grid(row = 7, column = 4, padx = 60, sticky = W )
        
        # Create number pad
        self.numPad = numberPad(ghostLabel)
        self.numPad.grid(row = 8, column = 1, columnspan = 3, padx = 80, sticky = E)
        
        # Creates labels that display last 6 transactions
        listRange = range(len(self.transactList) - 6, len(self.transactList))
        for i, j in zip(listRange, listRange):
            transactLabel = Label(self, text = self.getTransaction(i))
            transactLabel.grid(row = 1 + j, column = 1, columnspan = 3)
    
    def goBack(self, actionPage, account, numPad):
        self.master.switchFrameArgument(actionPage, account, self.numPad)

    def getHistory(self):
         infile = open(self.account.getUserID() + "-T" + ".pickle", "rb")
         transactList = pickle.load(infile)
         infile.close()
         
         return transactList

    
    def getTransaction(self, position):
        return self.transactList[position]
        
        
if __name__ == "__main__":
    app = SampleApp()
    app.title("JCU ATM Machine 1.0")
    app.mainloop()