import os
print("\n1. Run in CLI\n2. Run in WEB")

while True:
    choice = input("Enter your choice: ")
    if choice == '1':
        os.system('python lab1.py')
    elif choice == '2':
        os.system('python lab4.py')
