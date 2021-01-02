import json
import socket
import datetime

from inspect import cleandoc
from thread import *

HOST = '10.0.0.4'
PORT = 9486

clients = { 
	'user3': {
		'password': '123',
		'isOnline': False,
		'connection': None,
		'newpost': 0,
		'queue': [],
		'fqueue': [],
		'friends': [],
		'groups' : ['group 1', 'group 2', 'group 3'],
		
	}, 
	'user1': {
		'password': '123',
		'isOnline': False,
		'connection': None,
		'newpost': 0,
		'queue': [],
		'fqueue': [],
		'friends': [],
		'groups' : ['group1', 'group2', 'group3'],
	},
	'user2': {
		'password': '123',
		'isOnline': False,
		'connection': None,
		'newpost': 0,
		'queue': [],
		'fqueue': [],
		'friends': [],
		'groups' : ['group1', 'group2', 'group3'],
	} 
}

groups = {
	'group1': {
		'members': [],
	},
	'group2': {
		'members': [],
	},
	'group3': {
		'members': [],
	},
}

def timestamp():
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	return time[:-4]

def client_thread(conn):
	try:
		conn.send('Welcome to the server. Type something and hit enter\n')
		conn.send('Username: ')
		usr = conn.recv(1024)
		conn.send('Password: ')
		pswd = conn.recv(1024)

		if usr not in clients or clients[usr]['password'] != pswd:
			conn.send('Invalid username or password\n')
			conn.close()
		
		clients[usr]['isOnline'] = True;
		clients[usr]['connection'] = conn;
		
		options = cleandoc("""
		Choose an option:
		1. Change Password
		2. Logout
		3. Send Message
		4. View Message
		5. Broadcast Message
		6. List Groups
		""")
	
		goptions = cleandoc("""
		Choose an option:
		1. Request to Join Group
		2. Show Groups
		3. Send Group Message
		4. Quit Group
		5. Cancel Group Options
		""")

		conn.send(options + "\n\n")
		conn.send('{} unread messages\n'.format(len(clients[usr]['queue'])))
		#conn.send('{} pending friend requests\n'.format(len(clients[usr]['fqueue'])))
		#conn.send('{} new posts on your timeline\n\n'.format(clients[usr]['newpost']))

		while 1:
			data = conn.recv(1024)
			if not data:
				conn.send('Failed to interpret, retry?')
				continue
			
			if data == '3': #send message
				conn.send('Send to: ')
				target = conn.recv(1024)
				conn.send('Message to send: ')
				msg = conn.recv(1024)
				msg = msg + '\n'
			
				if clients[target]['isOnline']:
					conn.send('Message sent!\n\n')
					clients[target]['connection'].send('{}: {}'.format(usr, msg))
					clients[target]['connection'].send(options)
				else:
					conn.send('User is offline and will receive this message later.\n\n')
					clients[target]['queue'].append({'from': usr, 'message': msg})

			if data == '5': #broadcast message
				conn.send('Message: ')
				msg = conn.recv(1024)
				msg = msg + '\n'
				for usrs in clients:
					if clients[usrs]['isOnline']:
						clients[usrs]['connection'].send('{}: {}'.format(usr, msg))
						clients[usrs]['connection'].send(options)
				
				conn.send('Broadcast message sent!')
			
			if data == '4': #view messages
				
				for message in clients[usr]['queue']:
					conn.send('{}: {}'.format(message['from'], message['message']))
				
				del clients[usr]['queue'][:]

					
			if data == '6': #list groups				
				conn.send(goptions + "\n\n")
				while 1:
					gdata = conn.recv(1024)
					if gdata == '2': #show groups
						for f in clients[usr]['groups']:
							conn.send(f + "\n")

					if gdata == '1':#join group
						conn.send("Group to join: ")
						gtoadd = conn.recv(1024)
						if gtoadd not in groups:
							conn.send("Group does not exist \n")
						else:
							groups[gtoadd]['members'].append(usr)
							clients[usr]['groups'].append(usr)
							conn.send("Successfully joined group!")
					if gdata == '3':#send message to group
						conn.send('Group to send message: ')
						targets = conn.recv(1024)
						conn.send('Message to send: ')
						msg = conn.recv(1024)
						msg = msg + "\n"

						for usrs in clients:
							if clients[usrs]['isOnline']:
								clients[usrs]['connection'].send('{}: {}'.format(usr, msg))
								clients[usrs]['connection'].send(options)
						conn.send('Group message sent!')
						
					if gdata == '4': #quit group
						conn.send('List of groups')
						for f in clients[usr]['groups']:
							conn.send(f + "\n")

						conn.send('Choose group to leave')
						rgroup = conn.recv(1024)
						clients[usr]['groups'].remove(rgroup)
						clients[rgroups]['groups'].remove(usr)
						conn.send("Successfully left group!")

					if gdata == '5':#exit group options
						conn.send("Leaving group menu ..\n")
						break
					conn.send("\n\n" + goptions + "\n\n")
				
				
			if data == '1': #change password
				conn.send('Old Password: ')
				oldPswd = conn.recv(1024)
				conn.send('New Password: ')
				newPswd = conn.recv(1024)
				
				if oldPswd == clients[usr]['password']:
					clients[usr]['password'] = newPswd
					conn.send('Password changed.\n')
				else:
					conn.send('Old passwords do not match.')
			if data == '2': #logout
				clients[usr]['isOnline'] = False
				conn.send('user logout\n')
				conn.close()
		
			conn.send('\n\n' + options + "\n\n")
			conn.send('{} unread messages\n'.format(len(clients[usr]['queue'])))
			#conn.send('{} pending friend requests\n'.format(len(clients[usr]['fqueue'])))
			#conn.send('{} new posts on your timeline\n\n'.format(clients[usr]['newpost']))
	except:
		print('Client disconnected')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)
#print('Waiting for clients:{}'.format(PORT))

while 1:
	conn, addr = s.accept()
	print('Connected with {}:{}'.format(addr[0], addr[1]))
	start_new_thread(client_thread, (conn,))

s.close()	
