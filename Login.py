from tkinter import *
from tkinter import messagebox
import hashlib
import Client

class Login:
    # MAIN PAGE
    def __init__(self, root):
        self.root=root
        self.root.title("Python Project")
        self.root.geometry("300x210")
        Label(text="Instant Messaging App", width="300", height="2", font=("Verdana", 13)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="20", command=self.login).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="20", command=self.register).pack()

    # REGISTRATION PAGE
    def register(self):
        self.root_v1=Toplevel(self.root)
        self.root_v1.title("Register")
        self.root_v1.geometry("300x250")
        # Username and password are String Variables
        self.username=StringVar()
        self.password=StringVar()

        Label(self.root_v1, text="Registration Form").pack()
        Label(self.root_v1, text="").pack()
        Label(self.root_v1, text="Username").pack()
        self.username_entry=Entry(self.root_v1, textvariable=self.username)
        self.username_entry.pack()
        Label(self.root_v1, text="Password").pack()
        self.password_entry=Entry(self.root_v1, textvariable=self.password, show="*")
        self.password_entry.pack()
        Label(self.root_v1, text="").pack()
        Button(self.root_v1, text="Register", width="10", height="2", command=self.registerUser).pack()

    # REGISTER THE USER
    def registerUser(self):
        # Get the username and hash it in order to store it in the database
        username_info=hashlib.sha256(self.username.get().encode("utf-8")).hexdigest()
        password_info=hashlib.sha256(self.password.get().encode("utf-8")).hexdigest()

        if username_info=="" or password_info=="": # If the fields are empty show error
            messagebox.showerror("Error", "Please input both Username & Password", parent=self.root_v1)
        else:
            database=open("Database.txt", "a") # Append data into the database
            database.write(username_info+", "+password_info+"\n")
            database.close()

            nameDatabase=open('Names.txt', 'a') # Create a new list with only the names of users
            nameDatabase.write(self.username.get()+'\n')
            nameDatabase.close()
            # Empty the fields
            self.username_entry.delete(0, END) 
            self.password_entry.delete(0, END)
            messagebox.showinfo("Congratulations", "Registration successful", parent=self.root_v1)
            self.root_v1.destroy() # Once the messagebox is showed, destroy the registration page

    # LOGIN PAGE
    def login(self):
        self.root_v2=Toplevel(self.root)
        self.root_v2.title("Login")
        self.root_v2.geometry("300x250")

        Label(self.root_v2, text="Login Form").pack()
        Label(self.root_v2, text="").pack()
        # The username and password are String Variables
        self.username_verify=StringVar()
        self.password_verify=StringVar()

        Label(self.root_v2, text="Username").pack() # .pack() is a geometry function, in this case puts the text in the middle of the root
        self.username_entry1=Entry(self.root_v2, textvariable=self.username_verify)
        self.username_entry1.pack()
        Label(self.root_v2, text="").pack() # Leave empty space
        Label(self.root_v2, text="Password").pack()
        self.password_entry1=Entry(self.root_v2, show="*", textvariable=self.password_verify)
        self.password_entry1.pack()
        Label(self.root_v2, text="").pack()
        Button(self.root_v2, text="Login", width="10", height="2", command=self.loginVerify).pack()

    # LOGIN VERIFICATION
    def loginVerify(self):
        # Get username and pasword inputted and hash it so it can be compared to the stored data
        username1=hashlib.sha256(self.username_verify.get().encode("utf-8")).hexdigest() 
        password1=hashlib.sha256(self.password_verify.get().encode("utf-8")).hexdigest() 
        x = self.username_verify.get() # get username so that it can be used in the clients program
        # Delete user entries
        self.username_entry1.delete(0, END)
        self.password_entry1.delete(0, END)

        database=open("Database.txt")
        # Create empty lists
        username_list=[]
        password_list=[]
        for i in database: # Splitting the data from the database
            a, b=i.split(", ") # Split where ', ' is located
            b=b.strip() # .strip() removes any spaces before the text
            username_list.append(a) # Append username into the empty list
            password_list.append(b) # Append password into the empty list
        database.close()
        if username1 in username_list and password1 in password_list: # If the username and password are in the list
            messagebox.showinfo("Congratulations", "Login Successful", parent=self.root_v2) # Show messagebox
            self.root_v2.destroy() # Destroy Login Page
            self.root.destroy()
            Client.main(x) # call main() function from client and pass the username
        else:
            messagebox.showerror("Error", "Username or Password wrong") # If username and password aren't in the list show error

if __name__ == '__main__':
    root=Tk()
    login=Login(root)
    root.mainloop()