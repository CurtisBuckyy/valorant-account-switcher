#Valorant Account Switcher program created by Curtis Buckingham (https://github.com/CurtisBuckyy)

from tkinter import *
from tkinter import messagebox
import customtkinter
import os
import pathlib
import pyautogui
import time
from cryptography.fernet import Fernet
import psutil

root = customtkinter.CTk() # create CTk window like you do with the Tk window
root.title("Valorant Account Switcher") 
root.configure(background="#0c1824")
root.geometry("1200x785+360+147.5") #Sizing of application window and positioning to center of screen, assuming resolution is 1920x1080
root.resizable(False, False) #Making program un-resizable
root.iconbitmap("logo.ico") #Assigning icon to application window

#Setting Tk frames for GUI placement

frame = customtkinter.CTkFrame(master=root, corner_radius=5, fg_color="#0c1824")
frame.pack(side=LEFT, expand=True, fill=BOTH)

frameSeperator = customtkinter.CTkFrame(master=root, corner_radius=30, fg_color="white", width=2.5)
frameSeperator.pack(pady=80, side=LEFT, fill=BOTH)

frame2 = customtkinter.CTkFrame(master=root, corner_radius=5, fg_color="#0c1824")
frame2.pack(padx=30, pady=10, side=RIGHT, expand=True, fill=BOTH)

frame3 = customtkinter.CTkFrame(master=frame2, corner_radius=5, fg_color="#0c1824", width=200)

frame3.pack(fill="none", expand=True)

def grabKey(): 
    
    file = open('secret.key', 'rb')
    key = file.read()
    file.close()
    return key

def encrypyt(valorantPassword): #Encrypting Account Password

    key = grabKey()

    encoded = valorantPassword.encode()

    f = Fernet(key)

    valorantPassword = f.encrypt(encoded)

    return valorantPassword

def decrypt(password): #Decrypting Account Password

   key = grabKey()

   f2 = Fernet(key)

   decrypted = f2.decrypt(password.encode())

   password = decrypted.decode()

   return password

def readUsers():
     accountsList = []

     try: 
        for account in open("accounts.txt", "r").readlines():
            accountsList.append(account.split())

     except:
        open("accounts.txt", "w") #Creating accounts txt file if it doesn't exist

     return accountsList
     
def readAccounts():
        deleteOptionList.set("Delete account")

        #Accessing List Variables

        accountsList = readUsers()

        counter = 0

        accountNames = []

        for item in accountsList:
           accountNames.append(accountsList[counter][0])
           counter +=1

        accountsOptionList.configure(values=accountNames) #Appending accounts to combo box
        deleteOptionList.configure(values=accountNames) #Appending accounts to combo box

def importAccount():

    account_count = 0

    valorantUsername = usernameEntry.get()

    usernameList = []

    duplicateFlag = False

    for line in open("accounts.txt", "r").readlines():
           usernameList.append(line.split())
           account_count += 1 #Checking number of accounts
    
    for user in usernameList:
        if valorantUsername == user[0]:
            duplicateErrorLabel.configure(text="Username already taken, please input another.")
            duplicateErrorLabel.pack()
            accountCreatedLabel.configure(text="")
            deleteLabel.configure(text="")
            duplicateFlag = True
            return duplicateFlag

    if duplicateFlag != True:
        
        if account_count == 5: #Checking if number of accounts has reached the max of (5)
            errorLabel.pack()
            accountCreatedLabel.configure(text="")
            duplicateErrorLabel.configure(text="")
            errorLabel.configure(text="Max accounts of (5) created, please delete an account to Import.")
            
        else:
            valorantUsername = usernameEntry.get()
            valorantPassword = passwordEntry.get()

            encryptedValorantPassword = encrypyt(valorantPassword) #Calling function to encrypt account's Password

            duplicateErrorLabel.configure(text="")

            if len(valorantUsername) >= 3 and len(valorantUsername) <=16 and len(valorantPassword) >=8 and len(valorantPassword) <=30:

                with open('accounts.txt', 'ab') as accounts:
                    accounts.write(valorantUsername.encode())
                    accounts.write(" ".encode())
                    accounts.write(encryptedValorantPassword)
                    accounts.write(b"\n")
                    
                    accountCreatedLabel.configure(text="Account Name: '{}' Imported".format(valorantUsername))
                    accountCreatedLabel.pack()
                    deleteLabel.configure(text="")
                    
                    usernameEntry.configure(placeholder_text_color="white")
                    passwordEntry.configure(placeholder_text_color="white")

            else:
                usernameEntry.configure(placeholder_text_color="red")
                passwordEntry.configure(placeholder_text_color="red")

            readAccounts()
        

softwareLogo = PhotoImage(file = "logo.png")
softwareLogoLabel = Label(frame, image=softwareLogo, borderwidth=0)
softwareLogoLabel.pack(fill="none", expand=True)

infoLabel = customtkinter.CTkLabel(master=frame3, text="NOTE: Ensure that once an account is selected you do not touch the mouse or keyboard while the automation is in progress.", 
text_font =("Arial", -14), wraplength=400, text_color="red")
infoLabel.pack(pady=20)
    
