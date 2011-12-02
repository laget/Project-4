# Team Laget
# Scott Surette
# Zane Whitney
# Rani Aljondi

import os
import socket
import sys
import threading
import argparse

class Header:
	def __init__(self, date, server, connection, contentLength, contentType):
		self.date = date
		self.server = server
		self.connection = connection
		self.contentLength = contentLength
		self.contentType = contentType
		
		
def main (directory, port=8080):
	# main definition here
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("", port))
	server_socket.listen(5)
	
	print ("Waiting for requests on port", port)
	
	while 1:
		client_socket, address = server_socket.accept()
		print ("id CONNECT") # note - need to assign id
		ct = client_thread(clientsocket)
		print ("id REQUEST") # note - need to assign id
		ct.run()
		# need to check here if requested page can be found:
		# check mime type - see notes.txt - need to check file extension
		# if it can be found, print "id DELIVERED" and return requested file
		# if it can't be found, print "HTTP/1.0 404 Not Found"
		
		# when returning the requested file: 
		# print "HTTP/1.0 200 OK"
		# Header.date = currentDate
		# Header.server = serverName
		# Header.connection = close
		# Header.contentLength = numberOfBytesInContent
		# Header.contentType = header for mime type - see above and notes.txt
		# return Header, return requested file
		

if __name__ == "__main__":
	if (len(sys.argv) < 4):
		main (sys.argv[1])
	else:
		main (sys.argv[3], int(sys.argv[2]))