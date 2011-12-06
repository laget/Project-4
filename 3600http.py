# Team Laget
# Scott Surette
# Zane Whitney
# Rani Aljondi

import os
import socket
import sys
import threading
import datetime

class Header:
	def __init__(self, date, server, connection, contentLength, contentType):
		self.date = date
		self.server = server
		self.connection = connection
		self.contentLength = contentLength
		self.contentType = contentType

class Response:
	def __init__(self, Header, data):
		self.Header = Header
		self.data = data


def main (directory, port=8080):
	# main definition here

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("", port))

	print ("Waiting for requests on port", port)

	while 1:
		server_socket.listen(5)
		client_socket, address = server_socket.accept()

		print ("Client socket:", client_socket)
		print ("Address:", address)

		print ("id CONNECT") # note - need to assign id

		request = str(client_socket.recv(4096))
		print ("Request:", request)

		print ("id REQUEST") # note - need to assign id

		# need to check here if requested page can be found:
		# check mime type - see notes.txt - need to check file extension
		# if it can be found, print "id DELIVERED" and return requested file
		# if it can't be found, print "HTTP/1.0 404 Not Found"

		rlist = request.split()
		print (rlist)
		print (len(rlist))

		if (len(rlist) > 1):
			path = rlist[1]
			print (path)

		abspath = directory + str(path)

		print (abspath)

		if (os.path.exists(abspath)):
			fd = open(abspath, "r")
                        file = fd.read()
                        client_socket.sendall(file)

                        okmsg = "HTTP/1.0 200 OK\r\n"
                        now = datetime.datetime.now()
                        server = "Vår http-server 1.0\r\n"
                        connection = "close\r\n"
                        content_length = len(file)



                        header = Header();
		else:
			client_socket.sendall(b"HTTP/1.0 404 Not Found")


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
