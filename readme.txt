1.
The program consists of an ATM Interface: atmMachine.py is the main module.
It is able to create and handle several bank accounts, allowing the user to
view their balance, deposit/withdraw money (virtually), view their transaction history
and change their PIN Code.
The user must first create their account through a dedicated window and, upon
successful completion of the process, he/she will be assigned an ID number for 
logging into the system, along with a 4-digit PIN code of his/her choice.
The program stores account data in .pickle files, from which a database could be created.

2.
Abdul wrote the numPad module, worked on its implementation into the main
program, and contributed to debugging and exception handling. 
Anavir designed and coded the bankAccount module and some of the algorithms 
and functions to treat the omonimous class in the GUI (e.g. deposit/withdraw, change Pin).
Fabio coded the GUI, with the related functions needed to navigate between windows
and handle the main events, and dealt with the storage of data in files through the pickle module.

3.
The program has some limitations. The numberPad is not able to input values into
the entry field on focus, and is instead assigned to a single entry field per window.
It also cannot delete inserted numbers from entry fields. Also, the two blank
buttons input a string two spaces long into fields.
Finally, attempting to withdraw money when the resulting balance would be less
than the allowed limit (-$1000), correctly returns user to action page, but does
not show "Insufficient funds" error message. 
Resolving these issues would be our primary focus for future development. 
Other aspects would include the implementation of new functions, 
like wire transfers bewteen different bank accounts, and making
the interface more graphically appealing to the average user.
