from tkinter import *
from tkinter import messagebox
import socket
import threading

def main(x):
    global HOST, PORT, connectButton, messageBox, userDisplay, root # VAriables that can be used anywhere within the program
    root = Tk()
    root.title("Client")
    username = x # Username that is received from Login
    # TOP frame of GUI
    topFrame = Frame(root)
    nameLabel = Label(topFrame, text = f"Name: {username}").pack(side=LEFT)
    connectButton = Button(topFrame, text="Connect", command=lambda : connect(username))
    connectButton.pack(side=LEFT)
    topFrame.pack(side=TOP)
    # Frame that displays mesages received
    displayFrame = Frame(root)
    sep = Label(displayFrame, text="*********************************************************************").pack()
    scrollBar = Scrollbar(displayFrame)
    scrollBar.pack(side=RIGHT, fill=Y)
    userDisplay = Text(displayFrame, height=20, width=55)
    userDisplay.pack(side=LEFT, fill=Y, padx=(5, 0))
    userDisplay.tag_config("tag_your_message")
    scrollBar.config(command=userDisplay.yview)
    userDisplay.config(yscrollcommand=scrollBar.set, highlightbackground="grey", state="disabled")
    displayFrame.pack(side=TOP)
    # Frame that allows user to input data
    bottomFrame = Frame(root)
    messageBox = Text(bottomFrame, height=2, width=55)
    messageBox.pack(side=LEFT, padx=(5, 13), pady=(5, 10))
    messageBox.config(highlightbackground="grey", state="disabled")
    messageBox.bind("<Return>", (lambda event: getMessage(messageBox.get("1.0", END))))
    bottomFrame.pack(side=BOTTOM)

    # network client
    HOST = "127.0.0.1" # Server IP address
    PORT = 8080 # server PORT

    root.mainloop() # Run GUI in LOOP

def connect(name):
    global client
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set up client
        client.connect((HOST, PORT)) # Connect client to server
        client.send(name.encode('utf-8')) # Send name to server after connecting

        connectButton.config(state=DISABLED)
        messageBox.config(state=NORMAL)

        threading._start_new_thread(receiveMessage, (client, "m")) # Thread to keep receiving messages while program is running
    except Exception as e: # Show error if server is down or not reachable but don't close program
        messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST + " on port: " + str(PORT) + " Server may be Unavailable. Try again later")


def receiveMessage(conn, m):
    while True: # Infinite loop
        from_server = conn.recv(4096).decode('utf-8') # Receive message from server

        if not from_server: # If the server is not connected close program
            break

        texts = userDisplay.get("1.0", END).strip()
        userDisplay.config(state=NORMAL)
        # display message from server on the chat window
        if len(texts) < 1:
            userDisplay.insert(END, from_server)
        else:
            userDisplay.insert(END, "\n\n"+ from_server)

        userDisplay.config(state=DISABLED)
        userDisplay.see(END) # Always view the end of userDisplay by default

    conn.close()
    root.destroy()


def getMessage(msg):
    msg = msg.replace('\n', '')
    texts = userDisplay.get("1.0", END).strip()

    userDisplay.config(state=NORMAL)
    if len(texts) < 1:
        userDisplay.insert(END, "You->" + msg, "tag_your_message") # no line
    else:
        userDisplay.insert(END, "\n\n" + "You->" + msg, "tag_your_message")

    userDisplay.config(state=DISABLED)

    sendMessage(msg) # Calling function

    userDisplay.see(END)
    messageBox.delete('1.0', END)

def sendMessage(msg):
    client_msg = str(msg) # message is a string
    client.send(client_msg.encode('utf-8')) # Send message and encode it 
    print("Sending message")