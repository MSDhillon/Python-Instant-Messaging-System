from tkinter import *
import socket
import threading

root = Tk()
root.title("Sever")

# Top frame showing the buttons to start and stop the server
topFrame = Frame(root)
connButton = Button(topFrame, text="Start", command=lambda : start_server())
connButton.pack(side=LEFT)
stopButton = Button(topFrame, text="Stop", command=lambda : stopServer(), state=DISABLED)
stopButton.pack(side=LEFT)
topFrame.pack(side=TOP, pady=(5, 0))

# Middle frame showing the host IP address along with the PORT
midFrame = Frame(root)
hostLabel = Label(midFrame, text = "Host: X.X.X.X")
hostLabel.pack(side=LEFT)
portLabel = Label(midFrame, text = "Port:XXXX")
portLabel.pack(side=LEFT)
midFrame.pack(side=TOP, pady=(5, 0))

# Server frame displays all the activities that are going on within the server
serFrame = Frame(root)
sep = Label(serFrame, text="********** Server **********").pack()
scrollBar = Scrollbar(serFrame)
scrollBar.pack(side=RIGHT, fill=Y)
serverDisplay = Text(serFrame, height=15, width=30)
serverDisplay.pack(side=LEFT, fill=Y, padx=(5, 0))
scrollBar.config(command=serverDisplay.yview)
serverDisplay.config(yscrollcommand=scrollBar.set, highlightbackground="grey", state="disabled")
serFrame.pack(side=LEFT, pady=(5, 10))

# Frame shows all clients that are offline
OffcliFrame = Frame(root)
sep2 = Label(OffcliFrame, text="********** Offline Clients **********").pack()
scrollBar2 = Scrollbar(OffcliFrame)
scrollBar2.pack(side=RIGHT, fill=Y)
userDisplay = Text(OffcliFrame, height=15, width=30)
userDisplay.pack(side=LEFT, fill=Y, padx=(5, 0))
scrollBar2.config(command=userDisplay.yview)
userDisplay.config(yscrollcommand=scrollBar2.set, highlightbackground="grey", state="disabled")
OffcliFrame.pack(side=RIGHT, pady=(5, 10))

# Frame shows all clients that are online
cliFrame = Frame(root)
sep2 = Label(cliFrame, text="********** Online Clients **********").pack()
scrollBar2 = Scrollbar(cliFrame)
scrollBar2.pack(side=RIGHT, fill=Y)
userDisplay2 = Text(cliFrame, height=15, width=30)
userDisplay2.pack(side=LEFT, fill=Y, padx=(5, 0))
scrollBar2.config(command=userDisplay2.yview)
userDisplay2.config(yscrollcommand=scrollBar2.set, highlightbackground="grey", state="disabled")
cliFrame.pack(side=RIGHT, pady=(5, 10))

HOST = '127.0.0.1' #socket.gethostbyname(socket.gethostname()) is a better way to get the host IP address
PORT = 8080
clientName = " "
clients = []
connClients = []


# Start server function
def start_server():
    connButton.config(state=DISABLED)
    stopButton.config(state=NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Setting up server

    server.bind((HOST, PORT)) # Bind the host and port
    server.listen(5)  # server is listening for client connection

    serverDisplay.config(state=NORMAL)
    serverDisplay.insert(END, '[RUNNING] Server is running...\n')
    serverDisplay.config(state=DISABLED)

    updateDisplay() # Calling a function

    threading._start_new_thread(acceptClients, (server, " ")) # Starting a new thread 

    # Update the HOST and PORT label in the middle frame
    hostLabel["text"] = "Host: " + HOST 
    portLabel["text"] = "Port: " + str(PORT)

# Stop server function
def stopServer():
    connButton.config(state=NORMAL)
    stopButton.config(state=DISABLED)

    serverDisplay.config(state=NORMAL)
    serverDisplay.insert(END, '[STOPPING] Server has stopped running.\n')
    serverDisplay.config(state=DISABLED)

# Function to accept new client connections
def acceptClients(conn, y):
    while True: # Infinite loop
        client, addr = conn.accept() # Accept connections and store their name and IP address
        clients.append(client) # Append the client connected name in the list

        serverDisplay.config(state=NORMAL)
        serverDisplay.insert(END, f'[CONNECTION] {addr} has connected to the server...\n')
        serverDisplay.config(state=DISABLED)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(exchangeMessages, (client, addr))

# Function to exchange messages between clients
def exchangeMessages(clientConn, client_ip_addr):
    clientMsg = " "

    # send welcome message to client
    clientName  = clientConn.recv(4096).decode('utf-8') # Receive name from client
    welcomeMsg = f"Welcome {clientName}." 
    clientConn.send(welcomeMsg.encode('utf-8')) # Send a welcome message to the client

    connClients.append(clientName) # Append name into connected clients list

    updateDisplay() # Calling a function

    while True: # Infinite loop
        data = clientConn.recv(4096).decode('utf-8') # receive data from client
        if not data: # If the data received is empty break from the loop
            break

        clientMsg = data

        index = getIndex(clients, clientConn) # calling the function to get index
        sendName = connClients[index]

        for c in clients: # For all clients in the clients list
            if c != clientConn: 
                serverMsg = str(sendName + "->" + clientMsg)
                c.send(serverMsg.encode('utf-8'))

                serverDisplay.config(state=NORMAL)
                serverDisplay.insert(END, f'[MESSAGE] {client_ip_addr} sent a message...\n')
                serverDisplay.config(state=DISABLED)

    # find the client index then remove from both lists
    index = getIndex(clients, clientConn)
    del connClients[index] # Delete the client with the index number from the connected client's list
    del clients[index] # Delete the client from the clients list

    # Server update 
    serverDisplay.config(state=NORMAL)
    serverDisplay.insert(END, f'[DISCONNECTION] {client_ip_addr} has disconnected...\n')
    serverDisplay.config(state=DISABLED)

    updateDisplay()

# Function to calculate the index of the client connected, allows with easy removal from list of user
def getIndex(connectedClients, currentClient):
    index = 0
    for conn in connectedClients: # Stay in loop for all connected clients in the client's list
        if conn == currentClient: # If the connected client is the current client return the index
            break
        index += 1

    return index

# Update the clients name from the frames when a client connects or disconnects inputting their name in the appropriate frame
def updateDisplay():
    database=open('Names.txt')
    userDisplay.config(state=NORMAL) # state needs to be set as normal in order to make changes
    userDisplay2.config(state=NORMAL)
    userDisplay.delete('1.0', END) # Delete everything within the frame
    userDisplay2.delete('1.0', END)
    for i in database: # For every name (i) in database run this loop
        a = i.strip() # Remove any spaces before or after the text
        if a in connClients: # if the name is within the clients connected list show name in conn clients frame
            userDisplay2.insert(END, a+'\n')
        if a not in connClients: # if name is not within the conn clients list show name in offline clients frame
            userDisplay.insert(END, a+'\n')
    userDisplay.config(state=DISABLED) # Disabled frames so the user cannot make changes
    userDisplay2.config(state=DISABLED)

root.mainloop() # Run the GUI in a loop