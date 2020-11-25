from socket import *

serverName = 'localhost' 
serverPort = 6666 
serverAddress=(serverName, serverPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)

alias1 = input("Entrer votre alias: ")
clientSocket.sendto(alias1.encode("UTF-8"), serverAddress)


while True:
	action, serverAddress = clientSocket.recvfrom(1024)
	if action.decode() == "S":
		message, serverAddress = clientSocket.recvfrom(1024)
		if message.decode() == "exit":
			clientSocket.close()
		else:
			print(message.decode())
	elif action.decode() == "R":
		message = input()
		clientSocket.sendto(message.encode("UTF-8"), serverAddress)





