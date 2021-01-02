from __future__ import print_function

import getpass
import json
import socket

from threading import Timer

HOST = '10.0.0.4'
PORT = 9486

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def login():
	usr = raw_input("Username [%s]: " % getpass.getuser())
	if not user:
		usr = getpass.getuser()

	prompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

	pswd, conf = prompt()
	while pswd != conf:
		print('Passwords are not the same, retry')
		pswd, conf = prompt()

	return usr, pswd

while 1:
	p, addr = s.recvfrom(1024)
	print(p, end='')
	
	if p == 'done\n':
		break;

	reply = ''
	if 'Password' in p and 'Options' not in p:
		reply = getpass.getpass('')
	else:
		reply = raw_input()

	s.send(reply)

s.close()
