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

def buildpath(socket, basedir, httpid):
    """Builds a directory path to a file from an HTTP request."""
    request = socket.recv(4096)
    print str(httpid) + " REQUEST"
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

def servicerequest(path, socket, httpid):
    """Services an HTTP request based on the provided file path"""

    if (os.path.exists(path)):
        print str(httpid) + " DELIVERED"
        fd = open(path, "r")
        file = fd.read()

        okmsg = "HTTP/1.0 200 OK\r\n"
        now = datetime.datetime.now()

        datestr = now.strftime("%a %d %B %Y %H:%M:%S %z") + "\r\n"

        print "Date and time: " + datestr

        server = "Server: Var http-server 1.0\r\n"
        connection = "Connection: close\r\n"
        content_length = "Content length: " + str(sys.getsizeof(file)) + "\r\n"
        content_type = "Content type: " + mimetypes.guess_type(path)[0] + "\r\n\r\n"

        print content_type
        print content_length

        header = datestr + server + connection + content_length + content_type

        socket.sendall(okmsg + header + file)
        socket.close()
    else:
        print str(httpid) + " NOTFOUND"
        socket.sendall("HTTP/1.0 404 Not Found\r\n")
        socket.close()
        print str(httpid) + " CLOSE"

    return None

def main (directory, port=8080):

    httpid = 0

    # Building socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))

    print "Waiting for requests on port " + str(port)

    while 1:
        server_socket.listen(5)
        client_socket, address = server_socket.accept()

        httpid += 1
        print str(httpid) + " CONNECT"

        print "Client socket: " + str(client_socket)
        print "Address: " + str(address)

        searchpath = buildpath(client_socket, directory, httpid)

        thread.start_new_thread(servicerequest, (searchpath, client_socket, httpid))



if __name__ == "__main__":
    if (len(sys.argv) < 4):
        main (sys.argv[1])
    else:
        main (sys.argv[3], int(sys.argv[2]))
