from socket import *

#Both variables lastName and firstName refer to whoever is running or the author of this script
lastName = 'Ramirez'
firstName = 'Diana'

#Variable storing the email address of sender
sender_email = ''

#Variable storing the email address of recipient
rcpt_email = ''

#The following are the target SMTP Mail Server and its port
emailServer = ''
serverPort = 25

#The server_response variable will save the response of the server, if any, for printing.
#The new line variable is used when executing the SMTP Commands
server_response = ''
new_line = '\r\n'

#Creating a TCP connection socket.This socket will be used to communicate with the SMTP server
mySocket = socket(AF_INET, SOCK_STREAM)

#Initiating the connection (with a 3-way handshake) with the previously defined SMTP serve.r and its port
mySocket.connect((emailServer, serverPort))
print('Connection Initiated')

#First SMTP command. Used so the server could identify itself, and to initiate the SMTP conversation
hello = 'HELO '+emailServer+new_line
mySocket.send(hello.encode())
#Gathering the response from the server after the command, and printing
server_response = mySocket.recv(1024)
print(server_response)

#SMTP Command 'MAIL FROM: used to define who is the sender of the email
sender = 'MAIL FROM:<'+sender_email+'>'+new_line
mySocket.send(sender.encode())
#Gathering the response from the server after the command, and printing
server_response = mySocket.recv(1024)
print(server_response)

#SMTP Command 'RCPT TO:' used to define who will be the recipient of the email
recipient = 'RCPT TO:<'+rcpt_email+'>'+new_line
mySocket.send(recipient.encode())
#Gathering the response from the server after the command, and printing
server_response = mySocket.recv(1024)
print(server_response)

#SMTP Command 'DATA', used to begin the transfer of the email contents.
data = 'DATA'+new_line
mySocket.send(data.encode())
#Gathering the response from the server after the command, and printing
server_response = mySocket.recv(1024)
print(server_response)

#First part of the email content, the subject
subject = 'Subject: “Email from my email client”'+new_line
mySocket.send(subject.encode())
#This new line was used to separate the subject from the body of the email.
mySocket.send(new_line.encode())

#Body of the email along with a signature from the sender.
email_body = 'This is a test email from my own email client. Hope it finds you well.'+new_line
signature = lastName +','+firstName+new_line
mySocket.send(email_body.encode())
mySocket.send(signature.encode())

#A dot '.' is used to inform the server that all email contents have been sent.
end_dot = '.'+new_line
mySocket.send(end_dot.encode())
#Gathering the response from the server after the command if any, and printing
server_response = mySocket.recv(1024)
print(server_response)

#SMTP Command 'QUIT' asks the server to close the connection
quit = 'QUIT'+new_line
mySocket.send(quit.encode())
#Gathering the response from the server after the command if any, and printing
server_response = mySocket.recv(1024)
print(server_response)

#Closing the TCP connection
mySocket.close()