usernameEntry = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter Username:", text_font =("Arial", -14,), width=200, 
height= 40, text_color="white", fg_color=("#343638", "#343638"))
usernameEntry.pack(pady=15)

passwordEntry = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter Password:", text_font =("Arial", -14), 
width=200, height= 40, text_color="white", fg_color=("#343638", "#343638"))
passwordEntry.pack(pady=10)

submitAccountButton = customtkinter.CTkButton(master=frame3, text="Import account", width=100, height = 50, command=importAccount, text_color="white")
submitAccountButton.pack(padx=20, pady=40)

accountCreatedLabel = customtkinter.CTkLabel(master=frame3, text="", text_font =("Arial", -14), text_color = "white")

errorLabel = customtkinter.CTkLabel(master=frame3, text="Max accounts of (5) created, please delete an account to Import.", text_font =("Arial", -14), text_color = "red")

deleteLabel = customtkinter.CTkLabel(master=frame3, text="", text_font =("Arial", -14), text_color = "white")

duplicateErrorLabel = customtkinter.CTkLabel(master=frame3, text="Username already taken, please input another.", text_font =("Arial", -14), text_color = "red")

def accountsOptionMenu_callback(choice):

    accountList = readUsers() 

    #Finding user in accountslist and grabbing the password 

    for account in accountList:

        if choice == account[0]:
            password = account[1]

    username = choice
    password = password

    decrypytedPassword = decrypt(password)
    
    loadAccount(username, decrypytedPassword) #Calling loadAccount function to launch with username and decrypted Password

accountsOptionList = customtkinter.CTkOptionMenu(master=frame3,values=[],command=accountsOptionMenu_callback, text_font =("Arial", -16), 
width = 100, height = 35, button_color="#fa4553", dropdown_text_font =("Arial", -14), dropdown_color=("#343638", "#343638"), dropdown_text_color="white", text_color="white")

accountsOptionList.pack(padx=20, pady=5)
accountsOptionList.set("Load account")  #Setting initial value

def deleteAccounts_callback(choice):
    
     deleteConfirmation = messagebox.askyesno("Delete Confirmation","Are you sure you wish to delete this account?") #Stores message box response from user

     if deleteConfirmation == 1:

        deleteLabel.configure("DELETED")

        updatedAccountList = []

        for line in open("accounts.txt", "r").readlines():
            updatedAccountList.append(line.split())

        accountCounter = 0

        for item in updatedAccountList:
            if choice == item[0]:
                    updatedAccountList.pop(accountCounter)
                    break

            accountCounter +=1

        open('accounts.txt', 'wb').close() #Clearing accounts.txt
 
        #Re-writing data back to file by appending existing accounts

        with open('accounts.txt', 'ab') as f:

            for item in updatedAccountList:
                f.write(item[0].encode())
                f.write("  ".encode())
                f.write(item[1].encode())
                f.write(b"\n")

        errorLabel.configure(text="")

        deleteLabel.pack()

        deleteLabel.configure(text="Account Name: '{}' Deleted".format(choice))

        accountCreatedLabel.configure(text="")

        duplicateErrorLabel.configure(text="")

        readAccounts()
      
deleteOptionList = customtkinter.CTkOptionMenu(master=frame3, values=["test"], command=deleteAccounts_callback, text_font =("Arial", -16),
 width = 100, height = 35, button_color="#fa4553", dropdown_text_font =("Arial", -14), dropdown_color=("#343638", "#343638"), dropdown_text_color="white", text_color="white")

deleteOptionList.pack(padx=20, pady=20)
deleteOptionList.set("Delete account:")  # Setting initial value

def loadAccount(username, decryptedPassword):
        
    #Grabbing Windows User Name and Path Drive Letter
    os_drive = pathlib.Path.home().drive
    windowsUserName = os.getlogin() #Grabbing Windows user name

    file_path = "{drive}/Users/{user}/AppData/Local/Riot Games/Riot Client/Data/RiotGamesPrivateSettings.yaml".format(drive = os_drive, user = windowsUserName)

    if os.path.isfile(file_path):
        os.remove(file_path)

    os.startfile(r"{drive}\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\valorant".format(user = windowsUserName, drive = os_drive))

    while True:
     programStatus = "RiotClientUx.exe" in (i.name() for i in psutil.process_iter()) #Checking if application is running before proceeding

     if programStatus == True:
        break

    time.sleep(5)
    pyautogui.write(username)
    pyautogui.press("tab")
    pyautogui.write(decryptedPassword)
    pyautogui.press("tab")
    time.sleep(3)

    for i in range(4):
        pyautogui.press("tab")

    pyautogui.press("enter")
    time.sleep(2)

    for i in range(5):
        pyautogui.press("tab")

    time.sleep(2)
    pyautogui.press("enter")

    accountsOptionList.set("Load Account")  #Setting initial value


readAccounts()

root.mainloop()
