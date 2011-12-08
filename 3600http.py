# Team Laget
# Scott Surette
# Zane Whitney
# Rani Aljondi

import os, socket, sys, thread, datetime, mimetypes

def buildpath(socket, basedir):
    """Builds a directory path to a file from an HTTP request."""
    request = socket.recv(4096)
    print "id REQUEST" # note - need to assign id
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
        print "id DELIVERED" # note - need to assign id
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
    else:
        socket.sendall("HTTP/1.0 404 Not Found\r\n")

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

        print "id CONNECT" # note - need to assign id

        print "Client socket: " + str(client_socket)
        print "Address: " + str(address)

        searchpath = buildpath(client_socket, directory)

        thread.start_new_thread(servicerequest, (searchpath, client_socket))



if __name__ == "__main__":
    if (len(sys.argv) < 4):
        main (sys.argv[1])
    else:
        main (sys.argv[3], int(sys.argv[2]))
