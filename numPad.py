# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 02:31:37 2018

@author: PC
"""

from tkinter import *


class numberPad(Frame):
    def __init__(self, widget):
        Frame.__init__(self)
        self.widget = widget
        
        keys = [
    ['1', '2', '3'],    
    ['4', '5', '6'],    
    ['7', '8', '9'],    
    ['  ', '0', '  '],]

  
        # Creates number pad buttons
        for y, row in enumerate(keys, 1):
            for x, key in enumerate(row):
                b = Button(self, text = key, command = lambda val = key:self.code(val, widget))
                b.grid(row=y, column=x, ipadx = 20, ipady = 20)
                
    def code(self, value, widget):
        widget.insert('end', value)