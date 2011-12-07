# -*- coding: latin-1 -*-
# Team Laget
# Scott Surette
# Zane Whitney
# Rani Aljondi

import os
import socket
import sys
import thread
import datetime
import mimetypes

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

def buildpath(socket, basedir):
        """Builds a directory path to a file from an HTTP request."""

        request = str(socket.recv(4096))
        print "Request recieved: " + request

        reqlist = request.split()
        print "Request in list form: " + str(reqlist)
        print "Length of reqlist: " +  str(len(reqlist))

        if (len(reqlist) > 1):
                endpath = reqlist[1]
                print (endpath)

		abspath = basedir + str(endpath)
		print "Full path constructed: " + str(abspath)

                return abspath



def servicerequest(path, socket):
        """Services an HTTP request based on the provided file path"""

        if (os.path.exists(path)):
                fd = open(path, "r")
                file = fd.read()
                socket.sendall(file)

                okmsg = "HTTP/1.0 200 OK\r\n"
                now = datetime.datetime.now()

                datestr = now.strftime("%a, %d %B %G %H:%M:%S %Z")

                print "Formatted date and time: " + datestr

                server = "Server: Vår http-server 1.0\r\n"
                connection = "Connection: close\r\n"
                content_length = sys.getsizeof(file)
                content_type = mimetypes.guess_type(path)[0]

                httpresponse = str(okmsg) + datestr

                print "Content Type Header: " + content_type
                print "Size of file in bytes: " + str(content_length)

        # header = Header();
        else:
                socket.sendall(b"HTTP/1.0 404 Not Found")

                # when returning the requested file:
                # print "HTTP/1.0 200 OK"
                # Header.date = currentDate
                # Header.server = serverName
                # Header.connection = close
                # Header.contentLength = numberOfBytesInContent
                # Header.contentType = header for mime type - see above and notes.txt
                # return Header, return requested file

                return None

def main (directory, port=8080):

        # Building socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("", port))

	print "Waiting for requests on port " + str(port)

	while 1:
		server_socket.listen(5)
		client_socket, address = server_socket.accept()

		print "Client socket: " + str(client_socket)
		print "Address: " + str(address)

		print "id CONNECT" # note - need to assign id
		print "id REQUEST" # note - need to assign id

		# need to check here if requested page can be found:
		# check mime type - see notes.txt - need to check file extension
		# if it can be found, print "id DELIVERED" and return requested file
		# if it can't be found, print "HTTP/1.0 404 Not Found"

                searchpath = buildpath(client_socket, directory)

                servicerequest(searchpath, client_socket)



if __name__ == "__main__":
	if (len(sys.argv) < 4):
		main (sys.argv[1])
	else:
		main (sys.argv[3], int(sys.argv[2]))
