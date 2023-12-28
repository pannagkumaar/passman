from menu import menu, store, find, find_email, aesthetics
from encryption import generate_hash, check_hash
from database_manager import create_table,reset
from colorama import Style
import sys

aesthetics()
create_table()
generate_hash()
check,value=check_hash()
if not check:
    if value=="9":
        reset()
        generate_hash()
    else:    
        print(Style.RESET_ALL+"Wrong Password")
        sys.exit()
while True:
    choice = menu()
    if choice == "1":
        store()
    elif choice == "2":
        find()
    elif choice == "3":
        find_email()  
    elif choice.lower() == "q":
        print(Style.RESET_ALL)
        sys.exit("Exiting.....")
    else:
        print("-" * 40)
        print("Please enter a valid option")
        print("-" * 40)
