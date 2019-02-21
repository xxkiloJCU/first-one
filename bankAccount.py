# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:09:50 2018

@author: fsemeraro
"""

class bankAccount:
    def __init__(self, userID, ownerFirstName, ownerLastName, ownerSex, begBalance, phoneNumber, pinCode):
        self.balance = begBalance
        self.ownerFirstName = ownerFirstName
        self.ownerLastName = ownerLastName
        self.ownerSex = ownerSex
        self.phoneNumber = phoneNumber
        self.pinCode = pinCode
        self.userID = userID

    def changePinCode(self, newPinCode):
        self.pinCode = newPinCode
    
    def depositMoney(self, amount):
        self.balance = self.balance + amount
    
    def getBalance(self):
        return self.balance
    
    def getOwnerFirstName(self):
        return self.ownerFirstName
    
    def getOwnerLastName(self):
        return self.ownerLastName
    
    def getPhoneNumber(self):
        return self.phoneNumber
    
    def getPinCode(self):
        return self.pinCode
    
    def getTitle(self):
        if self.ownerSex == 1:
            return "Mr."
        
        else:
            return "Ms."
        
    def getUserID(self):
        return self.userID
        
    def pinCheck(self, pinInput):
        if pinInput == self.pinCode:
            return True
        
        else:
            return False
        
    def withdrawMoney(self, amount):
        self.balance = self.balance - amount