from socket import *
import ssl
import base64

#Both variables lastName and firstName refer to whoever is running or the author of this script
lastName = 'Ramirez'
firstName = 'Diana'

#Variable storing the email address of sender
sender_email = 'snder@gmail.com'

#Variable storing the email address of recipient
rcpt_email = 'rcpt@gmail.com'

#The following are the target SMTP Mail Server and its port
emailServer = 'smtp.gmail.com'
serverPort = 587

#The server_response variable will save the response of the server, if any, for printing.
#The new line variable is used when executing the SMTP Commands
server_response = ''
new_line = '\r\n'

##Credentials to send to server converted to bytes for base64 encoding
usrname = b'username@gmail.com'
passwd = b'yourownpassword'

#Creating a TCP connection socket.This socket will be used to communicate with the SMTP server
mySocket = socket(AF_INET, SOCK_STREAM)

#Initiating the connection (with a 3-way handshake) with the previously defined SMTP server and its port
mySocket.connect((emailServer, serverPort))
server_response = mySocket.recv(1024)
print(server_response)

#EHLO stands for Extended Hello,similar to the HELO command but this is used for ESMTP protocol.
ehlo = 'EHLO gmail.com'+new_line
mySocket.send(ehlo.encode())
server_response = mySocket.recv(1024)
print(server_response)

#STARTTLS command needed for communication that requires TLS.
stls = 'STARTTLS'+new_line
mySocket.send(stls.encode())
server_response = mySocket.recv(1024)
print(server_response)

##Need to wrap the socket using ssl_version matching google's protocol before authentication
wrap = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_SSLv23)

#AUTH LOGIN command is used before authenticating client
auth_l = 'AUTH LOGIN'+new_line
wrap.send(auth_l.encode())
server_response = wrap.recv(1024)
##The server response VXNlcm5hbWU6 is base64 for 'Username:'
print(server_response)

#Sending the username value
wrap.send(base64.b64encode(usrname)+ b'\r\n')
server_response = wrap.recv(1024).decode()
#The server response UGFzc3dvcmQ6 is base64 for 'Password:'
print(server_response)

wrap.send(base64.b64encode(passwd)+ b'\r\n')
server_response = wrap.recv(1024).decode()
##Server will either Accept or Reject the inputted credentials
print(server_response)

sender = 'MAIL FROM:<'+sender_email+'>'+new_line
wrap.send(sender.encode())
#Gathering the response from the server after the command, and printing
server_response = wrap.recv(1024)
print(server_response)

#SMTP Command 'RCPT TO:' used to define who will be the recipient of the email
recipient = 'RCPT TO:<'+rcpt_email+'>'+new_line
wrap.send(recipient.encode())
#Gathering the response from the server after the command, and printing
server_response = wrap.recv(1024)
print(server_response)

#SMTP Command 'DATA', used to begin the transfer of the email contents.
data = 'DATA'+new_line
wrap.send(data.encode())
#Gathering the response from the server after the command, and printing
server_response = wrap.recv(1024)
print(server_response)

#the email ubject
subject = 'Subject: “Email from my Gmail email client”'+new_line
wrap.send(subject.encode())
#This new line was used to separate the subject from the body of the email.
wrap.send(new_line.encode())


#Body of the email along with a signature from the sender.
email_body = 'This is a test email from my own gmail email client. Hope it finds you well.'+new_line
signature = lastName +','+firstName+new_line
wrap.send(email_body.encode())
wrap.send(signature.encode())

#A dot '.' is used to inform the server that all email contents have been sent.
end_dot = '.'+new_line
wrap.send(end_dot.encode())
#Gathering the response from the server after the command if any, and printing
server_response = wrap.recv(1024)
print(server_response)

#SMTP Command 'QUIT' asks the server to close the connection
quit = 'QUIT'+new_line
wrap.send(quit.encode())
#Gathering the response from the server after the command if any, and printing
server_response = wrap.recv(1024)
print(server_response)

#Closing the connection
wrap.close()