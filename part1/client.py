import socket
import sys
from thread import *
import getpass
import os

'''
Function Definition
'''
def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.0.4'
port = 9486
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''
# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server
while 1:
	for x in range(0,2):
		if x == 0:
			msg = raw_input('Login:')
		else:
			msg = getpass.getpass('Password: ')
		s.sendto(msg, (host, port))

'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''
reply = s.recv(5)
if reply == 'yes': # TODO: use the correct string to replace xxx here!

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	while True :

		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Post a message \n 3. Change password \n")
		
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			s.sendto(message, (host, port))
			if message == str(1):
				print 'Logout'
				# TODO: add logout operation
				sys.exit()
			if message == str(2):
				print 'Post a message'
			if message == str(3):
				message = getpass.getpass('Enter your old password: ')
				try:
					s.sendto(message, (host, port))
				except socket.error, msg:
					print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
					sys.exit()
				message = getpass.getpass('Enter your new password: ')
				try:
					s.sendto(message, (host, port))
				except socket.error, msg:
					print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
					sys.exit()
								

				if reply == 'yes':
					print 'Password changed successfully'
				else:
					print 'Your old password does not match.'
			# Add other operations, e.g. change password
		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'

s.close()
